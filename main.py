import dotenv
import flet as ft

from src.theme.config import get_dark_theme
from src.ui.views.main_view import MainView


def main(page: ft.Page):
    # 1. 基礎設定
    page.title = "自動點名系統-中國科技大學(專用)"
    page.theme = get_dark_theme()
    page.theme_mode = ft.ThemeMode.DARK
    page.window.width = 400
    page.window.height = 700

    dotenv.load_dotenv()

    # 2. 載入 View
    # 這裡示範最簡單的直接掛載，若專案較大建議使用 page.on_route_change
    main_content = MainView(page)

    # 3. 將內容加入頁面
    page.add(main_content)
    page.update()


if __name__ == "__main__":
    ft.app(target=main)
