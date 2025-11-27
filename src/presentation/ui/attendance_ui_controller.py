from datetime import datetime
from typing import Optional, Callable

import flet as ft

from ...application.services.attendance_application_service import AutoAttendanceApplicationService
from ...application.dto.attendance_dto import AttendanceRequest
from ...domain.value_objects.attendance_record import AttendanceRecord
from ...infrastructure.repositories.excel_attendance_repository import ExcelAttendanceRepository
from ...infrastructure.external.playwright_web_system import WebAttendanceSystemFactory

from .components.title_component import TitleComponent, UIConstants
from .components.input_component import InputComponent
from .components.status_component import StatusComponent
from .components.log_component import LogComponent
from .components.result_component import ResultComponent


class AttendanceUIController:
    """UI控制器"""
    
    def __init__(self):
        # 依賴注入
        self._attendance_repository = ExcelAttendanceRepository()
        self._attendance_service: Optional[AutoAttendanceApplicationService] = None
        
        # UI 組件
        self.title_component = TitleComponent()
        self.input_component = InputComponent()
        self.status_component = StatusComponent(on_start_click=self._start_attendance)
        self.log_component = LogComponent()
        self.result_component = ResultComponent()

    def create_ui(self, page: ft.Page):
        """創建使用者界面"""
        self._setup_page_config(page)
        
        # 創建UI組件容器
        title_container = self.title_component.get_container()
        input_container = self.input_component.get_container()
        status_container = self.status_component.get_container()
        log_container = self.log_component.get_container()
        result_container = self.result_component.get_container()
        
        # 主布局
        main_column = ft.Column([
            title_container,
            input_container,
            status_container,
            log_container,
            result_container,
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0)
        
        # 添加到頁面
        page.add(
            ft.Container(
                content=main_column,
                padding=ft.Padding(20, 20, 20, 20),
                expand=True
            )
        )
    
    def _setup_page_config(self, page: ft.Page):
        """設定頁面基本配置"""
        page.title = UIConstants.APP_TITLE
        page.theme_mode = ft.ThemeMode.LIGHT
        page.window.width = UIConstants.WINDOW_WIDTH
        page.window.height = UIConstants.WINDOW_HEIGHT
        page.window.resizable = False
        page.scroll = ft.ScrollMode.AUTO
    
    def _add_log(self, message: str, color: str = None):
        """新增日誌訊息"""
        self.log_component.add_log(message, color)
    
    def _clear_log(self):
        """清空日誌"""
        self.log_component.clear_log()
    
    def _clear_log_click(self, e):
        """按鈕觸發的清空日誌"""
        self._clear_log()
    
    def _scroll_to_top(self, e):
        """滾動到頂部"""
        self.log_component._scroll_to_top(e)
    
    def _scroll_to_bottom(self, e):
        """滾動到底部"""
        self.log_component._scroll_to_bottom(e)
    
    def _start_attendance(self, e):
        """開始自動點名流程"""
        try:
            # 驗證輸入
            if not self.input_component.get_class_value():
                self._show_error("請選擇班級")
                return
            
            if not self.input_component.get_date_value():
                self._show_error("請輸入日期")
                return
            
            # 驗證日期格式
            try:
                datetime.strptime(self.input_component.get_date_value(), "%Y-%m-%d")
            except ValueError:
                self._show_error("日期格式錯誤，請使用 YYYY-MM-DD 格式")
                return
            
            # 禁用開始按鈕
            self.status_component.set_button_enabled(False)
            
            # 清空之前的日誌和結果
            self._clear_log()
            self.result_component.clear_result()
            
            # 更新狀態
            self.status_component.set_status("正在初始化系統...", ft.Colors.ORANGE)
            self.status_component.set_progress(0.1, True)
            
            self._add_log("🔄 開始自動點名流程...")
            
            # 創建請求
            request = AttendanceRequest(
                class_name=self.input_component.get_class_value(),
                date=self.input_component.get_date_value()
            )
            
            # 初始化服務
            self.status_component.set_status("正在連接瀏覽器...")
            self.status_component.set_progress(0.3)
            
            web_system = WebAttendanceSystemFactory.create()
            self._attendance_service = AutoAttendanceApplicationService(
                self._attendance_repository,
                web_system
            )
            
            self._add_log("✅ 瀏覽器連接成功！", ft.Colors.GREEN)
            self._add_log(f"📋 頁面標題: {web_system.get_page_title()}")
            
            # 執行自動點名
            self.status_component.set_status("正在執行自動點名...")
            self.status_component.set_progress(0.6)
            
            # 執行自動點名，傳遞進度回調
            result = self._attendance_service.execute_auto_attendance(
                request,
                progress_callback=self._progress_callback
            )
            
            # 顯示結果
            self.status_component.set_progress(1.0)
            
            if result.success:
                self.status_component.set_status("點名完成！", ft.Colors.GREEN)
                self._add_log("✅ 自動點名完成！", ft.Colors.GREEN)
                self.result_component.show_result(result.get_summary())
            else:
                self.status_component.set_status("點名失敗", ft.Colors.RED)
                self._add_log(f"❌ 點名失敗！", ft.Colors.RED)
                
                for error in result.errors:
                    self._add_log(f"  • {error}", ft.Colors.RED)
            
        except Exception as ex:
            self._show_error(f"未預期錯誤: {str(ex)}")
        finally:
            # 重新啟用開始按鈕
            self.status_component.set_button_enabled(True)
    
    def _progress_callback(self, action: str, record, current: int, total: int):
        """進度回調函數 - 在 UI 中顯示學生處理狀態"""
        student_name = record.student.name.value
        student_id = record.student.student_id.value
        status_desc = record.status.description or "正常出席"
        
        # 更新進度條
        progress_value = current / total * 0.4 + 0.6  # 從 0.6 到 1.0
        self.status_component.set_progress(progress_value)
        
        # 創建進度指示器
        progress_text = f"[{current:2d}/{total:2d}]"
        
        if action == "present":
            self._add_log(f"{progress_text} ✅ 出席: {student_name}", ft.Colors.GREEN)
        elif action == "absent":
            self._add_log(f"{progress_text} ❌ 缺席/遲到: {student_name} - {status_desc}", ft.Colors.ORANGE)
        elif action == "official_leave":
            self._add_log(f"{progress_text} 🏛️ 公假: {student_name}", ft.Colors.BLUE)
        elif action == "error":
            self._add_log(f"{progress_text} ⚠️ 錯誤: {student_name}", ft.Colors.RED)
    
    def _show_error(self, message: str):
        """顯示錯誤訊息"""
        self.status_component.set_status(message, ft.Colors.RED)
        self.status_component.set_progress(0, False)
        
        self._add_log(f"❌ {message}", ft.Colors.RED)
        
        # 重新啟用開始按鈕
        self.status_component.set_button_enabled(True)


def create_ui_app() -> Callable[[ft.Page], None]:
    """創建UI應用程式"""
    def main(page: ft.Page):
        controller = AttendanceUIController()
        controller.create_ui(page)
    
    return main