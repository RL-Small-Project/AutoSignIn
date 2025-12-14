import flet as ft


class BaseButton(ft.ElevatedButton):
    def __init__(self, text: str, on_click=None):
        def on_hover_effect(e: ft.HoverEvent):
            e.control.bgcolor = (
                ft.Colors.BLUE_300 if e.data == "true" else ft.Colors.PRIMARY
            )
            e.control.update()

        super().__init__(
            text=text,
            bgcolor=ft.Colors.PRIMARY,
            color=ft.Colors.ON_PRIMARY,
            on_click=on_click,
            on_hover=lambda e: on_hover_effect(e),
        )
