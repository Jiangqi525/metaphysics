# src/domain/healing/events.py
from dataclasses import dataclass
from uuid import UUID
from src.domain.core.entities import DomainEvent


@dataclass
class HealingSessionCreatedEvent(DomainEvent):
    """疗愈会话创建事件"""
    session_id: UUID
    user_id: UUID
    session_type: str

    @property
    def event_type(self) -> str:
        return "healing.session.created"

    def to_dict(self) -> dict:
        return {
            "event_id": str(self.event_id),
            "event_type": self.event_type,
            "occurrence_time": self.occurrence_time,
            "session_id": str(self.session_id),
            "user_id": str(self.user_id),
            "session_type": self.session_type
        }


@dataclass
class HealingSessionStartedEvent(DomainEvent):
    """疗愈会话开始事件"""
    session_id: UUID

    @property
    def event_type(self) -> str:
        return "healing.session.started"

    def to_dict(self) -> dict:
        return {
            "event_id": str(self.event_id),
            "event_type": self.event_type,
            "occurrence_time": self.occurrence_time,
            "session_id": str(self.session_id)
        }


@dataclass
class HealingSessionCompletedEvent(DomainEvent):
    """疗愈会话完成事件"""
    session_id: UUID
    feedback: str

    @property
    def event_type(self) -> str:
        return "healing.session.completed"

    def to_dict(self) -> dict:
        return {
            "event_id": str(self.event_id),
            "event_type": self.event_type,
            "occurrence_time": self.occurrence_time,
            "session_id": str(self.session_id),
            "feedback": self.feedback
        }


@dataclass
class HealingSessionCancelledEvent(DomainEvent):
    """疗愈会话取消事件"""
    session_id: UUID

    @property
    def event_type(self) -> str:
        return "healing.session.cancelled"

    def to_dict(self) -> dict:
        return {
            "event_id": str(self.event_id),
            "event_type": self.event_type,
            "occurrence_time": self.occurrence_time,
            "session_id": str(self.session_id)
        }


@dataclass
class HealingPackageCreatedEvent(DomainEvent):
    """疗愈套餐创建事件"""
    package_id: UUID
    name: str

    @property
    def event_type(self) -> str:
        return "healing.package.created"

    def to_dict(self) -> dict:
        return {
            "event_id": str(self.event_id),
            "event_type": self.event_type,
            "occurrence_time": self.occurrence_time,
            "package_id": str(self.package_id),
            "name": self.name
        }


@dataclass
class HealingPackageDeactivatedEvent(DomainEvent):
    """疗愈套餐停用事件"""
    package_id: UUID

    @property
    def event_type(self) -> str:
        return "healing.package.deactivated"

    def to_dict(self) -> dict:
        return {
            "event_id": str(self.event_id),
            "event_type": self.event_type,
            "occurrence_time": self.occurrence_time,
            "package_id": str(self.package_id)
        }


@dataclass
class HealingPackageActivatedEvent(DomainEvent):
    """疗愈套餐启用事件"""
    package_id: UUID

    @property
    def event_type(self) -> str:
        return "healing.package.activated"

    def to_dict(self) -> dict:
        return {
            "event_id": str(self.event_id),
            "event_type": self.event_type,
            "occurrence_time": self.occurrence_time,
            "package_id": str(self.package_id)
        }
