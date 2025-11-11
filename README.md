## 事前準備
1. Python 3.10 版 + UV 套件管理工具
2. Edge 或 Chrome 瀏覽器
3. 點名表 excel

## 點名紀錄表單內容範例
| 姓名 | 日期(YYYY/MM/DD) |
|------|-----------------|
| 王小明 | 遲到 |
| 王大明 | 曠課 |
| 李大夫 |  |
| 林君君 | 缺遲 |

點名紀錄單的內容可以參考[Excel_Template_Guide.md](data/Excel_Template_Guide.md)

## 如何使用

在專案目錄底下執行環境建置
```bash
uv sync
```

將點名紀錄表單放到 data 目錄底下
```
./data/
├── A.xlsx
└── B.xlsx
```

打開瀏覽器遠端程式 (參考下方遠端瀏覽器設定)，然後執行程式。
```bash
uv run main.py
```

**補充說明：**
- 程式會自動在 `http://localhost:8080` 啟動 Web UI
- 請在自動化瀏覽器中打開該網址進行操作

### 🌐 遠端瀏覽器設定

在本機上打開 Edge 或 Chrome 瀏覽器的遠端程式

Windows PowerShell:
```bash
cd 'C:\Program Files (x86)\Microsoft\Edge\Application\'
.\msedge.exe --remote-debugging-port=9222 --user-data-dir="C:\edge_profile"
```

```bash
cd 'C:\Program Files\Google\Chrome\Application\'
.\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\Users\%USERNAME%\AppData\Local\Google\Chrome\User Data"
```

### 💻 介面

1. 執行程式後選擇 `1. 圖形化介面` 或 `2. 命令列介面`。

2. 輸入:
    - 授課班級
    - 點名日期

3. 系統會在瀏覽器中自動點名。