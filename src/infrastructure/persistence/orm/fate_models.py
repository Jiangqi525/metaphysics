from sqlalchemy import (
    Column, Integer, String, Date, Text, Boolean, TIMESTAMP, DECIMAL, ForeignKey, JSON
)
from sqlalchemy.orm import relationship
from .base import Base


class ZodiacSignModel(Base):
    __tablename__ = 'zodiac_signs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)
    element_id = Column(Integer, ForeignKey('elements.id'), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    is_chinese = Column(Boolean, default=False)
    description = Column(Text)
    characteristic = Column(Text)
    lucky_color = Column(String(50))
    lucky_number = Column(String(20))
    compatible_zodiacs = Column(Text)
    knowledge_embedding = Column(Text)
    is_del = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(TIMESTAMP, onupdate='CURRENT_TIMESTAMP')

    element = relationship("ElementModel")


class ChineseZodiacModel(Base):
    __tablename__ = 'chinese_zodiacs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)
    year_start = Column(Integer, nullable=False)
    year_end = Column(Integer, nullable=False)
    description = Column(Text)
    characteristic = Column(Text)
    lucky_color = Column(String(50))
    lucky_number = Column(String(20))
    compatible_zodiacs = Column(Text)
    is_del = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(TIMESTAMP, onupdate='CURRENT_TIMESTAMP')


class ElementModel(Base):
    __tablename__ = 'elements'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)
    description = Column(Text)
    characteristic = Column(Text)
    lucky_jewelry_categories = Column(Text)
    related_elements = Column(JSON)
    knowledge_vector = Column(Text)
    is_del = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(TIMESTAMP, onupdate='CURRENT_TIMESTAMP')


class FortuneTypeModel(Base):
    __tablename__ = 'fortune_types'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    description = Column(Text)
    input_requirements = Column(Text)
    algorithm_version = Column(String(20))
    is_active = Column(Boolean, default=True)
    is_del = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(TIMESTAMP, onupdate='CURRENT_TIMESTAMP')


class DivinationRecordModel(Base):
    __tablename__ = 'divination_records'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    fortune_type_id = Column(Integer, ForeignKey('fortune_types.id'), nullable=False)
    input_data = Column(JSON)
    result_data = Column(JSON)
    result_summary = Column(Text)
    is_shared = Column(Boolean, default=False)
    share_count = Column(Integer, default=0)
    scan_type = Column(String(20))
    recommend_jewelry = Column(JSON)
    spiritual_cost = Column(Integer, default=0)
    is_del = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(TIMESTAMP, onupdate='CURRENT_TIMESTAMP')

    user = relationship("UserModel")
    fortune_type = relationship("FortuneTypeModel")


class DivinationInterpretationModel(Base):
    __tablename__ = 'divination_interpretations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    fortune_type_id = Column(Integer, ForeignKey('fortune_types.id'), nullable=False)
    condition_key = Column(String(100), nullable=False)
    interpretation = Column(Text, nullable=False)
    recommended_jewelry = Column(Text)
    is_default = Column(Boolean, default=True)
    is_del = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(TIMESTAMP, onupdate='CURRENT_TIMESTAMP')

    fortune_type = relationship("FortuneTypeModel")


class AIFortuneAnalysisModel(Base):
    __tablename__ = 'ai_fortune_analysis'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    analysis_type = Column(String(20))
    input_data = Column(JSON)
    wuxing_analysis = Column(JSON)
    emotion_trend = Column(JSON)
    lucky_jewelry_ids = Column(Text)
    confidence_score = Column(DECIMAL(3, 2))
    energy_field = Column(JSON)
    destiny_trend = Column(JSON)
    compatibility_score = Column(DECIMAL(5, 2))
    is_del = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(TIMESTAMP, onupdate='CURRENT_TIMESTAMP')

    user = relationship("UserModel")


class FortuneModelModel(Base):
    __tablename__ = 'fortune_models'

    id = Column(Integer, primary_key=True, autoincrement=True)
    model_name = Column(String(100), nullable=False)
    model_type = Column(String(20))
    version = Column(String(20), nullable=False)
    parameters = Column(JSON, nullable=False)
    accuracy_rate = Column(DECIMAL(5, 2), default=0.0)
    is_active = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(TIMESTAMP, onupdate='CURRENT_TIMESTAMP')
