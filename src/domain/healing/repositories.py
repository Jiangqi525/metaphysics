# src/domain/healing/repositories.py
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from src.domain.healing.entities import HealingSession, HealingPackage


class HealingSessionRepository(ABC):
    """疗愈会话存储库接口"""

    @abstractmethod
    def save(self, session: HealingSession) -> None:
        """保存疗愈会话信息"""
        pass

    @abstractmethod
    def find_by_id(self, session_id: UUID) -> Optional[HealingSession]:
        """根据ID查找疗愈会话信息"""
        pass

    @abstractmethod
    def find_by_user_id(self, user_id: UUID) -> List[HealingSession]:
        """根据用户ID查找疗愈会话信息"""
        pass

    @abstractmethod
    def update(self, session: HealingSession) -> None:
        """更新疗愈会话信息"""
        pass

    @abstractmethod
    def delete(self, session_id: UUID) -> None:
        """删除疗愈会话信息"""
        pass


class HealingPackageRepository(ABC):
    """疗愈套餐存储库接口"""

    @abstractmethod
    def save(self, package: HealingPackage) -> None:
        """保存疗愈套餐信息"""
        pass

    @abstractmethod
    def find_by_id(self, package_id: UUID) -> Optional[HealingPackage]:
        """根据ID查找疗愈套餐信息"""
        pass

    @abstractmethod
    def find_all_active(self) -> List[HealingPackage]:
        """查找所有活跃的疗愈套餐信息"""
        pass

    @abstractmethod
    def update(self, package: HealingPackage) -> None:
        """更新疗愈套餐信息"""
        pass

    @abstractmethod
    def delete(self, package_id: UUID) -> None:
        """删除疗愈套餐信息"""
        pass