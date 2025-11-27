from abc import ABC, abstractmethod
from typing import Any
import flet as ft


class BaseComponent(ABC):
    """UI組件基礎類別"""
    
    def __init__(self):
        self._container = None
    
    @abstractmethod
    def create(self) -> ft.Container:
        """創建並返回組件容器"""
        pass
    
    def get_container(self) -> ft.Container:
        """獲取組件容器"""
        if self._container is None:
            self._container = self.create()
        return self._container
    
    def update(self):
        """更新組件顯示"""
        if self._container:
            self._container.update()