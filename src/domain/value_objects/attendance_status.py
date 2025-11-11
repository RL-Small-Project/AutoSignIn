from enum import Enum
from dataclasses import dataclass
from typing import Optional


class AttendanceStatusType(Enum):
    """出勤狀態類型"""
    PRESENT = "present"          # 正常出席
    LATE = "late"               # 遲到
    ABSENT = "absent"           # 曠課
    PARTIAL_ABSENT = "partial"  # 缺節
    LATE_AND_ABSENT = "late_absent"  # 缺遲
    OFFICIAL_LEAVE = "official"  # 公假


@dataclass(frozen=True)
class AttendanceStatus:
    """出勤狀態值物件"""
    status_type: AttendanceStatusType
    description: Optional[str] = None
    
    @classmethod
    def present(cls) -> 'AttendanceStatus':
        """正常出席"""
        return cls(AttendanceStatusType.PRESENT, "正常出席")
    
    @classmethod
    def late(cls) -> 'AttendanceStatus':
        """遲到"""
        return cls(AttendanceStatusType.LATE, "遲到")
    
    @classmethod
    def absent(cls) -> 'AttendanceStatus':
        """曠課"""
        return cls(AttendanceStatusType.ABSENT, "曠課")
    
    @classmethod
    def partial_absent(cls) -> 'AttendanceStatus':
        """缺節"""
        return cls(AttendanceStatusType.PARTIAL_ABSENT, "缺節")
    
    @classmethod
    def late_and_absent(cls) -> 'AttendanceStatus':
        """缺遲"""
        return cls(AttendanceStatusType.LATE_AND_ABSENT, "缺遲")
    
    @classmethod
    def official_leave(cls) -> 'AttendanceStatus':
        """公假"""
        return cls(AttendanceStatusType.OFFICIAL_LEAVE, "公假")
    
    @classmethod
    def from_excel_value(cls, value: str) -> 'AttendanceStatus':
        """從Excel值創建出勤狀態"""
        if not value or value.strip() == "":
            return cls.present()
        
        value_clean = value.strip()
        
        if "遲到" in value_clean:
            return cls.late()
        elif "曠課" in value_clean:
            return cls.absent()
        elif "缺節" in value_clean:
            return cls.partial_absent()
        elif "缺遲" in value_clean:
            return cls.late_and_absent()
        else:
            return cls.present()
    
    def should_skip_attendance(self) -> bool:
        """是否應該跳過點名（如公假）"""
        return self.status_type == AttendanceStatusType.OFFICIAL_LEAVE
    
    def affects_attendance_count(self) -> bool:
        """是否影響出勤人數統計"""
        return self.status_type in [
            AttendanceStatusType.ABSENT,
            AttendanceStatusType.OFFICIAL_LEAVE
        ]