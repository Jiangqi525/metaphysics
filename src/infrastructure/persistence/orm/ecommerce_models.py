from sqlalchemy import (
    Column, Integer, String, Date, Text, Boolean, TIMESTAMP, DECIMAL, ForeignKey, JSON, BigInteger
)
from sqlalchemy.orm import relationship
from .base import Base


class OrderModel(Base):
    __tablename__ = 'orders'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    order_no = Column(String(32), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    total_amount_cents = Column(BigInteger, nullable=False)
    discount_amount_cents = Column(Integer, default=0)
    actual_amount_cents = Column(BigInteger, nullable=False)
    payment_method = Column(String(20))
    payment_status = Column(String(20))
    payment_time = Column(TIMESTAMP)
    delivery_status = Column(String(20))
    delivery_time = Column(TIMESTAMP)
    sign_time = Column(TIMESTAMP)
    order_status = Column(String(20))
    cancel_reason = Column(Text)
    refund_reason = Column(Text)
    refund_amount_cents = Column(Integer, default=0)
    user_note = Column(Text)
    admin_note = Column(Text)
    shipping_address_id = Column(Integer, ForeignKey('user_addresses.id'))
    tracking_number = Column(String(100))
    logistics_company = Column(String(50))
    healing_package_id = Column(Integer)
    fortune_recommendation_id = Column(Integer, ForeignKey('divination_records.id'))
    promotion_rules = Column(JSON)
    knowledge_embedding = Column(Text)
    is_del = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(TIMESTAMP, onupdate='CURRENT_TIMESTAMP')

    user = relationship("UserModel")
    order_items = relationship("OrderItemModel", back_populates="order")
    shipping_address = relationship("UserAddressModel")
    fortune_recommendation = relationship("DivinationRecordModel")


class OrderItemModel(Base):
    __tablename__ = 'order_items'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    order_id = Column(BigInteger, ForeignKey('orders.id'), nullable=False)
    jewelry_id = Column(Integer, ForeignKey('jewelry_items.id'), nullable=False)
    jewelry_name = Column(String(100), nullable=False)
    jewelry_image_url = Column(String(255))
    price_cents = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    total_amount_cents = Column(Integer, nullable=False)
    specifications = Column(Text)
    relation_strength = Column(DECIMAL(5, 2), default=1.0)
    is_del = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(TIMESTAMP, onupdate='CURRENT_TIMESTAMP')

    order = relationship("OrderModel", back_populates="order_items")
    jewelry = relationship("JewelryItemModel")


class UserAddressModel(Base):
    __tablename__ = 'user_addresses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    consignee = Column(String(50), nullable=False)
    phone = Column(String(20), nullable=False)
    country = Column(String(50))
    province = Column(String(50))
    city = Column(String(50))
    district = Column(String(50))
    address_detail = Column(String(255), nullable=False)
    postal_code = Column(String(20))
    is_default = Column(Boolean, default=False)
    is_del = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(TIMESTAMP, onupdate='CURRENT_TIMESTAMP')

    user = relationship("UserModel")


class CouponModel(Base):
    __tablename__ = 'coupons'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    coupon_type = Column(String(20))
    amount_cents = Column(Integer)
    discount_rate = Column(DECIMAL(5, 2))
    min_amount_cents = Column(Integer, default=0)
    max_discount_cents = Column(Integer)
    start_time = Column(TIMESTAMP)
    end_time = Column(TIMESTAMP)
    total_count = Column(Integer, default=0)
    used_count = Column(Integer, default=0)
    per_user_limit = Column(Integer, default=1)
    applicable_products = Column(JSON)
    applicable_categories = Column(JSON)
    knowledge_vector = Column(Text)
    is_active = Column(Boolean, default=True)
    is_del = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(TIMESTAMP, onupdate='CURRENT_TIMESTAMP')


class UserCouponModel(Base):
    __tablename__ = 'user_coupons'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    coupon_id = Column(Integer, ForeignKey('coupons.id'), nullable=False)
    coupon_code = Column(String(50), unique=True, nullable=False)
    status = Column(String(20))
    order_id = Column(BigInteger, ForeignKey('orders.id'))
    used_time = Column(TIMESTAMP)
    relation_strength = Column(DECIMAL(5, 2), default=1.0)
    is_del = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(TIMESTAMP, onupdate='CURRENT_TIMESTAMP')

    user = relationship("UserModel")
    coupon = relationship("CouponModel")
    order = relationship("OrderModel")


class PaymentRecordModel(Base):
    __tablename__ = 'payment_records'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    order_id = Column(BigInteger, ForeignKey('orders.id'), nullable=False)
    payment_no = Column(String(64), unique=True, nullable=False)
    payment_method = Column(String(20))
    amount_cents = Column(Integer, nullable=False)
    status = Column(String(20))
    transaction_id = Column(String(100))
    payment_time = Column(TIMESTAMP)
    failure_reason = Column(Text)
    is_del = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(TIMESTAMP, onupdate='CURRENT_TIMESTAMP')

    order = relationship("OrderModel")


class RefundRecordModel(Base):
    __tablename__ = 'refund_records'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    order_id = Column(BigInteger, ForeignKey('orders.id'), nullable=False)
    refund_no = Column(String(64), unique=True, nullable=False)
    payment_record_id = Column(BigInteger, ForeignKey('payment_records.id'), nullable=False)
    amount_cents = Column(Integer, nullable=False)
    reason = Column(Text)
    status = Column(String(20))
    refund_time = Column(TIMESTAMP)
    transaction_id = Column(String(100))
    failure_reason = Column(Text)
    operator_id = Column(Integer)
    operator_note = Column(Text)
    is_del = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(TIMESTAMP, onupdate='CURRENT_TIMESTAMP')

    order = relationship("OrderModel")
    payment_record = relationship("PaymentRecordModel")