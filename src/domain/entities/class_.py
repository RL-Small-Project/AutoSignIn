from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from .student import Student, StudentId


@dataclass(frozen=True)
class ClassName:
    """班級名稱值物件"""
    value: str
    
    def __post_init__(self):
        if not self.value or not self.value.strip():
            raise ValueError("班級名稱不能為空")
        if self.value not in ["A", "B"]:
            raise ValueError("班級名稱必須是 A 或 B")


class Class:
    """班級聚合根"""
    
    def __init__(self, name: ClassName):
        self._name = name
        self._students: List[Student] = []
    
    @property
    def name(self) -> ClassName:
        return self._name
    
    @property
    def students(self) -> List[Student]:
        return self._students.copy()
    
    def add_student(self, student: Student) -> None:
        """新增學生到班級"""
        if student in self._students:
            raise ValueError(f"學生 {student.name.value} 已經在班級中")
        self._students.append(student)
    
    def remove_student(self, student_id: StudentId) -> None:
        """從班級移除學生"""
        student = self.find_student(student_id)
        if student:
            self._students.remove(student)
    
    def find_student(self, student_id: StudentId) -> Optional[Student]:
        """根據學生ID尋找學生"""
        for student in self._students:
            if student.student_id == student_id:
                return student
        return None
    
    def get_total_students(self) -> int:
        """取得班級總人數"""
        return len(self._students)
    
    def __str__(self) -> str:
        return f"Class(name={self._name.value}, students={len(self._students)})"