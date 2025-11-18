import os
from datetime import datetime
from typing import Optional, Callable

import flet as ft

from ...application.services.attendance_application_service import AutoAttendanceApplicationService
from ...application.dto.attendance_dto import AttendanceRequest
from ...domain.value_objects.attendance_record import AttendanceRecord
from ...infrastructure.repositories.excel_attendance_repository import ExcelAttendanceRepository
from ...infrastructure.external.playwright_web_system import WebAttendanceSystemFactory


class AttendanceUIController:
    """UI控制器"""
    
    def __init__(self):
        # 依賴注入
        self._attendance_repository = ExcelAttendanceRepository()
        self._attendance_service: Optional[AutoAttendanceApplicationService] = None
        
        # UI 元件
        self.class_dropdown = None
        self.date_picker = None
        self.status_text = None
        self.progress_bar = None
        self.log_container = None
        self.result_text = None
        self.start_button = None
        self.result_container = None

    def create_ui(self, page: ft.Page):
        """創建使用者界面"""
        page.title = "中國科技大學-自動化點名系統"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.window.width = 650
        page.window.height = 750
        page.window.resizable = False
        page.scroll = ft.ScrollMode.AUTO
        
        # 標題區塊
        title_container = ft.Container(
            content=ft.Column([
                ft.Text(
                    "📢 中國科技大學-自動化點名系統",
                    size=32,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_800,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Text(
                    "Design by Raylon",
                    size=16,
                    color=ft.Colors.GREY_600,
                    text_align=ft.TextAlign.CENTER
                ),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=ft.Colors.BLUE_50,
            padding=ft.Padding(20, 20, 20, 20),
            border_radius=10,
            margin=ft.Margin(0, 0, 0, 20)
        )
        
        # 輸入區塊
        self.class_dropdown = ft.Dropdown(
            label="選擇班級",
            hint_text="請選擇班級",
            options=[
                ft.dropdown.Option("A", "A班"),
                ft.dropdown.Option("B", "B班"),
            ],
            expand=True,
            border_color=ft.Colors.BLUE_400,
        )
        
        self.date_picker = ft.TextField(
            label="日期 (YYYY-MM-DD)",
            hint_text="例: 2025-11-11",
            value=datetime.now().strftime("%Y-%m-%d"),
            expand=True,
            border_color=ft.Colors.BLUE_400,
        )
        
        input_container = ft.Container(
            content=ft.Column([
                ft.Text("📝 基本設定", size=18, weight=ft.FontWeight.BOLD),
                ft.Row([
                    ft.Icon(ft.Icons.SCHOOL, color=ft.Colors.BLUE),
                    ft.Text("班級：", size=16),
                    self.class_dropdown,
                ], alignment=ft.MainAxisAlignment.START),
                ft.Row([
                    ft.Icon(ft.Icons.DATE_RANGE, color=ft.Colors.BLUE),
                    ft.Text("日期：", size=16),
                    self.date_picker,
                ], alignment=ft.MainAxisAlignment.START),
            ], spacing=15),
            bgcolor=ft.Colors.WHITE,
            padding=ft.Padding(20, 15, 20, 15),
            border_radius=10,
            border=ft.border.all(1, ft.Colors.BLUE_200),
            margin=ft.Margin(0, 0, 0, 20)
        )
        
        # 狀態顯示
        self.status_text = ft.Text(
            "請選擇班級和日期後點擊開始",
            size=14,
            color=ft.Colors.GREY_600,
            text_align=ft.TextAlign.CENTER
        )
        
        # 進度條
        self.progress_bar = ft.ProgressBar(
            value=0,
            width=500,
            visible=False,
            color=ft.Colors.GREEN,
            bgcolor=ft.Colors.GREY_300,
            border_radius=10,
        )
        
        # 開始按鈕
        self.start_button = ft.ElevatedButton(
            text="開始自動點名",
            icon=ft.Icons.PLAY_ARROW,
            on_click=self._start_attendance,
            width=200,
            height=50,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.GREEN_400,
                color=ft.Colors.WHITE,
                text_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD)
            )
        )
        
        # 狀態容器
        status_container = ft.Container(
            content=ft.Column([
                self.status_text,
                self.progress_bar,
                self.start_button,
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
            bgcolor=ft.Colors.GREY_50,
            padding=ft.Padding(20, 15, 20, 15),
            border_radius=10,
            margin=ft.Margin(0, 0, 0, 20)
        )
        
        # 日誌容器
        self.log_container = ft.ListView(
            height=300,
            spacing=3,
            padding=ft.Padding(10, 10, 10, 10),
            expand=True,
            auto_scroll=False,
        )
        
        log_title_container = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.LIST_ALT, color=ft.Colors.BLUE),
                    ft.Text("執行日誌", size=18, weight=ft.FontWeight.BOLD),
                    ft.Container(expand=True),  # 寬度 auto
                    ft.Row([
                        ft.IconButton(
                            icon=ft.Icons.KEYBOARD_ARROW_UP,
                            tooltip="滾動到頂部",
                            on_click=self._scroll_to_top,
                            icon_size=20
                        ),
                        ft.IconButton(
                            icon=ft.Icons.KEYBOARD_ARROW_DOWN,
                            tooltip="滾動到底部",
                            on_click=self._scroll_to_bottom,
                            icon_size=20
                        ),
                        ft.IconButton(
                            icon=ft.Icons.CLEAR,
                            tooltip="清空日誌",
                            on_click=self._clear_log_click,
                            icon_size=20
                        ),
                    ])
                ]),
                ft.Container(
                    content=self.log_container,
                    border=ft.border.all(1, ft.Colors.GREY_300),
                    border_radius=10,
                    bgcolor=ft.Colors.WHITE,
                ),
            ], spacing=10),
            bgcolor=ft.Colors.GREY_50,
            padding=ft.Padding(20, 15, 20, 15),
            border_radius=10,
            margin=ft.Margin(0, 0, 0, 20)
        )
        
        # 結果顯示
        self.result_text = ft.Text(
            "",
            size=16,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.GREEN_800,
            text_align=ft.TextAlign.CENTER
        )
        
        result_container = ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.ASSESSMENT, color=ft.Colors.GREEN, size=24),
                self.result_text,
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
            bgcolor=ft.Colors.GREEN_50,
            padding=ft.Padding(20, 15, 20, 15),
            border_radius=10,
            visible=False
        )
        
        self.result_container = result_container
        
        # 主布局
        main_column = ft.Column([
            title_container,
            input_container,
            status_container,
            log_title_container,
            result_container,
        ], 
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=0)
        
        # 添加到頁面
        page.add(
            ft.Container(
                content=main_column,
                padding=ft.Padding(20, 20, 20, 20),
                expand=True
            )
        )
    
    def _add_log(self, message: str, color: str = None):
        """新增日誌訊息"""
        if color is None:
            color = ft.Colors.BLACK
        
        log_item = ft.Container(
            content=ft.Text(
                message,
                size=12,
                color=color
            ),
            padding=ft.Padding(5, 2, 5, 2)
        )
        self.log_container.controls.append(log_item)
        
        # 手動滾動到最底部以顯示最新訊息
        self.log_container.update()
        
        # 使用異步方式滾動到底部
        try:
            if len(self.log_container.controls) > 0:
                self.log_container.scroll_to(
                    offset=-1,  # 滾動到最底部
                    duration=100
                )
        except:
            pass  # 忽略滾動錯誤
    
    def _clear_log(self):
        """清空日誌"""
        self.log_container.controls.clear()
        self.log_container.update()
    
    def _clear_log_click(self, e):
        """按鈕觸發的清空日誌"""
        self._clear_log()
    
    def _scroll_to_top(self, e):
        """滾動到頂部"""
        try:
            self.log_container.scroll_to(offset=0, duration=300)
        except:
            pass
    
    def _scroll_to_bottom(self, e):
        """滾動到底部"""
        try:
            self.log_container.scroll_to(offset=-1, duration=300)
        except:
            pass
    
    def _start_attendance(self, e):
        """開始自動點名流程"""
        try:
            # 驗證輸入
            if not self.class_dropdown.value:
                self._show_error("請選擇班級")
                return
            
            if not self.date_picker.value:
                self._show_error("請輸入日期")
                return
            
            # 驗證日期格式
            try:
                datetime.strptime(self.date_picker.value, "%Y-%m-%d")
            except ValueError:
                self._show_error("日期格式錯誤，請使用 YYYY-MM-DD 格式")
                return
            
            # 禁用開始按鈕
            self.start_button.disabled = True
            self.start_button.update()
            
            # 清空之前的日誌和結果
            self._clear_log()
            self.result_text.value = ""
            self.result_container.visible = False
            self.result_container.update()
            
            # 更新狀態
            self.status_text.value = "正在初始化系統..."
            self.status_text.color = ft.Colors.ORANGE
            self.progress_bar.visible = True
            self.progress_bar.value = 0.1
            self.status_text.update()
            self.progress_bar.update()
            
            self._add_log("🔄 開始自動點名流程...")
            
            # 創建請求
            request = AttendanceRequest(
                class_name=self.class_dropdown.value,
                date=self.date_picker.value
            )
            
            # 初始化服務
            self.status_text.value = "正在連接瀏覽器..."
            self.status_text.update()
            self.progress_bar.value = 0.3
            self.progress_bar.update()
            
            web_system = WebAttendanceSystemFactory.create()
            self._attendance_service = AutoAttendanceApplicationService(
                self._attendance_repository,
                web_system
            )
            
            self._add_log("✅ 瀏覽器連接成功！", ft.Colors.GREEN)
            self._add_log(f"📋 頁面標題: {web_system.get_page_title()}")
            
            # 執行自動點名
            self.status_text.value = "正在執行自動點名..."
            self.status_text.update()
            self.progress_bar.value = 0.6
            self.progress_bar.update()
            
            # 執行自動點名，傳遞進度回調
            result = self._attendance_service.execute_auto_attendance(
                request,
                progress_callback=self._progress_callback
            )
            
            # 顯示結果
            self.progress_bar.value = 1.0
            self.progress_bar.update()
            
            if result.success:
                self.status_text.value = "點名完成！"
                self.status_text.color = ft.Colors.GREEN
                self._add_log("✅ 自動點名完成！", ft.Colors.GREEN)
                self.result_text.value = result.get_summary()
                self.result_container.visible = True
                self.result_container.update()
            else:
                self.status_text.value = "點名失敗"
                self.status_text.color = ft.Colors.RED
                self._add_log(f"❌ 點名失敗: {result.message}", ft.Colors.RED)
                
                for error in result.errors:
                    self._add_log(f"  • {error}", ft.Colors.RED)
            
            self.status_text.update()
            
        except Exception as ex:
            self._show_error(f"未預期錯誤: {str(ex)}")
        finally:
            # 重新啟用開始按鈕
            self.start_button.disabled = False
            self.start_button.update()
    
    def _progress_callback(self, action: str, record, current: int, total: int):
        """進度回調函數 - 在 UI 中顯示學生處理狀態"""
        student_name = record.student.name.value
        student_id = record.student.student_id.value
        status_desc = record.status.description or "正常出席"
        
        # 更新進度條
        progress_value = current / total * 0.4 + 0.6  # 從 0.6 到 1.0
        self.progress_bar.value = progress_value
        self.progress_bar.update()
        
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
        self.status_text.value = message
        self.status_text.color = ft.Colors.RED
        self.progress_bar.visible = False
        self.status_text.update()
        self.progress_bar.update()
        
        self._add_log(f"❌ {message}", ft.Colors.RED)
        
        # 重新啟用開始按鈕
        self.start_button.disabled = False
        self.start_button.update()


def create_ui_app() -> Callable[[ft.Page], None]:
    """創建UI應用程式"""
    def main(page: ft.Page):
        controller = AttendanceUIController()
        controller.create_ui(page)
    
    return main