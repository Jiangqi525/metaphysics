from sqlalchemy import (
    Column, Integer, String, Date, Text, Boolean, TIMESTAMP, DECIMAL, ForeignKey, JSON
)
from sqlalchemy.orm import relationship
from .base import Base


class LanguageModel(Base):
    __tablename__ = 'languages'

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(10), unique=True, nullable=False)
    name = Column(String(50), nullable=False)
    native_name = Column(String(50), nullable=False)
    is_default = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    sort_order = Column(Integer, default=0)
    is_del = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(TIMESTAMP, onupdate='CURRENT_TIMESTAMP')


class I18nTranslationModel(Base):
    __tablename__ = 'i18n_translations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    table_name = Column(String(100), nullable=False)
    column_name = Column(String(100), nullable=False)
    record_id = Column(Integer, nullable=False)
    language_code = Column(String(10), ForeignKey('languages.code'), nullable=False)
    translated_text = Column(Text)
    is_verified = Column(Boolean, default=False)
    verified_by = Column(Integer)
    verified_at = Column(TIMESTAMP)
    is_del = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(TIMESTAMP, onupdate='CURRENT_TIMESTAMP')

    language = relationship("LanguageModel")


class UserActionModel(Base):
    __tablename__ = 'user_actions'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    action_type = Column(String(50), nullable=False)
    target_type = Column(String(50))
    target_id = Column(Integer)
    platform = Column(String(20))
    device_info = Column(Text)
    ip_address = Column(String(45))
    user_agent = Column(Text)
    action_data = Column(JSON)
    knowledge_embedding = Column(Text)
    is_del = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')


class UserFeedbackModel(Base):
    __tablename__ = 'user_feedbacks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    contact_info = Column(String(255))
    feedback_type = Column(String(20))
    content = Column(Text, nullable=False)
    images = Column(Text)
    reply = Column(Text)
    status = Column(String(20))
    platform = Column(String(20))
    device_info = Column(Text)
    knowledge_vector = Column(Text)
    is_del = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(TIMESTAMP, onupdate='CURRENT_TIMESTAMP')

    user = relationship("UserModel")


class ApiAccessLogModel(Base):
    __tablename__ = 'api_access_logs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    ip_address = Column(String(45))
    endpoint = Column(String(100), nullable=False)
    method = Column(String(10), nullable=False)
    request_data = Column(Text)
    response_data = Column(Text)
    user_agent = Column(Text)
    status_code = Column(Integer)
    execution_time_ms = Column(Integer)
    is_suspected_bot = Column(Boolean, default=False)
    expired_at = Column(TIMESTAMP)
    is_del = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(TIMESTAMP, onupdate='CURRENT_TIMESTAMP')

    user = relationship("UserModel")


class SecurityEventModel(Base):
    __tablename__ = 'security_events'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    ip_address = Column(String(45))
    event_type = Column(String(20))
    event_data = Column(JSON)
    threat_level = Column(String(20))
    is_resolved = Column(Boolean, default=False)
    resolved_by = Column(Integer)
    resolved_at = Column(TIMESTAMP)
    resolution_note = Column(Text)
    evidence_data = Column(JSON)
    is_del = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(TIMESTAMP, onupdate='CURRENT_TIMESTAMP')

    user = relationship("UserModel")


class SystemConfigModel(Base):
    __tablename__ = 'system_configs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    config_key = Column(String(100), unique=True, nullable=False)
    config_value = Column(Text, nullable=False)
    config_type = Column(String(20))
    description = Column(Text)
    is_system = Column(Boolean, default=False)
    knowledge_vector = Column(Text)
    is_del = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(TIMESTAMP, onupdate='CURRENT_TIMESTAMP')


class CampaignModel(Base):
    __tablename__ = 'campaigns'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    banner_url = Column(String(255))
    jump_link = Column(String(255))
    position = Column(String(20))
    start_time = Column(TIMESTAMP)
    end_time = Column(TIMESTAMP)
    is_active = Column(Boolean, default=True)
    priority = Column(Integer, default=0)
    target_audience = Column(JSON)
    display_count = Column(Integer, default=0)
    click_count = Column(Integer, default=0)
    conversion_count = Column(Integer, default=0)
    knowledge_embedding = Column(Text)
    is_del = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(TIMESTAMP, onupdate='CURRENT_TIMESTAMP')


class DailyVisitModel(Base):
    __tablename__ = 'daily_visits'

    id = Column(Integer, primary_key=True, autoincrement=True)
    visit_date = Column(Date, unique=True, nullable=False)
    total_visits = Column(Integer, default=0)
    unique_visitors = Column(Integer, default=0)
    new_users = Column(Integer, default=0)
    active_users = Column(Integer, default=0)
    platform_visits = Column(JSON)
    is_del = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(TIMESTAMP, onupdate='CURRENT_TIMESTAMP')


class DailySaleModel(Base):
    __tablename__ = 'daily_sales'

    id = Column(Integer, primary_key=True, autoincrement=True)
    sales_date = Column(Date, unique=True, nullable=False)
    total_orders = Column(Integer, default=0)
    total_amount_cents = Column(BigInteger, default=0)
    average_order_amount_cents = Column(Integer, default=0)
    total_items = Column(Integer, default=0)
    platform_sales = Column(JSON)
    best_selling_jewelry = Column(JSON)
    is_del = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(TIMESTAMP, onupdate='CURRENT_TIMESTAMP')


class FortuneAlgorithmConfigModel(Base):
    __tablename__ = 'fortune_algorithm_config'

    id = Column(Integer, primary_key=True, autoincrement=True)
    algorithm_name = Column(String(50), nullable=False)
    config_params = Column(JSON, nullable=False)
    accuracy_rate = Column(DECIMAL(5, 2), default=0.0)
    is_active = Column(Boolean, default=True)
    knowledge_vector = Column(Text)
    updated_at = Column(TIMESTAMP)
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')


class UserDeviceModel(Base):
    __tablename__ = 'user_devices'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    device_type = Column(String(20))
    device_id = Column(String(100), nullable=False)
    device_model = Column(String(100))
    os_version = Column(String(50))
    app_version = Column(String(20))
    last_scan_time = Column(TIMESTAMP)
    is_primary = Column(Boolean, default=False)
    relation_strength = Column(DECIMAL(5, 2), default=1.0)
    is_del = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(TIMESTAMP, onupdate='CURRENT_TIMESTAMP')

    user = relationship("UserModel")


class SystemLogModel(Base):
    __tablename__ = 'system_logs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    log_level = Column(String(20))
    message = Column(Text, nullable=False)
    context = Column(JSON)
    file_path = Column(String(255))
    line_number = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'))
    ip_address = Column(String(45))
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')

    user = relationship("UserModel")


class MaintenanceRecordModel(Base):
    __tablename__ = 'maintenance_records'

    id = Column(Integer, primary_key=True, autoincrement=True)
    maintenance_type = Column(String(20))
    start_time = Column(TIMESTAMP, nullable=False)
    end_time = Column(TIMESTAMP, nullable=False)
    description = Column(Text, nullable=False)
    impact_modules = Column(Text)
    operator_id = Column(Integer, ForeignKey('admin_users.id'), nullable=False)
    operator_name = Column(String(50), nullable=False)
    is_completed = Column(Boolean, default=True)
    result_summary = Column(Text)
    is_del = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(TIMESTAMP, onupdate='CURRENT_TIMESTAMP')

    operator = relationship("AdminUserModel")


class AdminUserModel(Base):
    __tablename__ = 'admin_users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    real_name = Column(String(50))
    email = Column(String(255), unique=True)
    phone = Column(String(20))
    avatar_url = Column(String(255))
    role_id = Column(Integer, ForeignKey('admin_roles.id'), nullable=False)
    last_login_at = Column(TIMESTAMP)
    last_login_ip = Column(String(45))
    is_active = Column(Boolean, default=True)
    is_super_admin = Column(Boolean, default=False)
    is_del = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(TIMESTAMP, onupdate='CURRENT_TIMESTAMP')

    role = relationship("AdminRoleModel")


class AdminRoleModel(Base):
    __tablename__ = 'admin_roles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    role_name = Column(String(50), unique=True, nullable=False)
    description = Column(Text)
    permissions = Column(JSON)
    is_default = Column(Boolean, default=False)
    knowledge_vector = Column(Text)
    is_del = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(TIMESTAMP, onupdate='CURRENT_TIMESTAMP')


class SpiritualTransactionModel(Base):
    __tablename__ = 'spiritual_transactions'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    transaction_type = Column(String(20))
    amount = Column(BigInteger, nullable=False)
    source_type = Column(String(20))
    source_id = Column(BigInteger)
    transaction_time = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    description = Column(Text)
    relation_strength = Column(DECIMAL(5, 2), default=1.0)
    is_del = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(TIMESTAMP, onupdate='CURRENT_TIMESTAMP')

    user = relationship("UserModel")


class SpiritualRuleConfigModel(Base):
    __tablename__ = 'spiritual_rule_configs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    rule_name = Column(String(100), nullable=False)
    rule_type = Column(String(20), nullable=False)
    rule_params = Column(JSON, nullable=False)
    effective_time = Column(TIMESTAMP, nullable=False)
    expiry_time = Column(TIMESTAMP)
    is_active = Column(Boolean, default=True)
    is_default = Column(Boolean, default=False)
    knowledge_vector = Column(Text)
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(TIMESTAMP, onupdate='CURRENT_TIMESTAMP')