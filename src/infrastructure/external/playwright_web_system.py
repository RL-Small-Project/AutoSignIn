import asyncio
import requests
import dotenv
from concurrent.futures import ThreadPoolExecutor
from playwright.sync_api import sync_playwright, Browser, Page, Playwright as SyncPlaywright
from typing import Optional
import threading

from ...domain.services.attendance_service import WebAttendanceSystem
from ...domain.value_objects.attendance_record import AttendanceRecord
from ...domain.value_objects.attendance_status import AttendanceStatusType
from ...domain.exceptions import AttendanceProcessingError


class PlaywrightWebAttendanceSystem(WebAttendanceSystem):
    """使用Playwright實作的網頁點名系統"""
    
    def __init__(self):
        dotenv.load_dotenv()
        self._base_url = dotenv.get_key(dotenv_path=".env", key_to_get="URL")
        self._playwright: Optional[SyncPlaywright] = None
        self._browser: Optional[Browser] = None
        self._page: Optional[Page] = None
        self._main_frame = None
        self._is_connected = False
        self._executor = ThreadPoolExecutor(max_workers=1)
        self._thread_local = threading.local()
    
    def _get_or_create_playwright(self):
        """在當前線程中獲取或創建 playwright 實例"""
        if not hasattr(self._thread_local, 'playwright') or self._thread_local.playwright is None:
            self._thread_local.playwright = sync_playwright().start()
        return self._thread_local.playwright
    
    def connect(self) -> bool:
        """連接到瀏覽器"""
        try:
            # 如果已經連接，先斷開
            if self._is_connected:
                self.disconnect()
                
            url = f"http://{self._base_url}/json/version"
            headers = {"Host": "localhost"}
            
            resp = requests.get(url, headers=headers, timeout=5)
            token = resp.json()["webSocketDebuggerUrl"].split("/")[-1]
            
            ws_url = f"ws://{self._base_url}/devtools/browser/{token}"
            
            # 在線程池中執行 Playwright 操作
            future = self._executor.submit(self._connect_in_thread, ws_url)
            return future.result(timeout=10)  # 10秒超時
            
        except requests.exceptions.ConnectionError:
            raise AttendanceProcessingError("無法連接到瀏覽器，請確認瀏覽器已啟動並開啟遠端模式")
        except Exception as e:
            raise AttendanceProcessingError(f"連接瀏覽器時發生錯誤: {str(e)}")
    
    def _connect_in_thread(self, ws_url: str) -> bool:
        """在專用線程中連接瀏覽器"""
        try:
            # 在專用線程中使用同步 API
            self._playwright = self._get_or_create_playwright()
            self._browser = self._playwright.chromium.connect_over_cdp(ws_url)
            
            # 獲取現有的 context 和 page
            contexts = self._browser.contexts
            if contexts:
                context = contexts[0]
                pages = context.pages
                if pages:
                    self._page = pages[0]
                    # 等待頁面加載並獲取 main frame
                    self._page.wait_for_load_state()
                    
                    # 查找 main frame
                    for frame in self._page.frames:
                        if frame.name == "main":
                            self._main_frame = frame
                            break
                    
                    # 如果沒有找到 main frame，使用主頁面
                    if not self._main_frame:
                        self._main_frame = self._page.main_frame
            
            self._is_connected = True
            return True
            
        except Exception as e:
            if self._browser:
                try:
                    self._browser.close()
                except:
                    pass
            raise AttendanceProcessingError(f"連接瀏覽器時發生錯誤: {str(e)}")
    
    def verify_student_id(self, excel_student_id: int, index: int) -> bool:
        """驗證學生ID是否與系統一致"""
        if not self._is_connected or not self._main_frame:
            raise AttendanceProcessingError("尚未連接到瀏覽器")
        
        try:
            # 在線程池中執行操作
            future = self._executor.submit(self._verify_student_id_in_thread, excel_student_id, index)
            return future.result(timeout=5)
        except Exception as e:
            raise AttendanceProcessingError(f"驗證學生ID時發生錯誤: {str(e)}")
    
    def _verify_student_id_in_thread(self, excel_student_id: int, index: int) -> bool:
        """在專用線程中驗證學生ID"""
        try:
            element = self._main_frame.locator(f"#dgmuster_lblstdNO_{index}")
            text_content = element.inner_text()
            system_student_id = int(text_content)
            return excel_student_id == system_student_id
        except Exception as e:
            raise AttendanceProcessingError(f"驗證學生ID時發生錯誤: {str(e)}")
    
    def mark_attendance(self, index: int, record: AttendanceRecord) -> None:
        """在網頁上標記出勤狀態"""
        if not self._is_connected or not self._main_frame:
            raise AttendanceProcessingError("尚未連接到瀏覽器")
        
        try:
            # 在線程池中執行操作
            future = self._executor.submit(self._mark_attendance_in_thread, index, record)
            future.result(timeout=5)
        except Exception as e:
            raise AttendanceProcessingError(f"標記出勤狀態時發生錯誤: {str(e)}")
    
    def _mark_attendance_in_thread(self, index: int, record: AttendanceRecord) -> None:
        """在專用線程中標記出勤狀態"""
        try:
            radios = self._main_frame.locator(
                f"input[type='radio'][name*='dgmuster:_ctl{index + 2}:rbl']"
            )
            
            status_type = record.status.status_type
            
            if status_type == AttendanceStatusType.ABSENT:
                radios.nth(2).check()  # 第1節曠課
                radios.nth(5).check()  # 第2節曠課
            elif status_type == AttendanceStatusType.LATE:
                radios.nth(1).check()  # 第1節遲到
            elif status_type == AttendanceStatusType.PARTIAL_ABSENT:
                radios.nth(2).check()  # 第1節曠課
            elif status_type == AttendanceStatusType.LATE_AND_ABSENT:
                radios.nth(2).check()  # 第1節曠課
                radios.nth(4).check()  # 第2節遲到
            # PRESENT 狀態不需要特別標記，預設就是出席
            
        except Exception as e:
            raise AttendanceProcessingError(f"標記出勤狀態時發生錯誤: {str(e)}")
    
    def is_student_on_official_leave(self, index: int) -> bool:
        """檢查學生是否為公假狀態"""
        if not self._is_connected or not self._main_frame:
            raise AttendanceProcessingError("尚未連接到瀏覽器")
        
        try:
            # 在線程池中執行操作
            future = self._executor.submit(self._is_student_on_official_leave_in_thread, index)
            return future.result(timeout=5)
        except Exception as e:
            raise AttendanceProcessingError(f"檢查公假狀態時發生錯誤: {str(e)}")
    
    def _is_student_on_official_leave_in_thread(self, index: int) -> bool:
        """在專用線程中檢查學生是否為公假狀態"""
        try:
            radios = self._main_frame.locator(
                f"input[type='radio'][name*='dgmuster:_ctl{index + 2}:rbl']"
            )
            return radios.nth(0).is_disabled()
        except Exception as e:
            raise AttendanceProcessingError(f"檢查公假狀態時發生錯誤: {str(e)}")
    
    def get_page_title(self) -> str:
        """取得頁面標題"""
        if not self._is_connected or not self._page:
            raise AttendanceProcessingError("尚未連接到瀏覽器")
        
        try:
            # 在線程池中執行操作
            future = self._executor.submit(self._get_page_title_in_thread)
            return future.result(timeout=5)
        except Exception as e:
            raise AttendanceProcessingError(f"取得頁面標題時發生錯誤: {str(e)}")
    
    def _get_page_title_in_thread(self) -> str:
        """在專用線程中取得頁面標題"""
        try:
            return self._page.title()
        except Exception as e:
            raise AttendanceProcessingError(f"取得頁面標題時發生錯誤: {str(e)}")
    
    def disconnect(self) -> None:
        """中斷連接"""
        if self._is_connected:
            # 在線程池中執行斷開操作
            try:
                future = self._executor.submit(self._disconnect_in_thread)
                future.result(timeout=5)
            except Exception:
                pass  # 忽略斷開連接時的錯誤
            finally:
                self._is_connected = False
    
    def _disconnect_in_thread(self) -> None:
        """在專用線程中中斷連接"""
        try:
            if self._browser:
                self._browser.close()
            if hasattr(self._thread_local, 'playwright') and self._thread_local.playwright:
                self._thread_local.playwright.stop()
        except Exception:
            pass  # 忽略斷開連接時的錯誤
        finally:
            self._browser = None
            self._page = None
            self._main_frame = None
            self._playwright = None
            if hasattr(self._thread_local, 'playwright'):
                self._thread_local.playwright = None


class WebAttendanceSystemFactory:
    """網頁點名系統工廠"""
    
    @staticmethod
    def create() -> WebAttendanceSystem:
        """創建並連接網頁點名系統"""
        system = PlaywrightWebAttendanceSystem()
        system.connect()
        return system