from sqlalchemy import Column, Integer, String, Text, DateTime
from src.infrastructure.persistence.orm.base import Base
import datetime


class SystemConfig(Base):
    __tablename__ = 'system_configs'

    id = Column(Integer, primary_key=True)
    config_key = Column(String(100), unique=True, nullable=False)
    config_value = Column(Text, nullable=False)
    config_type = Column(String(20), nullable=False)  # 'string', 'int', 'float', 'json', 'boolean'
    description = Column(String(255), nullable=True)
    last_updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
