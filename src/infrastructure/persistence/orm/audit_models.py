from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from src.infrastructure.persistence.orm.base import Base
import datetime


class SensitiveDataAccessLog(Base):
    __tablename__ = 'sensitive_data_access_log'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)  # 关联用户ID，可为空（如系统操作）
    accessed_by_user_id = Column(Integer, ForeignKey('users.id'), nullable=True)  # 实际操作用户ID
    accessed_table = Column(String(100), nullable=False)
    accessed_field = Column(String(100), nullable=False)
    access_type = Column(String(10), nullable=False)  # 'READ', 'WRITE', 'DELETE'
    access_time = Column(DateTime, default=datetime.datetime.utcnow)
    ip_address = Column(String(45), nullable=True)
    query_params = Column(JSON, nullable=True)  # 记录查询参数或操作详情

    user = relationship("UserModel", foreign_keys=[user_id])
    accessed_by_user = relationship("UserModel", foreign_keys=[accessed_by_user_id])
