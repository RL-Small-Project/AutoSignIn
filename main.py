import sys
import flet as ft

from src.presentation.cli.attendance_cli_controller import AttendanceCliController
from src.presentation.ui.attendance_ui_controller import create_ui_app


def main():
    print("📢 自動點名系統")
    print("============================")
    print("1. 圖形化介面 (推薦)")
    print("2. 命令列介面") 
    print("3. 退出")
    
    while True:
        choice = input("\n請選擇執行模式 (1/2/3): ").strip()
        
        if choice == "1":
            print("🌐 正在啟動圖形化介面...")
            start_ui()
            break
        elif choice == "2":
            print("💻 正在啟動命令列介面...")
            start_cli()
            break
        elif choice == "3":
            print("👋 再見！")
            sys.exit(0)
        else:
            print("❌ 無效選擇，請輸入 1、2 或 3")


def start_ui():
    """啟動圖形化介面"""
    try:
        import os
        port = int(os.environ.get("FLET_PORT", 8080))
        print(f"🔗 請在瀏覽器中打開: http://localhost:{port}")
        
        ui_app = create_ui_app()
        ft.app(target=ui_app, port=port, view=ft.AppView.WEB_BROWSER)
    except Exception as e:
        print(f"❌ 啟動UI失敗: {str(e)}")


def start_cli():
    """啟動命令列介面"""
    try:
        cli_controller = AttendanceCliController()
        cli_controller.run()
    except Exception as e:
        print(f"❌ 啟動CLI失敗: {str(e)}")


if __name__ == "__main__":
    main()