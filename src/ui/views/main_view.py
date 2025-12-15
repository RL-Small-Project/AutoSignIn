import os
from datetime import datetime

import flet as ft
import requests

from src.services.attendance import AttendanceService
from src.services.check_web import CheckWebService
from src.services.read_excel import ReadExcelService
from src.ui.components.base_button import BaseButton
from src.ui.components.log_container import LogContainer


def MainView(page: ft.Page):
    # init services
    check_web_service = CheckWebService()
    read_excel_service = ReadExcelService(os.getenv("DATA_FOLDER_NAME"))

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
        log_listview.controls.append(log_item)
        log_listview.scroll_to(offset=-1, duration=300)
        log_listview.update()

    def choose_date(e):
        """選擇日期"""
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
            else:
                add_log("請選擇年級與班級！", color=ft.Colors.RED)
        except requests.exceptions.ConnectionError:
            add_log(
                "無法連接到瀏覽器，請確認瀏覽器是否已開啟遠端模式！",
                color=ft.Colors.RED,
            )
        except FileNotFoundError:
            add_log(
                f"在 {read_excel_service.data_path} 中找不到 {grade_dd.value}年{class_dd.value}班 的點名紀錄檔，請確認檔案是否存在！",
                color=ft.Colors.RED,
            )
        except ValueError:
            add_log("請確認日期是否正確！", color=ft.Colors.RED)
        except Exception as ex:
            add_log(f"發生錯誤：{type(ex)}", color=ft.Colors.RED)
        start_button.disabled = False
        start_button.text = "開始點名"
        start_button.update()

    # components
    log_listview = ft.ListView(
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
            ft.Column([date_picker]),
            ft.Divider(),
            LogContainer(log_listview),
        ],
        scroll=ft.ScrollMode.AUTO,
    )

    return view_content
