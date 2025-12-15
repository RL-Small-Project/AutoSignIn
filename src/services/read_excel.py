import os


class ReadExcelService:
    def __init__(self, data_folder: str):
        root_path = os.getenv("ROOT_PATH")
        self.data_path = os.path.join(root_path, data_folder)

    def read_data(self, filename: str):
        import pandas as pd

        file_path = f"{self.data_path}/{filename}"
        try:
            df = pd.read_excel(file_path)
            return df
        except Exception as e:
            raise e
