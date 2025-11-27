from datetime import datetime
import flet as ft
from .base_component import BaseComponent
from .title_component import UIConstants


class InputComponent(BaseComponent):
    """輸入區塊組件"""
    
    def __init__(self):
        super().__init__()
        self.class_dropdown = None
        self.date_picker = None
    
    def create(self) -> ft.Container:
        """創建輸入區塊"""
        # 初始化輸入元件
        self.class_dropdown = ft.Dropdown(
            label="選擇班級",
            hint_text="請選擇班級",
            options=UIConstants.CLASS_OPTIONS,
            border_color=UIConstants.SECONDARY_COLOR,
            expand=True
        )
        
        self.date_picker = ft.TextField(
            label="日期 (YYYY-MM-DD)",
            hint_text="例: 2025-11-11",
            value=datetime.now().strftime("%Y-%m-%d"),
            border_color=UIConstants.SECONDARY_COLOR,
            expand=True,
        )
        
        return ft.Container(
            content=ft.Column([
                ft.Text("📝 基本設定", size=18, weight=ft.FontWeight.BOLD),
                ft.Row([
                    ft.Icon(ft.Icons.SCHOOL, color=UIConstants.INFO_COLOR),
                    ft.Text("班級：", size=16),
                    self.class_dropdown,
                ], alignment=ft.MainAxisAlignment.START),
                ft.Row([
                    ft.Icon(ft.Icons.DATE_RANGE, color=UIConstants.INFO_COLOR),
                    ft.Text("日期：", size=16),
                    self.date_picker,
                ], alignment=ft.MainAxisAlignment.START),
            ], spacing=15),
            bgcolor=ft.Colors.WHITE,
            padding=ft.Padding(20, 15, 20, 15),
            border_radius=10,
            border=ft.border.all(1, ft.Colors.BLUE_200),
            margin=ft.Margin(0, 0, 0, 20),
            height=200
        )
    
    def get_class_value(self) -> str:
        """獲取選中的班級"""
        return self.class_dropdown.value if self.class_dropdown else None
    
    def get_date_value(self) -> str:
        """獲取輸入的日期"""
        return self.date_picker.value if self.date_picker else None