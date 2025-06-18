# src/domain/compliance/entities.py
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from uuid import UUID
from src.domain.core.entities import AggregateRoot


@dataclass
class ComplianceCheck(AggregateRoot):
    """合规检查实体"""
    check_name: str
    check_type: str  # 例如：'data_privacy', 'security', 'regulatory'
    status: str = "pending"  # 状态：pending, in_progress, completed, failed
    start_time: str = field(default_factory=lambda: str(datetime.datetime.now()))
    end_time: Optional[str] = None
    result: Optional[str] = None
    details: Optional[str] = None

    def start_check(self) -> None:
        if self.status != "pending":
            raise ValueError("Check cannot be started from this status.")
        self.status = "in_progress"

    def complete_check(self, result: str, details: str) -> None:
        if self.status != "in_progress":
            raise ValueError("Check must be in progress to be completed.")
        self.status = "completed"
        self.end_time = str(datetime.datetime.now())
        self.result = result
        self.details = details

    def fail_check(self, details: str) -> None:
        if self.status != "in_progress":
            raise ValueError("Check must be in progress to fail.")
        self.status = "failed"
        self.end_time = str(datetime.datetime.now())
        self.details = details


@dataclass
class CompliancePolicy(AggregateRoot):
    """合规政策实体"""
    policy_name: str
    policy_description: str
    policy_type: str  # 例如：'data_privacy', 'security', 'regulatory'
    is_active: bool = True
    created_at: str = field(default_factory=lambda: str(datetime.datetime.now()))
    updated_at: str = field(default_factory=lambda: str(datetime.datetime.now()))

    def deactivate_policy(self) -> None:
        if not self.is_active:
            raise ValueError("Policy is already inactive.")
        self.is_active = False
        self.updated_at = str(datetime.datetime.now())

    def activate_policy(self) -> None:
        if self.is_active:
            raise ValueError("Policy is already active.")
        self.is_active = True
        self.updated_at = str(datetime.datetime.now())