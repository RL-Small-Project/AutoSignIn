from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class StudentId:
    """學生ID值物件"""
    value: int
    
    def __post_init__(self):
        if self.value <= 0:
            raise ValueError("學生ID必須為正整數")


@dataclass(frozen=True)
class StudentName:
    """學生姓名值物件"""
    value: str
    
    def __post_init__(self):
        if not self.value or not self.value.strip():
            raise ValueError("學生姓名不能為空")
        if len(self.value.strip()) > 50:
            raise ValueError("學生姓名不能超過50個字元")


class Student:
    """學生實體"""
    
    def __init__(self, student_id: StudentId, name: StudentName):
        self._student_id = student_id
        self._name = name
    
    @property
    def student_id(self) -> StudentId:
        return self._student_id
    
    @property
    def name(self) -> StudentName:
        return self._name
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Student):
            return False
        return self._student_id == other._student_id
    
    def __hash__(self) -> int:
        return hash(self._student_id.value)
    
    def __str__(self) -> str:
        return f"Student(id={self._student_id.value}, name={self._name.value})"