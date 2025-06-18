# src/domain/healing/entities.py
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional
from uuid import UUID
from src.domain.core.entities import AggregateRoot
from src.domain.core.value_objects import Money


@dataclass
class HealingSession(AggregateRoot):
    user_id: UUID
    session_type: str  # 疗愈类型，如 "energy_healing", "meditation" 等
    start_time: str
    end_time: str
    duration: int  # 疗愈时长（分钟）
    status: str = "pending"  # 状态：pending, in_progress, completed, cancelled
    cost: Money = field(default_factory=lambda: Money(0))
    jewelry_ids: List[int] = field(default_factory=list)  # 本次疗愈使用的珠宝ID列表
    feedback: str = ""  # 用户反馈
    created_at: str = field(default_factory=lambda: str(datetime.datetime.now()))
    updated_at: str = field(default_factory=lambda: str(datetime.datetime.now()))

    def start_session(self) -> None:
        if self.status != "pending":
            raise ValueError("Session cannot be started from this status.")
        self.status = "in_progress"
        self.updated_at = str(datetime.datetime.now())

    def complete_session(self, feedback: str = "") -> None:
        if self.status != "in_progress":
            raise ValueError("Session must be in progress to be completed.")
        self.status = "completed"
        self.feedback = feedback
        self.updated_at = str(datetime.datetime.now())

    def cancel_session(self) -> None:
        if self.status in ["completed", "cancelled"]:
            raise ValueError("Session cannot be cancelled from this status.")
        self.status = "cancelled"
        self.updated_at = str(datetime.datetime.now())


@dataclass
class HealingPackage(AggregateRoot):
    name: str
    description: str
    session_types: List[str]  # 包含的疗愈类型列表
    price: Money
    session_count: int  # 包含的疗愈次数
    is_active: bool = True
    created_at: str = field(default_factory=lambda: str(datetime.datetime.now()))
    updated_at: str = field(default_factory=lambda: str(datetime.datetime.now()))

    def deactivate_package(self) -> None:
        if not self.is_active:
            raise ValueError("Package is already inactive.")
        self.is_active = False
        self.updated_at = str(datetime.datetime.now())

    def activate_package(self) -> None:
        if self.is_active:
            raise ValueError("Package is already active.")
        self.is_active = True
        self.updated_at = str(datetime.datetime.now())
