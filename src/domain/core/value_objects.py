# src/domain/core/value_objects.py
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from uuid import UUID, uuid4
import decimal


@dataclass(frozen=True)
class Money:
    amount: decimal.Decimal
    currency: str = "CNY"

    def __add__(self, other):
        if self.currency != other.currency:
            raise ValueError("Cannot add money with different currencies")
        return Money(self.amount + other.amount, self.currency)

    def __sub__(self, other):
        if self.currency != other.currency:
            raise ValueError("Cannot subtract money with different currencies")
        return Money(self.amount - other.amount, self.currency)


@dataclass(frozen=True)
class EnergyProfile:
    wuxing: Dict[str, float] = field(default_factory=dict)  # 五行能量值
    emotion_score: float = 0.0  # 情绪评分
    spiritual_power: int = 0  # 灵力值

    def get_element_value(self, element: str) -> float:
        return self.wuxing.get(element, 0.0)

    def update_wuxing(self, element: str, value: float) -> 'EnergyProfile':
        updated_wuxing = self.wuxing.copy()
        updated_wuxing[element] = value
        return EnergyProfile(updated_wuxing, self.emotion_score, self.spiritual_power)


@dataclass(frozen=True)
class BirthData:
    birth_datetime: str  # 出生日期时间
    location: Dict[str, float] = field(default_factory=dict)  # 经纬度坐标
    timezone: str = "Asia/Shanghai"

    def to_dict(self) -> Dict:
        return {
            "birth_datetime": self.birth_datetime,
            "location": self.location,
            "timezone": self.timezone
        }


@dataclass(frozen=True)
class Money:
    amount: decimal.Decimal
    currency: str = "CNY"

    def __add__(self, other):
        if self.currency != other.currency:
            raise ValueError("Cannot add money with different currencies")
        return Money(self.amount + other.amount, self.currency)

    def __sub__(self, other):
        if self.currency != other.currency:
            raise ValueError("Cannot subtract money with different currencies")
        return Money(self.amount - other.amount, self.currency)
