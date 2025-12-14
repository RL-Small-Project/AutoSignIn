class ReadExcelService:
    def __init__(self, base_path: str):
        self.base_path = base_path

    def read_data(self, filename: str):
        import pandas as pd

        file_path = f"{self.base_path}/{filename}"
        try:
            df = pd.read_excel(file_path)
            return df
        except Exception as e:
            raise e
