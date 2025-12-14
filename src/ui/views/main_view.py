import os
from datetime import datetime

import flet as ft
import requests

from src.services.attendance import AttendanceService
from src.services.check_web import CheckWebService
from src.services.read_excel import ReadExcelService
from src.ui.components.base_button import BaseButton


def MainView(page: ft.Page):
    # init services
    check_web_service = CheckWebService()
    read_excel_service = ReadExcelService(os.getenv("DATAPATH"))

    grades = ["1", "2", "3", "4"]
    groups = ["A", "B", "C", "D"]

    # init events
    def get_options(method: list[str]):
        options = []
        for option in method:
            options.append(
                ft.DropdownOption(
                    key=option,
                    content=ft.Text(value=option, color=ft.Colors.ON_SURFACE),
                )
            )
        return options

    def add_log(message: str, color: str = None):
        """新增日誌訊息"""
        print("Log:", message)
        if color is None:
            color = ft.Colors.BLACK

        log_item = ft.Container(
            content=ft.Text(message, size=14, color=color),
            padding=ft.Padding(5, 2, 5, 2),
        )
        log_container.controls.append(log_item)
        log_container.scroll_to(offset=-1, duration=300)
        log_container.update()

    def ClearLogClick(e):
        """清空日誌"""
        log_container.controls.clear()
        log_container.update()

    def ScrollToTop(e):
        """滾動到頂部"""
        log_container.scroll_to(offset=0, duration=300)
        log_container.update()

    def ScrollToBottom(e):
        """滾動到底部"""
        log_container.scroll_to(offset=-1, duration=300)
        log_container.update()

    def choose_date(e):
        """選擇日期"""
        print("選擇的日期:", e.control.value.strftime("%Y-%m-%d"))
        date_picker.value = e.control.value.strftime("%Y-%m-%d")
        date_picker.update()

    def start_attendance(e):
        """開始點名"""
        try:
            ws_endpoint = check_web_service.get_browser_ws_endpoint()
            attendance_service = AttendanceService(ws_endpoint, log_callback=add_log)
            if grade_dd.value and class_dd.value:
                df = read_excel_service.read_data(
                    f"{grade_dd.value}{class_dd.value}.xlsx"
                )
                y, m, d = map(int, date_picker.value.split("-"))
                add_log(
                    f"{grade_dd.value}年{class_dd.value}班開始進行點名，日期：{date_picker.value}",
                    color=ft.Colors.BLUE,
                )
                attendance_service.attend(df, datetime(y, m, d))
                start_button.disabled = True
                start_button.text = "點名中..."
                start_button.update()
                add_log("自動點名完成！", color=ft.Colors.GREEN)
            else:
                add_log("請選擇年級與班級！", color=ft.Colors.RED)
        except requests.exceptions.ConnectionError:
            add_log(
                "無法連接到瀏覽器，請確認瀏覽器是否已開啟遠端模式！",
                color=ft.Colors.RED,
            )
        except FileNotFoundError:
            add_log(
                f"找不到{grade_dd.value}年{class_dd.value}班的點名紀錄檔，請確認檔案是否存在！",
                color=ft.Colors.RED,
            )
        except ValueError:
            add_log("請確認日期是否正確！", color=ft.Colors.RED)
        except IndexError as ie:
            add_log(f"{ie.args[0]}", color=ft.Colors.RED)
        except Exception as ex:
            add_log(f"發生錯誤：{type(ex)}", color=ft.Colors.RED)
        start_button.disabled = False
        start_button.text = "開始點名"
        start_button.update()

    # components
    log_container = ft.ListView(
        height=300,
        spacing=3,
        padding=ft.Padding(10, 10, 10, 10),
        expand=True,
        auto_scroll=False,
    )

    grade_dd = ft.Dropdown(
        label="年級",
        options=get_options(grades),
        border_color=ft.Colors.OUTLINE,
    )
    class_dd = ft.Dropdown(
        label="班級",
        options=get_options(groups),
        border_color=ft.Colors.OUTLINE,
    )
    date_picker = ft.TextField(
        label="點名日期",
        value=datetime.today().strftime("%Y/%m/%d"),
        read_only=True,
        on_click=lambda e: page.open(
            ft.DatePicker(
                first_date=datetime(year=2000, month=10, day=1),
                last_date=datetime.today(),
                on_change=choose_date,
            ),
        ),
        border_color=ft.Colors.OUTLINE,
    )
    start_button = BaseButton(text="開始點名", on_click=lambda e: start_attendance(e))

    # Layout
    view_content = ft.Column(
        controls=[
            ft.Column(
                [
                    ft.Container(
                        ft.Text("AutoSignIn", size=30, color=ft.Colors.ON_PRIMARY),
                        alignment=ft.alignment.center,
                        bgcolor=ft.Colors.PRIMARY,
                        border_radius=10,
                    )
                ],
            ),
            ft.Divider(),
            ft.Row(
                [
                    ft.Icon(ft.Icons.SETTINGS, color=ft.Colors.ON_SURFACE),
                    ft.Text("基本設定", size=18, weight=ft.FontWeight.BOLD),
                ]
            ),
            ft.Row(
                [grade_dd, class_dd, start_button],
                wrap=True,  # 允許換行
                spacing=20,
            ),
            ft.Column(
                [
                    date_picker,
                    BaseButton(
                        text="測試按鈕",
                        on_click=lambda e: add_log(
                            "這是一條測試日誌", color=ft.Colors.GREEN
                        ),
                    ),
                ]
            ),
            ft.Divider(),
            ft.Container(
                content=ft.Column(
                    controls=[
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
                            content=log_container,
                            bgcolor=ft.Colors.SURFACE,
                            border_radius=10,
                        ),
                    ]
                )
            ),
        ],
        scroll=ft.ScrollMode.AUTO,
    )

    return view_content
