# src/domain/jewelry/entities.py
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from uuid import UUID
from src.domain.core.entities import AggregateRoot
from src.domain.core.value_objects import EnergyProfile, Money


@dataclass
class JewelryCategory:
    id: int
    name: str
    parent_id: int = None
    icon_url: str = None
    description: str = None
    is_active: bool = True
    sort_order: int = 0
    is_del: bool = False

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "parent_id": self.parent_id,
            "icon_url": self.icon_url,
            "description": self.description,
            "is_active": self.is_active,
            "sort_order": self.sort_order,
            "is_del": self.is_del
        }


@dataclass
class JewelryEnergySignature:
    energy_type: str  # wuxing, emotion, meditation, solar_term
    energy_values: Dict[str, float] = field(default_factory=dict)
    associated_text: str = None
    sound_freq: str = None

    def get_element_value(self, element: str) -> float:
        return self.energy_values.get(element, 0.0)

    def to_dict(self) -> Dict:
        return {
            "energy_type": self.energy_type,
            "energy_values": self.energy_values,
            "associated_text": self.associated_text,
            "sound_freq": self.sound_freq
        }


@dataclass
class Jewelry(AggregateRoot):
    name: str
    sub_name: str = None
    brand_id: int = None
    category_id: int = None
    main_image_url: str = None
    image_urls: List[str] = field(default_factory=list)
    price: Money = field(default_factory=lambda: Money(decimal.Decimal(0)))
    original_price: Money = field(default_factory=lambda: Money(decimal.Decimal(0)))
    cost_price: Money = field(default_factory=lambda: Money(decimal.Decimal(0)))
    stock_quantity: int = 0
    sold_quantity: int = 0
    weight: float = 0.0
    material: str = None
    gemstone: str = None
    color: str = None
    size: str = None
    suitable_gender: str = "all"
    status: str = "draft"  # draft, pending, online, offline, sold_out
    is_hot: bool = False
    is_recommend: bool = False
    is_new: bool = False
    view_count: int = 0
    favorite_count: int = 0
    description: str = None
    fortune_properties: str = None
    energy_signature: JewelryEnergySignature = field(default_factory=JewelryEnergySignature)
    energy_frequency: float = 0.0
    healing_cycles: int = 0
    is_limited: bool = False
    launch_date: str = None
    created_at: str = field(default_factory=lambda: str(datetime.datetime.now()))
    updated_at: str = field(default_factory=lambda: str(datetime.datetime.now()))

    def update_price(self, price: Money, original_price: Money = None) -> None:
        self.price = price
        if original_price:
            self.original_price = original_price
        self.updated_at = str(datetime.datetime.now())

    def update_stock(self, quantity: int) -> None:
        if quantity < 0:
            raise ValueError("Stock quantity cannot be negative")
        self.stock_quantity = quantity
        self.updated_at = str(datetime.datetime.now())

    def increase_stock(self, quantity: int) -> None:
        if quantity < 0:
            raise ValueError("Quantity cannot be negative")
        self.stock_quantity += quantity
        self.updated_at = str(datetime.datetime.now())

    def decrease_stock(self, quantity: int) -> None:
        if quantity < 0:
            raise ValueError("Quantity cannot be negative")
        if self.stock_quantity < quantity:
            raise ValueError("Insufficient stock")
        self.stock_quantity -= quantity
        self.sold_quantity += quantity
        self.updated_at = str(datetime.datetime.now())

    def update_energy_signature(self, energy_signature: JewelryEnergySignature) -> None:
        self.energy_signature = energy_signature
        self.updated_at = str(datetime.datetime.now())
