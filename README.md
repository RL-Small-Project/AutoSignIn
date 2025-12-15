## 🧭 簡介

這是一個專為中國科技大學（CUTe）設計的自動化點名工具。透過讀取 Excel 點名表，自動操作瀏覽器完成校務系統的點名作業，大幅節省人工點選的時間。

## ✨ 特色功能

* **自動化點名**：連接已開啟的瀏覽器，自動填寫校務系統的點名欄位。
* **Excel 整合**：直接讀取標準格式的 Excel 點名單，支援批次處理。
* **即時日誌**：GUI 介面提供詳細的執行日誌，即時顯示每位學生的點名狀態。
* **防呆機制**：
    * 自動偵測「休學」學生並跳過。
    * 自動偵測「公假」狀態（若系統已鎖定欄位）。
    * 自動檢查學號是否匹配。

## 🛠️ 技術

*   **語言**: Python 3.10+
*   **GUI 框架**: [Flet](https://flet.dev/)
*   **瀏覽器自動化**: [Playwright](https://playwright.dev/)

## 📖 如何使用
1. 從 [Releases](https://github.com/RL-Small-Project/AutoSignIn/releases) 下載最新發佈的執行檔。

2. 使用以下命令打開遠端瀏覽器
    > 請確認系統已安裝 Edge 或 Chrome 瀏覽器。

    Windows:
    - Chrome
        ```bash
        cd C:\Program Files\Google\Chrome\Application\
        .\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\Users\%USERNAME%\AppData\Local\Google\Chrome\User Data"
        ```
    - Edge
        ```bash
        cd C:\Program Files (x86)\Microsoft\Edge\Application\
        .\msedge.exe --remote-debugging-port=9222 --user-data-dir="C:\edge_profile"
        ```

    Linux (Dabian/Ubuntu):
    - Chrome
        ```bash
        google-chrome   --remote-debugging-port=9222   --user-data-dir=/tmp/edge-profile
        ```
    - Edge
        ```bash
        microsoft-edge   --remote-debugging-port=9222   --user-data-dir=/tmp/edge-profile
        ```

3. 把點名紀錄檔依照 [內容格式](data/Excel_Template_Guide.md) 並存放在 Data 目錄中。
    ```
    ./data/
    ├── A.xlsx
    └── B.xlsx
    ```

## 💡 回報問題 & 貢獻

- 問題回報：您可以到 [Issues](https://github.com/RL-Small-Project/AutoSignIn/issues) 進行回報，並說明問題點與執行時的錯誤代碼。

- 成為貢獻者：請 [Fork](https://github.com/RL-Small-Project/AutoSignIn/fork) 此倉庫，建立新分支進行修改，然後提交 [Pull Request](https://github.com/RL-Small-Project/AutoSignIn/pulls)。

## 🏗️ 開發環境建置
注意：請使用 DevContainer 進行開發。

1. 同步 UV 套件
    ```bash
    uv sync
    ```

2. 安裝必要套件
    ```bash
    sudo apt-get update && sudo apt-get install -y libgtk-3-0 libgstreamer1.0-0 libgstreamer-plugins-base1.0-0 libegl1 libgl1 fonts-wqy-microhei fonts-noto-cjk
    ```

    ```bash
    sudo apt-get install -y clang cmake ninja-build pkg-config libgtk-3-dev liblzma-dev
    ```

3. 安裝瀏覽器
    ```bash
    playwright install
    ```

4. 建置 .env
    > 打包應用時必須把 `DEV_MODE` 設定為 `0`。
    
    ```
    ## Web browser URL
    URL = "localhost:9222"
    ## Data folder name
    DATA_FOLDER_NAME = "data"
    ## Develop mode
    DEV_MODE = 0
    ```

執行完上述步驟及可進行開發。