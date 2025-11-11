from dataclasses import dataclass
from datetime import datetime
from .attendance_status import AttendanceStatus
from ..entities.student import Student


@dataclass(frozen=True)
class AttendanceDate:
    """出勤日期值物件"""
    value: datetime
    
    def __post_init__(self):
        if not isinstance(self.value, datetime):
            raise ValueError("出勤日期必須是datetime物件")
    
    def to_string(self) -> str:
        """轉換為字串格式"""
        return self.value.strftime("%Y-%m-%d")


@dataclass(frozen=True)
class AttendanceRecord:
    """出勤記錄值物件"""
    student: Student
    date: AttendanceDate
    status: AttendanceStatus
    
    def is_present(self) -> bool:
        """是否出席"""
        return not self.status.affects_attendance_count()
    
    def should_skip(self) -> bool:
        """是否應該跳過點名"""
        return self.status.should_skip_attendance()