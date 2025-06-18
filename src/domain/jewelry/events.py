# src/domain/jewelry/events.py
from dataclasses import dataclass
from uuid import UUID
from src.domain.core.entities import DomainEvent


@dataclass
class JewelryCreatedEvent(DomainEvent):
    """珠宝创建事件"""
    jewelry_id: UUID
    name: str
    category_id: int

    @property
    def event_type(self) -> str:
        return "jewelry.created"

    def to_dict(self) -> dict:
        return {
            "event_id": str(self.event_id),
            "event_type": self.event_type,
            "occurrence_time": self.occurrence_time,
            "jewelry_id": str(self.jewelry_id),
            "name": self.name,
            "category_id": self.category_id
        }


@dataclass
class JewelryUpdatedEvent(DomainEvent):
    """珠宝更新事件"""
    jewelry_id: UUID
    updated_fields: list

    @property
    def event_type(self) -> str:
        return "jewelry.updated"

    def to_dict(self) -> dict:
        return {
            "event_id": str(self.event_id),
            "event_type": self.event_type,
            "occurrence_time": self.occurrence_time,
            "jewelry_id": str(self.jewelry_id),
            "updated_fields": self.updated_fields
        }


@dataclass
class JewelryDeletedEvent(DomainEvent):
    """珠宝删除事件"""
    jewelry_id: UUID

    @property
    def event_type(self) -> str:
        return "jewelry.deleted"

    def to_dict(self) -> dict:
        return {
            "event_id": str(self.event_id),
            "event_type": self.event_type,
            "occurrence_time": self.occurrence_time,
            "jewelry_id": str(self.jewelry_id)
        }


@dataclass
class JewelryCategoryCreatedEvent(DomainEvent):
    """珠宝分类创建事件"""
    category_id: int
    name: str

    @property
    def event_type(self) -> str:
        return "jewelry.category.created"

    def to_dict(self) -> dict:
        return {
            "event_id": str(self.event_id),
            "event_type": self.event_type,
            "occurrence_time": self.occurrence_time,
            "category_id": self.category_id,
            "name": self.name
        }


@dataclass
class JewelryCategoryUpdatedEvent(DomainEvent):
    """珠宝分类更新事件"""
    category_id: int
    updated_fields: list

    @property
    def event_type(self) -> str:
        return "jewelry.category.updated"

    def to_dict(self) -> dict:
        return {
            "event_id": str(self.event_id),
            "event_type": self.event_type,
            "occurrence_time": self.occurrence_time,
            "category_id": self.category_id,
            "updated_fields": self.updated_fields
        }


@dataclass
class JewelryCategoryDeletedEvent(DomainEvent):
    """珠宝分类删除事件"""
    category_id: int

    @property
    def event_type(self) -> str:
        return "jewelry.category.deleted"

    def to_dict(self) -> dict:
        return {
            "event_id": str(self.event_id),
            "event_type": self.event_type,
            "occurrence_time": self.occurrence_time,
            "category_id": self.category_id
        }
