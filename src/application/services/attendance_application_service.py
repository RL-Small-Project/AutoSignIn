from typing import List, Optional, Callable
from datetime import datetime

from ..dto.attendance_dto import AttendanceRequest, AttendanceResult as AttendanceResultDTO
from ...domain.entities.class_ import ClassName
from ...domain.value_objects.attendance_record import AttendanceDate, AttendanceRecord
from ...domain.repositories.attendance_repository import AttendanceRepository
from ...domain.services.attendance_service import AttendanceProcessingService, WebAttendanceSystem
from ...domain.exceptions import DomainException


class AutoAttendanceApplicationService:
    """自動點名應用服務"""
    
    def __init__(
        self, 
        attendance_repository: AttendanceRepository,
        web_attendance_system: WebAttendanceSystem
    ):
        self._attendance_repository = attendance_repository
        self._processing_service = AttendanceProcessingService(web_attendance_system)
    
    def execute_auto_attendance(
        self, 
        request: AttendanceRequest,
        progress_callback: Optional[Callable[[str, AttendanceRecord, int, int], None]] = None
    ) -> AttendanceResultDTO:
        """執行自動點名
        
        Args:
            request: 點名請求
            progress_callback: 進度回調函數 (action, record, current, total)
        """
        try:
            # 驗證輸入
            class_name = ClassName(request.class_name)
            attendance_date = AttendanceDate(request.to_datetime())
            
            # 載入出勤記錄
            records = self._attendance_repository.load_from_excel(class_name, attendance_date)
            
            if not records:
                return AttendanceResultDTO(
                    success=False,
                    total_students=0,
                    actual_attendance=0,
                    skipped_count=0,
                    errors=[],
                    message=f"找不到 {request.class_name} 班 {request.date} 的出勤記錄"
                )
            
            # 檢查是否在正確的頁面上
            try:
                if hasattr(self._processing_service._web_system, 'ensure_on_attendance_page'):
                    is_on_correct_page = self._processing_service._web_system.ensure_on_attendance_page()
                    if not is_on_correct_page:
                        return AttendanceResultDTO(
                            success=False,
                            total_students=len(records),
                            actual_attendance=0,
                            skipped_count=0,
                            errors=["瀏覽器未在正確的點名頁面上，請手動導航到點名頁面"],
                            message="頁面檢查失敗"
                        )
            except Exception:
                pass  # 忽略頁面檢查錯誤，繼續執行
            
            # 處理出勤記錄，傳遞進度回調
            result = self._processing_service.process_attendance_records(records, progress_callback)
            
            # 保存處理結果
            if not result.has_errors:
                self._attendance_repository.save_records(records)
            
            return AttendanceResultDTO(
                success=not result.has_errors,
                total_students=result.total_students,
                actual_attendance=result.actual_attendance,
                skipped_count=result.skipped_count,
                errors=result.errors,
                message="自動點名完成！" if not result.has_errors else "點名過程中發生錯誤"
            )
            
        except DomainException as e:
            return AttendanceResultDTO(
                success=False,
                total_students=0,
                actual_attendance=0,
                skipped_count=0,
                errors=[str(e)],
                message=f"領域錯誤: {str(e)}"
            )
        except Exception as e:
            return AttendanceResultDTO(
                success=False,
                total_students=0,
                actual_attendance=0,
                skipped_count=0,
                errors=[str(e)],
                message=f"未預期錯誤: {str(e)}"
            )


class AttendanceQueryService:
    """出勤查詢服務"""
    
    def __init__(self, attendance_repository: AttendanceRepository):
        self._attendance_repository = attendance_repository
    
    def get_class_attendance_records(
        self, 
        class_name: str, 
        date: str
    ) -> List[dict]:
        """查詢班級出勤記錄"""
        try:
            class_name_vo = ClassName(class_name)
            attendance_date = AttendanceDate(datetime.strptime(date, "%Y-%m-%d"))
            
            records = self._attendance_repository.find_by_class_and_date(
                class_name_vo, 
                attendance_date
            )
            
            return [
                {
                    "student_id": record.student.student_id.value,
                    "student_name": record.student.name.value,
                    "status": record.status.description,
                    "is_present": record.is_present()
                }
                for record in records
            ]
            
        except Exception as e:
            return []