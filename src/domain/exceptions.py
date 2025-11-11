"""
自定義領域異常
"""


class DomainException(Exception):
    """領域異常基礎類別"""
    pass


class StudentIDMismatchError(DomainException):
    """學生ID不匹配錯誤"""
    pass


class AttendanceProcessingError(DomainException):
    """出勤處理錯誤"""
    pass


class InvalidAttendanceDataError(DomainException):
    """無效的出勤數據錯誤"""
    pass