import os
import pandas as pd
from typing import List, Optional
from datetime import datetime

from ...domain.repositories.attendance_repository import AttendanceRepository
from ...domain.entities.class_ import ClassName
from ...domain.entities.student import Student, StudentId, StudentName
from ...domain.value_objects.attendance_record import AttendanceRecord, AttendanceDate
from ...domain.value_objects.attendance_status import AttendanceStatus
from ...domain.exceptions import InvalidAttendanceDataError


class ExcelAttendanceRepository(AttendanceRepository):
    """Excel檔案出勤記錄倉儲實作"""
    
    def __init__(self, data_folder: str = "data"):
        self._data_folder = data_folder
    
    def find_by_class_and_date(self, class_name: ClassName, 
                              date: AttendanceDate) -> List[AttendanceRecord]:
        """根據班級和日期查找出勤記錄"""
        return self.load_from_excel(class_name, date)
    
    def save_records(self, records: List[AttendanceRecord]) -> None:
        """批量保存出勤記錄（目前不實作，因為主要是讀取Excel）"""
        # 在實際應用中，這裡可能會保存到資料庫或更新Excel檔案
        pass
    
    def load_from_excel(self, class_name: ClassName, 
                       date: AttendanceDate) -> List[AttendanceRecord]:
        """從Excel檔案載入出勤記錄"""
        try:
            excel_path = os.path.join(self._data_folder, f"{class_name.value}.xlsx")
            
            if not os.path.exists(excel_path):
                raise InvalidAttendanceDataError(f"找不到Excel檔案: {excel_path}")
            
            # 讀取Excel檔案
            df = pd.read_excel(excel_path, sheet_name="點名單")
            
            # 過濾掉姓名為空的行
            filtered_df = df[df["姓名"].notna()]
            
            if filtered_df.empty:
                raise InvalidAttendanceDataError("Excel檔案中沒有有效的學生資料")
            
            records = []
            date_column = date.to_string()  # YYYY-MM-DD 格式
            
            # 檢查日期欄位是否存在
            if date_column not in filtered_df.columns:
                # 嘗試尋找相似的日期格式
                date_obj = date.value
                possible_formats = [
                    date_obj.strftime("%Y-%m-%d"),
                    date_obj.strftime("%Y/%m/%d"),
                    date_obj.strftime("%m/%d/%Y"),
                    date_obj,  # datetime 物件本身
                ]
                
                found_column = None
                for col in filtered_df.columns:
                    if col in possible_formats or col == date_obj:
                        found_column = col
                        break
                
                if found_column:
                    date_column = found_column
                else:
                    raise InvalidAttendanceDataError(
                        f"在Excel檔案中找不到日期欄位: {date.to_string()}"
                    )
            
            for _, row in filtered_df.iterrows():
                try:
                    # 創建學生實體
                    student = Student(
                        StudentId(int(row["學號"])),
                        StudentName(str(row["姓名"]))
                    )
                    
                    # 取得出勤狀態
                    status_value = row.get(date_column, "")
                    if pd.isna(status_value):
                        status_value = ""
                    
                    status = AttendanceStatus.from_excel_value(str(status_value))
                    
                    # 創建出勤記錄
                    record = AttendanceRecord(
                        student=student,
                        date=date,
                        status=status
                    )
                    
                    records.append(record)
                    
                except Exception as e:
                    raise InvalidAttendanceDataError(
                        f"處理學生資料時發生錯誤 (行 {_}): {str(e)}"
                    )
            
            return records
            
        except pd.errors.EmptyDataError:
            raise InvalidAttendanceDataError("Excel檔案為空")
        except pd.errors.ParserError:
            raise InvalidAttendanceDataError("無法解析Excel檔案")
        except FileNotFoundError:
            raise InvalidAttendanceDataError(f"找不到檔案: {excel_path}")
        except Exception as e:
            raise InvalidAttendanceDataError(f"讀取Excel檔案時發生錯誤: {str(e)}")