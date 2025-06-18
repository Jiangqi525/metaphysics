from sqlalchemy import (
    Column, Integer, String, Date, Text, Boolean, TIMESTAMP, DECIMAL, ForeignKey, JSON
)
from sqlalchemy.orm import relationship
from .base import Base


class JewelryCategoryModel(Base):
    __tablename__ = 'jewelry_categories'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    parent_id = Column(Integer, ForeignKey('jewelry_categories.id'))
    icon_url = Column(String(255))
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    sort_order = Column(Integer, default=0)
    is_del = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(TIMESTAMP, onupdate='CURRENT_TIMESTAMP')

    parent = relationship("JewelryCategoryModel", remote_side=[id])


class JewelryItemModel(Base):
    __tablename__ = 'jewelry_items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    sub_name = Column(String(100))
    brand_id = Column(Integer, ForeignKey('brands.id'))
    category_id = Column(Integer, ForeignKey('jewelry_categories.id'))
    main_image_url = Column(String(255))
    image_urls = Column(Text)
    price_cents = Column(Integer, nullable=False)
    original_price_cents = Column(Integer)
    cost_price_cents = Column(Integer)
    stock_quantity = Column(Integer, default=0)
    sold_quantity = Column(Integer, default=0)
    weight = Column(DECIMAL(10, 2))
    material = Column(String(100))
    gemstone = Column(String(100))
    color = Column(String(50))
    size = Column(String(50))
    suitable_gender = Column(String(20))
    status = Column(String(20))
    is_hot = Column(Boolean, default=False)
    is_recommend = Column(Boolean, default=False)
    is_new = Column(Boolean, default=False)
    view_count = Column(Integer, default=0)
    favorite_count = Column(Integer, default=0)
    description = Column(Text)
    fortune_properties = Column(Text)
    energy_type = Column(String(20))
    healing_effect = Column(Text)
    associated_text = Column(Text)
    energy_frequency = Column(DECIMAL(10, 2))
    healing_cycles = Column(Integer, default=0)
    is_limited = Column(Boolean, default=False)
    launch_date = Column(Date)
    knowledge_embedding = Column(Text)
    is_del = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(TIMESTAMP, onupdate='CURRENT_TIMESTAMP')

    brand = relationship("BrandModel")
    category = relationship("JewelryCategoryModel")


class BrandModel(Base):
    __tablename__ = 'brands'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    logo_url = Column(String(255))
    description = Column(Text)
    origin_country = Column(String(50))
    brand_story = Column(Text)
    is_active = Column(Boolean, default=True)
    is_del = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(TIMESTAMP, onupdate='CURRENT_TIMESTAMP')


class JewelryZodiacModel(Base):
    __tablename__ = 'jewelry_zodiacs'

    jewelry_id = Column(Integer, ForeignKey('jewelry_items.id'), primary_key=True)
    zodiac_id = Column(Integer, ForeignKey('zodiac_signs.id'), primary_key=True)
    is_recommended = Column(Boolean, default=False)
    association_strength = Column(Integer, default=1)
    is_del = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')

    jewelry = relationship("JewelryItemModel")
    zodiac = relationship("ZodiacSignModel")


class JewelryChineseZodiacModel(Base):
    __tablename__ = 'jewelry_chinese_zodiacs'

    jewelry_id = Column(Integer, ForeignKey('jewelry_items.id'), primary_key=True)
    chinese_zodiac_id = Column(Integer, ForeignKey('chinese_zodiacs.id'), primary_key=True)
    is_recommended = Column(Boolean, default=False)
    association_strength = Column(Integer, default=1)
    is_del = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')

    jewelry = relationship("JewelryItemModel")
    chinese_zodiac = relationship("ChineseZodiacModel")


class JewelryElementModel(Base):
    __tablename__ = 'jewelry_elements'

    jewelry_id = Column(Integer, ForeignKey('jewelry_items.id'), primary_key=True)
    element_id = Column(Integer, ForeignKey('elements.id'), primary_key=True)
    is_recommended = Column(Boolean, default=False)
    association_strength = Column(Integer, default=1)
    is_del = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')

    jewelry = relationship("JewelryItemModel")
    element = relationship("ElementModel")


class JewelryEnergyModel(Base):
    __tablename__ = 'jewelry_energy'

    id = Column(Integer, primary_key=True, autoincrement=True)
    jewelry_id = Column(Integer, ForeignKey('jewelry_items.id'), nullable=False)
    energy_type = Column(String(20))
    energy_value = Column(DECIMAL(3, 1))
    associated_text = Column(Text)
    sound_freq = Column(String(50))
    is_default = Column(Boolean, default=False)
    is_del = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(TIMESTAMP, onupdate='CURRENT_TIMESTAMP')

    jewelry = relationship("JewelryItemModel")
