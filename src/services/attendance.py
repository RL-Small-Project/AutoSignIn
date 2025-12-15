import flet as ft
import pandas as pd
from playwright.sync_api import sync_playwright

from src.theme.config import StatusColors


class AttendanceService:
    def __init__(self, ws_endpoint: str, log_callback=None):
        self.ws_endpoint = ws_endpoint
        self.log_callback = log_callback

    def log(self, message: str, status_color: str = None):
        if self.log_callback:
            self.log_callback(str(message), color=status_color)
        else:
            print(message)

    def attend(self, df: pd.DataFrame, date: str):
        try:
            with sync_playwright() as p:
                browser = p.chromium.connect_over_cdp(self.ws_endpoint)
                context = browser.contexts[0]  # 取得現有 context
                page = context.pages[0]  # 取得現有分頁
                main_frame = page.frame(name="main")
                all_students = len(df["姓名"].tolist())
                skip_class = 0  # 曠課人數
                student_rows = main_frame.locator('tr[nowrap="nowrap"]').all()
                for std_row in student_rows:
                    std_no_elem = std_row.locator('span[id*="lblstdNO"]').first
                    note_elem = std_row.locator("td:nth-child(4)")
                    if note_elem.count() > 0:
                        if note_elem.inner_text().strip() == "休學":
                            continue
                    if std_no_elem.count() > 0:
                        system_student_id = std_no_elem.inner_text()
                        df_result = df[df["學號"] == int(system_student_id)]
                        student_id = int(df_result["學號"].iloc[0])
                        name = df_result["姓名"].iloc[0]
                        status = df_result[date].iloc[0]
                        rbl1_table = std_row.locator('table[id*="rbl1"]').first
                        rbl2_table = std_row.locator('table[id*="rbl2"]').first
                        rbl1_options = rbl1_table.locator('input[type="radio"]').all()
                        rbl2_options = rbl2_table.locator('input[type="radio"]').all()
                        if (
                            rbl1_options[0].is_disabled()
                            or rbl2_options[0].is_disabled()
                        ):
                            self.log(f"{student_id} {name}: 公假", StatusColors.LEAVE)
                            continue
                        elif "曠課" in str(status):
                            self.log(f"{student_id} {name}: 曠課", StatusColors.ABSENT)
                            rbl1_options[2].check()  # 第1節
                            rbl2_options[2].check()  # 第2節

                            skip_class += 1
                        elif "遲到" in str(status):
                            self.log(f"{student_id} {name}: 遲到", StatusColors.LATE)
                            rbl1_options[1].check()  # 第1節
                        elif "缺節" in str(status):
                            self.log(f"{student_id} {name}: 缺節", StatusColors.LATE)
                            rbl1_options[2].check()  # 第1節
                        elif "缺遲" in str(status):
                            self.log(f"{student_id} {name}: 缺遲", StatusColors.LATE)
                            rbl1_options[2].check()  # 第1節
                            rbl2_options[1].check()  # 第2節
                        else:
                            self.log(f"{student_id} {name}: 出席", StatusColors.PRESENT)
            self.log("自動點名完成！", color=ft.Colors.GREEN)
        except IndexError:
            self.log(
                f"找不到學號為 {system_student_id} 的學生資料，請確認點名表是否正確！",
                ft.Colors.RED,
            )
        except AttributeError:
            self.log(
                "請確認點名表的日期以及遠端瀏覽器是否在中國科技大學-點名頁面！",
                ft.Colors.RED,
            )
        except Exception as e:
            raise e
