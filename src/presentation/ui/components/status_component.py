from typing import Callable, Optional
import flet as ft
from .base_component import BaseComponent
from .title_component import UIConstants


class StatusComponent(BaseComponent):
    """狀態顯示區塊組件"""
    
    def __init__(self, on_start_click: Optional[Callable] = None):
        super().__init__()
        self.status_text = None
        self.progress_bar = None
        self.start_button = None
        self._on_start_click = on_start_click
    
    def create(self) -> ft.Container:
        """創建狀態顯示區塊"""
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
            color=UIConstants.SUCCESS_COLOR,
            bgcolor=ft.Colors.GREY_300,
            border_radius=10,
        )
        
        # 開始按鈕
        self.start_button = ft.ElevatedButton(
            text="開始自動點名",
            icon=ft.Icons.PLAY_ARROW,
            on_click=self._on_start_click,
            width=200,
            height=50,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.GREEN_400,
                color=ft.Colors.WHITE,
                text_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD)
            )
        )
        
        return ft.Container(
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
    
    def set_status(self, message: str, color: str = None):
        """設置狀態文字"""
        if self.status_text:
            self.status_text.value = message
            if color:
                self.status_text.color = color
            try:
                self.status_text.update()
            except:
                pass  # 忽略未添加到頁面的錯誤
    
    def set_progress(self, value: float, visible: bool = True):
        """設置進度條"""
        if self.progress_bar:
            self.progress_bar.value = value
            self.progress_bar.visible = visible
            try:
                self.progress_bar.update()
            except:
                pass  # 忽略未添加到頁面的錯誤
    
    def set_button_enabled(self, enabled: bool):
        """設置按鈕啟用狀態"""
        if self.start_button:
            self.start_button.disabled = not enabled
            try:
                self.start_button.update()
            except:
                pass  # 忽略未添加到頁面的錯誤