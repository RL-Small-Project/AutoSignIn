from datetime import datetime

import pandas as pd
import requests
from playwright.sync_api import sync_playwright

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
        print(page.title())
        main_frame = page.frame(name="main")
        # radios = main_frame.locator("input[type='radio'][name*='dgmuster:_ctl2:rbl']")
        # print(radios)
        # radios.nth(0).check()
        # radios.nth(5).check()
        # main_frame.check("#dgmuster_rbl3_0_1_0")

        skip_class = 0  # 曠課人數

        for index, row in filtered_df.iterrows():
            index += 2
            name = row["姓名"]
            status = row[target_date]
            print(f"{name}: {status}")
            radios = main_frame.locator(
                f"input[type='radio'][name*='dgmuster:_ctl{index}:rbl']"
            )

            if "曠課" in str(status):
                print("22")
                radios.nth(2).check()  # 第1節
                radios.nth(5).check()  # 第2節
                skip_class += 1
            if "遲到" in str(status):
                print("10")
                radios.nth(1).check()  # 第1節
            if "缺節" in str(status):
                print("20")
                radios.nth(2).check()  # 第1節
            if "缺遲" in str(status):
                print("21")
                radios.nth(2).check()  # 第1節
                radios.nth(4).check()  # 第2節

        print("✅ 自動點名完成！")
    # print(page.content())
    print("應到人數:", all_students)
    print("實到人數:", all_students - skip_class)

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
