from sqlalchemy import (
    Column, Integer, String, Date, Text, Boolean, TIMESTAMP, DECIMAL, ForeignKey, JSON
)
from sqlalchemy.orm import relationship
from .base import Base


class UserHealingRecordModel(Base):
    __tablename__ = 'user_healing_records'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    jewelry_id = Column(Integer, ForeignKey('jewelry_items.id'), nullable=False)
    healing_method = Column(String(20))
    start_time = Column(TIMESTAMP)
    end_time = Column(TIMESTAMP)
    emotion_before = Column(DECIMAL(3, 1))
    emotion_after = Column(DECIMAL(3, 1))
    feedback = Column(Text)
    is_complete = Column(Boolean, default=False)
    spiritual_reward = Column(Integer, default=0)
    knowledge_embedding = Column(Text)
    is_del = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(TIMESTAMP, onupdate='CURRENT_TIMESTAMP')

    user = relationship("UserModel")
    jewelry = relationship("JewelryItemModel")


class AudioHealingResourceModel(Base):
    __tablename__ = 'audio_healing_resources'

    id = Column(Integer, primary_key=True, autoincrement=True)
    resource_name = Column(String(100), nullable=False)
    audio_url = Column(String(255), nullable=False)
    healing_type = Column(String(20))
    associated_jewelry = Column(Text)
    duration_seconds = Column(Integer)
    is_premium = Column(Boolean, default=False)
    play_count = Column(Integer, default=0)
    knowledge_vector = Column(Text)
    is_del = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(TIMESTAMP, onupdate='CURRENT_TIMESTAMP')


class SolarTermEnergyModel(Base):
    __tablename__ = 'solar_term_energy'

    id = Column(Integer, primary_key=True, autoincrement=True)
    solar_term_name = Column(String(50), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    energy_element = Column(Integer, ForeignKey('elements.id'))
    lucky_jewelry_ids = Column(Text)
    healing_ritual = Column(Text)
    related_zodiacs = Column(Text)
    is_del = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(TIMESTAMP, onupdate='CURRENT_TIMESTAMP')

    energy_element_rel = relationship("ElementModel")


class EnergyResonanceModel(Base):
    __tablename__ = 'energy_resonance'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    jewelry_id = Column(Integer, ForeignKey('jewelry_items.id'), nullable=False)
    resonance_time = Column(TIMESTAMP, nullable=False)
    energy_level = Column(DECIMAL(5, 2), nullable=False)
    resonance_pattern = Column(JSON)
    is_optimized = Column(Boolean, default=False)
    relation_strength = Column(DECIMAL(5, 2), default=1.0)
    is_del = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(TIMESTAMP, onupdate='CURRENT_TIMESTAMP')

    user = relationship("UserModel")
    jewelry = relationship("JewelryItemModel")


class ResonanceFeedbackModel(Base):
    __tablename__ = 'resonance_feedback'

    id = Column(Integer, primary_key=True, autoincrement=True)
    resonance_id = Column(Integer, ForeignKey('energy_resonance.id'), nullable=False)
    user_feedback = Column(Text)
    physiological_data = Column(JSON)
    feedback_time = Column(TIMESTAMP, nullable=False)
    knowledge_embedding = Column(Text)
    is_del = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(TIMESTAMP, onupdate='CURRENT_TIMESTAMP')

    resonance = relationship("EnergyResonanceModel")
