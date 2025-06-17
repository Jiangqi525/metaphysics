# src/domain/core/entities.py
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional
from uuid import UUID, uuid4


class AggregateRoot(ABC):
    """聚合根基类，所有聚合的根实体应继承此类"""
    id: UUID

    def __init__(self, id: UUID = None):
        self.id = id or uuid4()

    @abstractmethod
    def get_domain_events(self) -> List["DomainEvent"]:
        """获取该实体产生的领域事件"""
        pass

    @abstractmethod
    def clear_domain_events(self) -> None:
        """清除已处理的领域事件"""
        pass


@dataclass
class DomainEvent(ABC):
    """领域事件基类"""
    event_id: UUID = field(default_factory=uuid4)
    occurrence_time: str = field(default_factory=lambda: str(datetime.datetime.now()))

    @property
    @abstractmethod
    def event_type(self) -> str:
        """事件类型标识"""
        pass
