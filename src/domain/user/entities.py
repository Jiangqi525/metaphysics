# src/domain/user/entities.py
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from uuid import UUID
from src.domain.core.entities import AggregateRoot
from src.domain.core.value_objects import EnergyProfile, Money
import datetime


@dataclass
class UserProfile:
    zodiac_id: int = None
    chinese_zodiac_id: int = None
    birth_time: str = None
    birth_location: Dict[str, float] = field(default_factory=dict)
    constellation_element: int = None
    character_traits: List[str] = field(default_factory=list)
    fortune_preferences: List[str] = field(default_factory=list)
    jewelry_style_preferences: List[str] = field(default_factory=list)
    wuxing_attribute: int = None
    emotion_tags: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return {
            "zodiac_id": self.zodiac_id,
            "chinese_zodiac_id": self.chinese_zodiac_id,
            "birth_time": self.birth_time,
            "birth_location": self.birth_location,
            "constellation_element": self.constellation_element,
            "character_traits": self.character_traits,
            "fortune_preferences": self.fortune_preferences,
            "jewelry_style_preferences": self.jewelry_style_preferences,
            "wuxing_attribute": self.wuxing_attribute,
            "emotion_tags": self.emotion_tags
        }


@dataclass
class User(AggregateRoot):
    username: str
    email: str
    password_hash: str
    salt: str
    birthdate: str
    gender: str = "unknown"
    phone: str = None
    avatar_url: str = None
    user_level: int = 1
    points: int = 0
    spiritual_power: int = 0
    is_verified: bool = False
    last_login_at: str = None
    last_login_ip: str = None
    is_active: bool = True
    is_del: bool = False
    created_at: str = field(default_factory=lambda: str(datetime.datetime.now()))
    updated_at: str = field(default_factory=lambda: str(datetime.datetime.now()))
    face_scan_token: str = None
    palm_print_hash: str = None
    emotion_score: float = 0.0
    astrological_index: float = 0.0
    last_energy_scan: str = None
    device_fingerprint: str = None
    security_question: str = None
    profile: UserProfile = field(default_factory=UserProfile)
    energy_profile: EnergyProfile = field(default_factory=EnergyProfile)

    def change_password(self, new_password_hash: str, new_salt: str) -> None:
        self.password_hash = new_password_hash
        self.salt = new_salt
        self.updated_at = str(datetime.datetime.now())

    def update_profile(self, profile: UserProfile) -> None:
        self.profile = profile
        self.updated_at = str(datetime.datetime.now())

    def add_spiritual_power(self, amount: int) -> None:
        if amount < 0:
            raise ValueError("Spiritual power amount cannot be negative")
        self.spiritual_power += amount
        self.updated_at = str(datetime.datetime.now())

    def consume_spiritual_power(self, amount: int) -> None:
        if amount < 0:
            raise ValueError("Spiritual power amount cannot be negative")
        if self.spiritual_power < amount:
            raise ValueError("Insufficient spiritual power")
        self.spiritual_power -= amount
        self.updated_at = str(datetime.datetime.now())