from sqlalchemy import (
    Column, Integer, String, Date, Enum, Boolean, TIMESTAMP, DECIMAL, ForeignKey
)
from sqlalchemy.orm import relationship
from .base import Base
import enum


class Gender(enum.Enum):
    unknown = 'unknown'
    male = 'male'
    female = 'female'
    other = 'other'


class AuthType(enum.Enum):
    email = 'email'
    phone = 'phone'
    wechat = 'wechat'
    qq = 'qq'
    weibo = 'weibo'


class UserModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    salt = Column(String(64), nullable=False)
    birthdate = Column(Date)
    gender = Column(Enum(Gender), default=Gender.unknown)
    phone = Column(String(20), unique=True)
    avatar_url = Column(String(255))
    user_level = Column(Integer, default=1)
    points = Column(Integer, default=0)
    is_verified = Column(Boolean, default=False)
    last_login_at = Column(TIMESTAMP)
    last_login_ip = Column(String(45))
    is_active = Column(Boolean, default=True)
    is_del = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(TIMESTAMP, onupdate='CURRENT_TIMESTAMP')
    face_scan_token = Column(String(255))
    palm_print_hash = Column(String(255))
    emotion_score = Column(DECIMAL(3, 1))
    astrological_index = Column(DECIMAL(5, 2), default=0.0)
    last_energy_scan = Column(TIMESTAMP)
    device_fingerprint = Column(String(255))
    security_question = Column(String(255))

    user_auths = relationship("UserAuthModel", back_populates="user")
    user_profiles = relationship("UserProfileModel", back_populates="user", uselist=False)


class UserAuthModel(Base):
    __tablename__ = 'user_auths'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    auth_type = Column(Enum(AuthType), nullable=False)
    identifier = Column(String(100), nullable=False)
    credential = Column(String(255))
    is_primary = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    is_del = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(TIMESTAMP, onupdate='CURRENT_TIMESTAMP')

    user = relationship("UserModel", back_populates="user_auths")


class UserProfileModel(Base):
    __tablename__ = 'user_profiles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True, nullable=False)
    zodiac_id = Column(Integer, ForeignKey('zodiac_signs.id'))
    chinese_zodiac_id = Column(Integer, ForeignKey('chinese_zodiacs.id'))
    birth_time = Column(String(8))
    birth_location = Column(String(50))
    constellation_element = Column(Integer, ForeignKey('elements.id'))
    character_traits = Column(String(255))
    fortune_preferences = Column(String(255))
    jewelry_style_preferences = Column(String(255))
    wuxing_attribute = Column(Integer, ForeignKey('elements.id'))
    emotion_tags = Column(String(255))
    facial_features = Column(String(255))
    is_del = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(TIMESTAMP, onupdate='CURRENT_TIMESTAMP')

    user = relationship("UserModel", back_populates="user_profiles")
    zodiac = relationship("ZodiacSignModel")
    chinese_zodiac = relationship("ChineseZodiacModel")
    constellation_element_rel = relationship("ElementModel", foreign_keys=[constellation_element])
    wuxing_attribute_rel = relationship("ElementModel", foreign_keys=[wuxing_attribute])