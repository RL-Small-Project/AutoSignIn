from datetime import datetime

import pandas as pd
import requests
from application.use_case.count_class_students import CountClassStudents
from application.use_case.show_completions import ShowCompletions
from application.use_case.show_title import ShowTitle
from double_check import DoubleCheck
from errors.student_id_mismatch import StudentIDMismatchError
from playwright.sync_api import sync_playwright

double_check_use_case = DoubleCheck()
show_completions_use_case = ShowCompletions()
count_class_students_use_case = CountClassStudents()
show_title_use_case = ShowTitle()

url = "http://host.docker.internal:9222/json/version"
headers = {"Host": "localhost"}  # 使用 localhost 的標頭

try:
    resp = requests.get(url, headers=headers, timeout=5)
    token = resp.json()["webSocketDebuggerUrl"].split("/")[-1]
    print("✅ 連線成功！")

    ws_url = f"ws://host.docker.internal:9222/devtools/browser/{token}"

    class_name = input("請輸入班級(A/B):")
    y, m, d = map(int, input("輸入日期 (格式: YYYY-MM-DD): ").split("-"))
    target_date = datetime(y, m, d)
    df = pd.read_excel(f"data/{class_name}.xlsx", sheet_name="點名單")
    filtered_df = df[df["姓名"].notna()]
    all_students = len(filtered_df["姓名"].tolist())

    with sync_playwright() as p:
        # 連接到現有瀏覽器（要先啟動瀏覽器有 debugging port）
        browser = p.chromium.connect_over_cdp(ws_url)
        context = browser.contexts[0]  # 取得現有 context
        page = context.pages[0]  # 取得現有分頁
        show_title_use_case.execute(page.title())
        main_frame = page.frame(name="main")

        skip_class = 0  # 曠課人數

        for index, row in filtered_df.iterrows():
            name = row["姓名"]
            student_id = int(row["學號"])
            status = row[target_date]

            if type(status) is str:
                print(f"{name}: {status}")

            system_student_id = int(
                main_frame.locator(f"#dgmuster_lblstdNO_{index}").inner_text()
            )

            if student_id != system_student_id:
                raise StudentIDMismatchError(
                    f"學號不相符：Excel={student_id} 網頁={system_student_id}，請確認點名表人數或順序是否正確！"
                )

            radios = main_frame.locator(
                f"input[type='radio'][name*='dgmuster:_ctl{index + 2}:rbl']"
            )

            if radios.nth(0).is_disabled():
                print(f"{name}: 公假(跳過點名)")
                skip_class += 1
                continue

            if "曠課" in str(status):
                radios.nth(2).check()  # 第1節
                radios.nth(5).check()  # 第2節
                skip_class += 1
            if "遲到" in str(status):
                radios.nth(1).check()  # 第1節
            if "缺節" in str(status):
                radios.nth(2).check()  # 第1節
            if "缺遲" in str(status):
                radios.nth(2).check()  # 第1節
                radios.nth(4).check()  # 第2節

        show_completions_use_case.execute()
    count_class_students_use_case.execute(all_students, skip_class)

except requests.exceptions.ConnectionError:
    print("❌ 無法連接到瀏覽器，請確認瀏覽器已啟動並開啟遠端模式。")
except requests.exceptions.Timeout:
    print("⚠️ 連線逾時，請檢查網路或 debug port 設定")
except requests.exceptions.HTTPError as e:
    print(f"⚠️ HTTP 錯誤：{e.response.status_code}")
except Exception as e:
    print(f"⚠️ 未預期錯誤：{type(e).__name__} - {e}")

# cd 'C:\Program Files (x86)\Microsoft\Edge\Application\'
# .\msedge.exe --remote-debugging-port=9222 --user-data-dir="C:\edge_profile"
# 打開點名頁面即可直接抓取點名表的 (Excel 檔案) 內容
# http://localhost:9222/json/version
# "ws://host.docker.internal:9222/devtools/browser/<token>"
