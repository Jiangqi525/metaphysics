# src/domain/jewelry/repositories.py
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from src.domain.jewelry.entities import Jewelry, JewelryCategory


class JewelryRepository(ABC):
    """珠宝存储库接口"""

    @abstractmethod
    def save(self, jewelry: Jewelry) -> None:
        """保存珠宝信息"""
        pass

    @abstractmethod
    def find_by_id(self, jewelry_id: UUID) -> Optional[Jewelry]:
        """根据ID查找珠宝信息"""
        pass

    @abstractmethod
    def find_all(self) -> List[Jewelry]:
        """查找所有珠宝信息"""
        pass

    @abstractmethod
    def update(self, jewelry: Jewelry) -> None:
        """更新珠宝信息"""
        pass

    @abstractmethod
    def delete(self, jewelry_id: UUID) -> None:
        """删除珠宝信息"""
        pass


class JewelryCategoryRepository(ABC):
    """珠宝分类存储库接口"""

    @abstractmethod
    def save(self, category: JewelryCategory) -> None:
        """保存珠宝分类信息"""
        pass

    @abstractmethod
    def find_by_id(self, category_id: int) -> Optional[JewelryCategory]:
        """根据ID查找珠宝分类信息"""
        pass

    @abstractmethod
    def find_all(self) -> List[JewelryCategory]:
        """查找所有珠宝分类信息"""
        pass

    @abstractmethod
    def update(self, category: JewelryCategory) -> None:
        """更新珠宝分类信息"""
        pass

    @abstractmethod
    def delete(self, category_id: int) -> None:
        """删除珠宝分类信息"""
        pass