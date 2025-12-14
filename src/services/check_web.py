import requests


class CheckWebService:
    def __init__(self):
        self.url = "http://localhost:9222/json/version"
        self.headers = {"Host": "localhost"}

    def get_browser_ws_endpoint(self) -> str:
        try:
            response = requests.get(self.url, headers=self.headers, timeout=5)
            token = response.json()["webSocketDebuggerUrl"].split("/")[-1]
            return f"ws://localhost:9222/devtools/browser/{token}"
        except Exception as e:
            raise e
