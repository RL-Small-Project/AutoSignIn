import sys
from datetime import datetime
from typing import Optional

from ...application.services.attendance_application_service import AutoAttendanceApplicationService
from ...application.dto.attendance_dto import AttendanceRequest
from ...domain.value_objects.attendance_record import AttendanceRecord
from ...infrastructure.repositories.excel_attendance_repository import ExcelAttendanceRepository
from ...infrastructure.external.playwright_web_system import WebAttendanceSystemFactory


class AttendanceCliController:
    """命令列介面控制器"""
    
    def __init__(self):
        # 依賴注入
        self._attendance_repository = ExcelAttendanceRepository()
        self._attendance_service: Optional[AutoAttendanceApplicationService] = None
    
    def run(self):
        """執行命令列介面"""
        print("📢 自動點名系統 (命令列模式)")
        print("============================")
        
        try:
            # 獲取用戶輸入
            class_name = self._get_class_name()
            date = self._get_date()
            
            # 創建請求
            request = AttendanceRequest(class_name=class_name, date=date)
            
            # 初始化服務（需要連接瀏覽器）
            print("正在連接瀏覽器...")
            web_system = WebAttendanceSystemFactory.create()
            self._attendance_service = AutoAttendanceApplicationService(
                self._attendance_repository,
                web_system
            )
            
            print(f"📋 頁面標題: {web_system.get_page_title()}")
            print("開始執行自動點名...")
            print("=" * 50)
            
            # 執行自動點名，傳遞進度回調
            result = self._attendance_service.execute_auto_attendance(
                request, 
                progress_callback=self._progress_callback
            )
            
            # 顯示結果
            self._display_result(result)
            
        except KeyboardInterrupt:
            print("\n\n⚠️ 使用者中斷操作")
        except Exception as e:
            print(f"\n❌ 發生錯誤: {str(e)}")
        finally:
            print("\n👋 程式結束")
    
    def _progress_callback(self, action: str, record, current: int, total: int):
        """進度回調函數 - 顯示學生處理狀態"""
        student_name = record.student.name.value
        student_id = record.student.student_id.value
        status_desc = record.status.description or "正常出席"
        
        # 創建進度指示器
        progress = f"[{current:2d}/{total:2d}]"
        
        if action == "present":
            print(f"{progress} ✅ 出席: {student_name}")
        elif action == "absent":
            print(f"{progress} ❌ 缺席/遲到: {student_name} - {status_desc}")
        elif action == "official_leave":
            print(f"{progress} 🏛️ 公假: {student_name}")
        elif action == "error":
            print(f"{progress} ⚠️ 錯誤: {student_name} - 處理失敗")
    
    def _get_class_name(self) -> str:
        """獲取班級名稱"""
        while True:
            class_name = input("請輸入班級(A/B): ").strip().upper()
            if class_name in ["A", "B"]:
                return class_name
            print("❌ 請輸入有效的班級名稱 (A 或 B)")
    
    def _get_date(self) -> str:
        """獲取日期"""
        while True:
            date_str = input("輸入日期 (格式: YYYY-MM-DD): ").strip()
            try:
                # 驗證日期格式
                datetime.strptime(date_str, "%Y-%m-%d")
                return date_str
            except ValueError:
                print("❌ 日期格式錯誤，請使用 YYYY-MM-DD 格式")
    
    def _display_result(self, result):
        """顯示執行結果"""
        print("\n" + "=" * 30)
        
        if result.success:
            print("✅ 自動點名完成！")
            print(f"📊 {result.get_summary()}")
        else:
            print("❌ 自動點名失敗")
            print(f"原因: {result.message}")
            
            if result.errors:
                print("\n錯誤詳情:")
                for error in result.errors:
                    print(f"  • {error}")
        
        print("=" * 30)