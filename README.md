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

在本機上打開 Edge 或 Chrome 瀏覽器的遠端程式

Windows PowerShell:
```bash
cd 'C:\Program Files (x86)\Microsoft\Edge\Application\'
.\msedge.exe --remote-debugging-port=9222 --user-data-dir="C:\edge_profile"
```

```bash
cd "C:\Program Files (x86)\Google\Chrome\Application\"
.\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrome_profile"
```

Linux:
```bash
cd /usr/bin
google-chrome --remote-debugging-port=9222 --user-data-dir="/home/$USER/chrome_profile"
```

```bash
cd /usr/bin
microsoft-edge --remote-debugging-port=9222 --user-data-dir="/home/$USER/edge_profile"
```

執行程式
```bash
uv run main.py
```