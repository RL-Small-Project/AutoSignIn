from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime
from ..entities.class_ import Class, ClassName
from ..entities.student import Student
from ..value_objects.attendance_record import AttendanceRecord, AttendanceDate


class ClassRepository(ABC):
    """班級倉儲介面"""
    
    @abstractmethod
    def find_by_name(self, name: ClassName) -> Optional[Class]:
        """根據班級名稱查找班級"""
        pass
    
    @abstractmethod
    def save(self, class_: Class) -> None:
        """保存班級"""
        pass


class AttendanceRepository(ABC):
    """出勤記錄倉儲介面"""
    
    @abstractmethod
    def find_by_class_and_date(self, class_name: ClassName, 
                              date: AttendanceDate) -> List[AttendanceRecord]:
        """根據班級和日期查找出勤記錄"""
        pass
    
    @abstractmethod
    def save_records(self, records: List[AttendanceRecord]) -> None:
        """批量保存出勤記錄"""
        pass
    
    @abstractmethod
    def load_from_excel(self, class_name: ClassName, 
                       date: AttendanceDate) -> List[AttendanceRecord]:
        """從Excel檔案載入出勤記錄"""
        pass