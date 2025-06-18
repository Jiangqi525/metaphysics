# src/domain/fortune/events.py
from dataclasses import dataclass
from uuid import UUID
from src.domain.core.entities import DomainEvent  # 现在可以正确导入 DomainEvent

@dataclass
class FortuneAnalysisCreatedEvent(DomainEvent):
    """命理分析创建事件"""
    analysis_id: UUID
    user_id: UUID
    analysis_type: str

    @property
    def event_type(self) -> str:
        return "fortune.analysis.created"

    def to_dict(self) -> dict:
        return {
            "event_id": str(self.event_id),
            "event_type": self.event_type,
            "occurrence_time": self.occurrence_time,
            "analysis_id": str(self.analysis_id),
            "user_id": str(self.user_id),
            "analysis_type": self.analysis_type
        }

@dataclass
class FortuneAnalysisUpdatedEvent(DomainEvent):
    """命理分析更新事件"""
    analysis_id: UUID
    user_id: UUID
    updated_fields: list

    @property
    def event_type(self) -> str:
        return "fortune.analysis.updated"

    def to_dict(self) -> dict:
        return {
            "event_id": str(self.event_id),
            "event_type": self.event_type,
            "occurrence_time": self.occurrence_time,
            "analysis_id": str(self.analysis_id),
            "user_id": str(self.user_id),
            "updated_fields": self.updated_fields
        }