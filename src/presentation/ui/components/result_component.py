import flet as ft
from .base_component import BaseComponent
from .title_component import UIConstants


class ResultComponent(BaseComponent):
    """結果顯示區塊組件"""
    
    def __init__(self):
        super().__init__()
        self.result_text = None
    
    def create(self) -> ft.Container:
        """創建結果顯示區塊"""
        # 結果顯示
        self.result_text = ft.Text(
            "",
            size=16,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.GREEN_800,
            text_align=ft.TextAlign.CENTER
        )
        
        container = ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.ASSESSMENT, color=UIConstants.SUCCESS_COLOR, size=24),
                self.result_text,
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
            bgcolor=ft.Colors.GREEN_50,
            padding=ft.Padding(20, 15, 20, 15),
            border_radius=10,
            visible=False
        )
        
        return container
    
    def show_result(self, message: str):
        """顯示結果"""
        if self.result_text and self._container:
            self.result_text.value = message
            self._container.visible = True
            try:
                self.result_text.update()
                self._container.update()
            except:
                pass  # 忽略未添加到頁面的錯誤
    
    def hide_result(self):
        """隱藏結果"""
        if self._container:
            self._container.visible = False
            try:
                self._container.update()
            except:
                pass  # 忽略未添加到頁面的錯誤
    
    def clear_result(self):
        """清空結果"""
        if self.result_text:
            self.result_text.value = ""
            try:
                self.result_text.update()
            except:
                pass  # 忽略未添加到頁面的錯誤
        self.hide_result()