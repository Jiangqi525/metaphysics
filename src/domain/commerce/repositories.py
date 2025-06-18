# src/domain/commerce/repositories.py
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from src.domain.commerce.entities import Order, Promotion


class OrderRepository(ABC):
    """订单存储库接口"""

    @abstractmethod
    def save(self, order: Order) -> None:
        """保存订单信息"""
        pass

    @abstractmethod
    def find_by_id(self, order_id: UUID) -> Optional[Order]:
        """根据ID查找订单信息"""
        pass

    @abstractmethod
    def find_by_user_id(self, user_id: UUID) -> List[Order]:
        """根据用户ID查找订单信息"""
        pass

    @abstractmethod
    def update(self, order: Order) -> None:
        """更新订单信息"""
        pass


class PromotionRepository(ABC):
    """促销活动存储库接口"""

    @abstractmethod
    def save(self, promotion: Promotion) -> None:
        """保存促销活动信息"""
        pass

    @abstractmethod
    def find_by_id(self, promotion_id: UUID) -> Optional[Promotion]:
        """根据ID查找促销活动信息"""
        pass

    @abstractmethod
    def find_all_active(self) -> List[Promotion]:
        """查找所有活跃的促销活动信息"""
        pass

    @abstractmethod
    def update(self, promotion: Promotion) -> None:
        """更新促销活动信息"""
        pass
