# src/domain/compliance/events.py
from dataclasses import dataclass
from uuid import UUID
from src.domain.core.entities import DomainEvent


@dataclass
class ComplianceCheckStartedEvent(DomainEvent):
    """合规检查开始事件"""
    check_id: UUID

    @property
    def event_type(self) -> str:
        return "compliance.check.started"

    def to_dict(self) -> dict:
        return {
            "event_id": str(self.event_id),
            "event_type": self.event_type,
            "occurrence_time": self.occurrence_time,
            "check_id": str(self.check_id)
        }


@dataclass
class ComplianceCheckCompletedEvent(DomainEvent):
    """合规检查完成事件"""
    check_id: UUID
    result: str
    details: str

    @property
    def event_type(self) -> str:
        return "compliance.check.completed"

    def to_dict(self) -> dict:
        return {
            "event_id": str(self.event_id),
            "event_type": self.event_type,
            "occurrence_time": self.occurrence_time,
            "check_id": str(self.check_id),
            "result": self.result,
            "details": self.details
        }


@dataclass
class ComplianceCheckFailedEvent(DomainEvent):
    """合规检查失败事件"""
    check_id: UUID
    details: str

    @property
    def event_type(self) -> str:
        return "compliance.check.failed"

    def to_dict(self) -> dict:
        return {
            "event_id": str(self.event_id),
            "event_type": self.event_type,
            "occurrence_time": self.occurrence_time,
            "check_id": str(self.check_id),
            "details": self.details
        }


@dataclass
class CompliancePolicyCreatedEvent(DomainEvent):
    """合规政策创建事件"""
    policy_id: UUID
    policy_name: str

    @property
    def event_type(self) -> str:
        return "compliance.policy.created"

    def to_dict(self) -> dict:
        return {
            "event_id": str(self.event_id),
            "event_type": self.event_type,
            "occurrence_time": self.occurrence_time,
            "policy_id": str(self.policy_id),
            "policy_name": self.policy_name
        }


@dataclass
class CompliancePolicyDeactivatedEvent(DomainEvent):
    """合规政策停用事件"""
    policy_id: UUID

    @property
    def event_type(self) -> str:
        return "compliance.policy.deactivated"

    def to_dict(self) -> dict:
        return {
            "event_id": str(self.event_id),
            "event_type": self.event_type,
            "occurrence_time": self.occurrence_time,
            "policy_id": str(self.policy_id)
        }


@dataclass
class CompliancePolicyActivatedEvent(DomainEvent):
    """合规政策启用事件"""
    policy_id: UUID

    @property
    def event_type(self) -> str:
        return "compliance.policy.activated"

    def to_dict(self) -> dict:
        return {
            "event_id": str(self.event_id),
            "event_type": self.event_type,
            "occurrence_time": self.occurrence_time,
            "policy_id": str(self.policy_id)
        }
