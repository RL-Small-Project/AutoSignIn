import flet as ft
from .base_component import BaseComponent


class UIConstants:
    """UI界面常數"""
    WINDOW_WIDTH = 650
    WINDOW_HEIGHT = 750
    APP_TITLE = "中國科技大學-自動化點名系統"
    DESIGNER_CREDIT = "Design by Raylon"
    
    # 顏色配置
    PRIMARY_COLOR = ft.Colors.BLUE_800
    SECONDARY_COLOR = ft.Colors.BLUE_400
    SUCCESS_COLOR = ft.Colors.GREEN
    ERROR_COLOR = ft.Colors.RED
    WARNING_COLOR = ft.Colors.ORANGE
    INFO_COLOR = ft.Colors.BLUE
    
    # 班級選項
    CLASS_OPTIONS = [
        ft.dropdown.Option("A", "A班"),
        ft.dropdown.Option("B", "B班"),
    ]


class TitleComponent(BaseComponent):
    """標題區塊組件"""
    
    def create(self) -> ft.Container:
        """創建標題區塊"""
        return ft.Container(
            content=ft.Column([
                ft.Text(
                    f"📢 {UIConstants.APP_TITLE}",
                    size=32,
                    weight=ft.FontWeight.BOLD,
                    color=UIConstants.PRIMARY_COLOR,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Text(
                    UIConstants.DESIGNER_CREDIT,
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