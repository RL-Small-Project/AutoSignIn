import flet as ft


class LogContainer(ft.Container):
    def __init__(self, log_listview: ft.ListView):
        def ClearLogClick(e):
            """清空日誌"""
            log_listview.controls.clear()
            log_listview.update()

        def ScrollToTop(e):
            """滾動到頂部"""
            log_listview.scroll_to(offset=0, duration=300)
            log_listview.update()

        def ScrollToBottom(e):
            """滾動到底部"""
            log_listview.scroll_to(offset=-1, duration=300)
            log_listview.update()

        super().__init__(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.LIST_ALT, color=ft.Colors.ON_SURFACE),
                            ft.Text("執行日誌", size=18, weight=ft.FontWeight.BOLD),
                            ft.Container(expand=True),
                            ft.IconButton(
                                icon=ft.Icons.KEYBOARD_ARROW_UP,
                                tooltip="滾動到頂部",
                                on_click=ScrollToTop,
                                icon_size=20,
                            ),
                            ft.IconButton(
                                icon=ft.Icons.KEYBOARD_ARROW_DOWN,
                                tooltip="滾動到底部",
                                on_click=ScrollToBottom,
                                icon_size=20,
                            ),
                            ft.IconButton(
                                icon=ft.Icons.CLEAR,
                                tooltip="清空日誌",
                                on_click=ClearLogClick,
                                icon_size=20,
                            ),
                        ]
                    ),
                    ft.Container(
                        content=log_listview,
                        bgcolor=ft.Colors.SURFACE,
                        border_radius=10,
                    ),
                ]
            )
        )
