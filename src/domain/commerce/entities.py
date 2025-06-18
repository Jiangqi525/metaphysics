# src/domain/commerce/entities.py
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from uuid import UUID
from src.domain.core.entities import AggregateRoot
from src.domain.core.value_objects import Money


@dataclass
class Order(AggregateRoot):
    user_id: UUID
    jewelry_ids: List[UUID]
    total_price: Money
    status: str = "pending"  # pending, paid, shipped, completed, cancelled
    created_at: str = field(default_factory=lambda: str(datetime.datetime.now()))
    updated_at: str = field(default_factory=lambda: str(datetime.datetime.now()))

    def pay_order(self) -> None:
        if self.status != "pending":
            raise ValueError("Order cannot be paid from this status.")
        self.status = "paid"
        self.updated_at = str(datetime.datetime.now())

    def ship_order(self) -> None:
        if self.status != "paid":
            raise ValueError("Order must be paid to be shipped.")
        self.status = "shipped"
        self.updated_at = str(datetime.datetime.now())

    def complete_order(self) -> None:
        if self.status != "shipped":
            raise ValueError("Order must be shipped to be completed.")
        self.status = "completed"
        self.updated_at = str(datetime.datetime.now())

    def cancel_order(self) -> None:
        if self.status in ["completed", "cancelled"]:
            raise ValueError("Order cannot be cancelled from this status.")
        self.status = "cancelled"
        self.updated_at = str(datetime.datetime.now())


@dataclass
class Promotion(AggregateRoot):
    promotion_name: str
    discount_rate: float
    start_time: str
    end_time: str
    applicable_jewelry_categories: List[int] = field(default_factory=list)
    is_active: bool = True
    created_at: str = field(default_factory=lambda: str(datetime.datetime.now()))
    updated_at: str = field(default_factory=lambda: str(datetime.datetime.now()))

    def deactivate_promotion(self) -> None:
        if not self.is_active:
            raise ValueError("Promotion is already inactive.")
        self.is_active = False
        self.updated_at = str(datetime.datetime.now())

    def activate_promotion(self) -> None:
        if self.is_active:
            raise ValueError("Promotion is already active.")
        self.is_active = True
        self.updated_at = str(datetime.datetime.now())
