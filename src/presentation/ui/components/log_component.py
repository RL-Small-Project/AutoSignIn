from typing import Callable, Optional
import flet as ft
from .base_component import BaseComponent
from .title_component import UIConstants


class LogComponent(BaseComponent):
    """日誌區塊組件"""
    
    def __init__(self):
        super().__init__()
        self.log_container = None
    
    def create(self) -> ft.Container:
        """創建日誌區塊"""
        # 日誌容器
        self.log_container = ft.ListView(
            height=300,
            spacing=3,
            padding=ft.Padding(10, 10, 10, 10),
            expand=True,
            auto_scroll=False,
        )
        
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.LIST_ALT, color=UIConstants.INFO_COLOR),
                    ft.Text("執行日誌", size=18, weight=ft.FontWeight.BOLD),
                    ft.Container(expand=True),  # 填充空間
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
    
    def add_log(self, message: str, color: str = None):
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
        try:
            self.log_container.update()
        except:
            pass  # 忽略未添加到頁面的錯誤
        
        # 使用異步方式滾動到底部
        try:
            if len(self.log_container.controls) > 0:
                self.log_container.scroll_to(
                    offset=-1,  # 滾動到最底部
                    duration=100
                )
        except:
            pass  # 忽略滾動錯誤
    
    def clear_log(self):
        """清空日誌"""
        self.log_container.controls.clear()
        try:
            self.log_container.update()
        except:
            pass  # 忽略未添加到頁面的錯誤
    
    def _clear_log_click(self, e):
        """按鈕觸發的清空日誌"""
        self.clear_log()
    
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