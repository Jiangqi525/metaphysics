# src/domain/user/events.py
from dataclasses import dataclass
from uuid import UUID
from src.domain.core.entities import DomainEvent


@dataclass
class UserRegisteredEvent(DomainEvent):
    """用户注册事件"""
    user_id: UUID
    username: str
    email: str

    @property
    def event_type(self) -> str:
        return "user.registered"

    def to_dict(self) -> dict:
        return {
            "event_id": str(self.event_id),
            "event_type": self.event_type,
            "occurrence_time": self.occurrence_time,
            "user_id": str(self.user_id),
            "username": self.username,
            "email": self.email
        }


@dataclass
class UserProfileUpdatedEvent(DomainEvent):
    """用户资料更新事件"""
    user_id: UUID
    profile_changes: dict

    @property
    def event_type(self) -> str:
        return "user.profile.updated"

    def to_dict(self) -> dict:
        return {
            "event_id": str(self.event_id),
            "event_type": self.event_type,
            "occurrence_time": self.occurrence_time,
            "user_id": str(self.user_id),
            "profile_changes": self.profile_changes
        }


@dataclass
class SpiritualPowerChangedEvent(DomainEvent):
    """灵力值变更事件"""
    user_id: UUID
    amount: int
    change_type: str  # increase/decrease
    source_type: str  # recharge/consume/reward/transfer

    @property
    def event_type(self) -> str:
        return "user.spiritual.power.changed"

    def to_dict(self) -> dict:
        return {
            "event_id": str(self.event_id),
            "event_type": self.event_type,
            "occurrence_time": self.occurrence_time,
            "user_id": str(self.user_id),
            "amount": self.amount,
            "change_type": self.change_type,
            "source_type": self.source_type
        }