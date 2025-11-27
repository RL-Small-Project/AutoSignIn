import sys
import flet as ft

from src.presentation.ui.attendance_ui_controller import create_ui_app


def main():
    print("📢 自動點名系統")
    print("============================")
    try:
        ui_app = create_ui_app()
        # 桌面應用程式模式
        ft.app(
            target=ui_app,
            view=ft.AppView.FLET_APP_WEB,  # 使用原生應用程式視窗
            assets_dir="assets",  # 資源目錄
        )
    except Exception as e:
        print(f"❌ 啟動UI失敗: {str(e)}")
        input("按 Enter 鍵退出...")


if __name__ == "__main__":
    main()