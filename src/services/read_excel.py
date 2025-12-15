import os
import sys


class ReadExcelService:
    def __init__(self, data_folder: str):
        current_path = os.path.dirname(os.path.abspath(sys.argv[0]))
        print("Current Path:", current_path)
        self.data_path = os.path.join(current_path, data_folder)

    def read_data(self, filename: str):
        import pandas as pd

        file_path = f"{self.data_path}/{filename}"
        print("Reading Excel File:", file_path)
        try:
            df = pd.read_excel(file_path)
            return df
        except Exception as e:
            raise e
