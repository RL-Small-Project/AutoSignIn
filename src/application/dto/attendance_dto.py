from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime


@dataclass
class AttendanceRequest:
    """點名請求DTO"""
    class_name: str
    date: str  # YYYY-MM-DD format
    
    def to_datetime(self) -> datetime:
        """轉換日期字串為datetime物件"""
        return datetime.strptime(self.date, "%Y-%m-%d")


@dataclass 
class AttendanceResult:
    """點名結果DTO"""
    success: bool
    total_students: int
    actual_attendance: int
    skipped_count: int
    errors: List[str]
    message: str
    
    def get_summary(self) -> str:
        """取得結果摘要"""
        if not self.success:
            return f"點名失敗: {self.message}"
        return f"應到人數: {self.total_students} | 實到人數: {self.actual_attendance}"


@dataclass
class StudentInfo:
    """學生資訊DTO"""
    student_id: int
    name: str
    status: str
    
    
@dataclass
class ClassInfo:
    """班級資訊DTO"""
    name: str
    total_students: int
    students: List[StudentInfo]