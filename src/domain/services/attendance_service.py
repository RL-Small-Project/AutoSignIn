from abc import ABC, abstractmethod
from typing import List, Callable, Optional
from ..entities.student import StudentId
from ..value_objects.attendance_record import AttendanceRecord


class WebAttendanceSystem(ABC):
    """網頁點名系統抽象介面"""
    
    @abstractmethod
    def verify_student_id(self, excel_student_id: int, index: int) -> bool:
        """驗證學生ID是否與系統一致"""
        pass
    
    @abstractmethod
    def mark_attendance(self, index: int, record: AttendanceRecord) -> None:
        """在網頁上標記出勤狀態"""
        pass
    
    @abstractmethod
    def is_student_on_official_leave(self, index: int) -> bool:
        """檢查學生是否為公假狀態"""
        pass
    
    @abstractmethod
    def get_page_title(self) -> str:
        """取得頁面標題"""
        pass


class AttendanceProcessingService:
    """出勤處理領域服務"""
    
    def __init__(self, web_system: WebAttendanceSystem):
        self._web_system = web_system
    
    def process_attendance_records(
        self, 
        records: List[AttendanceRecord],
        progress_callback: Optional[Callable[[str, AttendanceRecord, int, int], None]] = None
    ) -> 'AttendanceResult':
        """處理出勤記錄
        
        Args:
            records: 出勤記錄列表
            progress_callback: 進度回調函數 (action, record, current, total)
        """
        processed_count = 0
        skipped_count = 0
        errors = []
        total_records = len(records)
        
        for i, record in enumerate(records):
            current_index = i + 1
            student_name = record.student.name.value
            student_id = record.student.student_id.value
            status_desc = record.status.description or "正常出席"
            
            try:
                # 通知開始處理學生
                if progress_callback:
                    progress_callback("processing", record, current_index, total_records)
                
                # 驗證學生ID
                if not self._web_system.verify_student_id(student_id, i):
                    error_msg = f"學號不相符：Excel={student_id} 網頁=系統值，學生：{student_name}"
                    errors.append(error_msg)
                    if progress_callback:
                        progress_callback("error", record, current_index, total_records)
                    continue
                
                # 檢查是否為公假
                if self._web_system.is_student_on_official_leave(i):
                    skipped_count += 1
                    if progress_callback:
                        progress_callback("official_leave", record, current_index, total_records)
                    continue
                
                # 標記出勤狀態
                self._web_system.mark_attendance(i, record)
                
                if record.status.affects_attendance_count():
                    skipped_count += 1
                    if progress_callback:
                        progress_callback("absent", record, current_index, total_records)
                else:
                    processed_count += 1
                    if progress_callback:
                        progress_callback("present", record, current_index, total_records)
                    
            except Exception as e:
                error_msg = f"處理學生 {student_name} 時發生錯誤: {str(e)}"
                errors.append(error_msg)
                if progress_callback:
                    progress_callback("error", record, current_index, total_records)
        
        return AttendanceResult(
            total_students=len(records),
            processed_count=processed_count,
            skipped_count=skipped_count,
            errors=errors
        )


class AttendanceResult:
    """出勤處理結果"""
    
    def __init__(self, total_students: int, processed_count: int, 
                 skipped_count: int, errors: List[str]):
        self.total_students = total_students
        self.processed_count = processed_count
        self.skipped_count = skipped_count
        self.errors = errors
    
    @property
    def actual_attendance(self) -> int:
        """實際出勤人數"""
        return self.total_students - self.skipped_count
    
    @property
    def has_errors(self) -> bool:
        """是否有錯誤"""
        return len(self.errors) > 0
    
    def get_summary(self) -> str:
        """取得結果摘要"""
        return f"應到人數: {self.total_students} | 實到人數: {self.actual_attendance}"