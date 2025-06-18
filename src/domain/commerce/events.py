# src/domain/commerce/events.py
from dataclasses import dataclass
from uuid import UUID
from src.domain.core.entities import DomainEvent
from typing import List  # 新增导入



@dataclass
class OrderCreatedEvent(DomainEvent):
    """订单创建事件"""
    order_id: UUID
    user_id: UUID
    jewelry_ids: List[UUID]
    total_price: str

    @property
    def event_type(self) -> str:
        return "commerce.order.created"

    def to_dict(self) -> dict:
        return {
            "event_id": str(self.event_id),
            "event_type": self.event_type,
            "occurrence_time": self.occurrence_time,
            "order_id": str(self.order_id),
            "user_id": str(self.user_id),
            "jewelry_ids": [str(id) for id in self.jewelry_ids],
            "total_price": str(self.total_price)
        }


@dataclass
class OrderPaidEvent(DomainEvent):
    """订单支付事件"""
    order_id: UUID

    @property
    def event_type(self) -> str:
        return "commerce.order.paid"

    def to_dict(self) -> dict:
        return {
            "event_id": str(self.event_id),
            "event_type": self.event_type,
            "occurrence_time": self.occurrence_time,
            "order_id": str(self.order_id)
        }


@dataclass
class OrderShippedEvent(DomainEvent):
    """订单发货事件"""
    order_id: UUID

    @property
    def event_type(self) -> str:
        return "commerce.order.shipped"

    def to_dict(self) -> dict:
        return {
            "event_id": str(self.event_id),
            "event_type": self.event_type,
            "occurrence_time": self.occurrence_time,
            "order_id": str(self.order_id)
        }


@dataclass
class OrderCompletedEvent(DomainEvent):
    """订单完成事件"""
    order_id: UUID

    @property
    def event_type(self) -> str:
        return "commerce.order.completed"

    def to_dict(self) -> dict:
        return {
            "event_id": str(self.event_id),
            "event_type": self.event_type,
            "occurrence_time": self.occurrence_time,
            "order_id": str(self.order_id)
        }


@dataclass
class OrderCancelledEvent(DomainEvent):
    """订单取消事件"""
    order_id: UUID

    @property
    def event_type(self) -> str:
        return "commerce.order.cancelled"

    def to_dict(self) -> dict:
        return {
            "event_id": str(self.event_id),
            "event_type": self.event_type,
            "occurrence_time": self.occurrence_time,
            "order_id": str(self.order_id)
        }


@dataclass
class PromotionCreatedEvent(DomainEvent):
    """促销活动创建事件"""
    promotion_id: UUID
    promotion_name: str

    @property
    def event_type(self) -> str:
        return "commerce.promotion.created"

    def to_dict(self) -> dict:
        return {
            "event_id": str(self.event_id),
            "event_type": self.event_type,
            "occurrence_time": self.occurrence_time,
            "promotion_id": str(self.promotion_id),
            "promotion_name": self.promotion_name
        }


@dataclass
class PromotionDeactivatedEvent(DomainEvent):
    """促销活动停用事件"""
    promotion_id: UUID

    @property
    def event_type(self) -> str:
        return "commerce.promotion.deactivated"

    def to_dict(self) -> dict:
        return {
            "event_id": str(self.event_id),
            "event_type": self.event_type,
            "occurrence_time": self.occurrence_time,
            "promotion_id": str(self.promotion_id)
        }


@dataclass
class PromotionActivatedEvent(DomainEvent):
    """促销活动启用事件"""
    promotion_id: UUID

    @property
    def event_type(self) -> str:
        return "commerce.promotion.activated"

    def to_dict(self) -> dict:
        return {
            "event_id": str(self.event_id),
            "event_type": self.event_type,
            "occurrence_time": self.occurrence_time,
            "promotion_id": str(self.promotion_id)
        }
