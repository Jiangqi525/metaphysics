from sqlalchemy import (
    Column, Integer, String, Date, Text, Boolean, TIMESTAMP, DECIMAL, ForeignKey, JSON
)
from sqlalchemy.orm import relationship
from .base import Base


class UserRelationModel(Base):
    __tablename__ = 'user_relations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    follower_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    following_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    is_mutual = Column(Boolean, default=False)
    relation_strength = Column(DECIMAL(5, 2), default=1.0)
    is_del = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(TIMESTAMP, onupdate='CURRENT_TIMESTAMP')

    follower = relationship("UserModel", foreign_keys=[follower_id])
    following = relationship("UserModel", foreign_keys=[following_id])


class PostModel(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String(200))
    content = Column(Text, nullable=False)
    images = Column(Text)
    post_type = Column(String(20))
    jewelry_id = Column(Integer, ForeignKey('jewelry_items.id'))
    fortune_record_id = Column(Integer, ForeignKey('divination_records.id'))
    is_published = Column(Boolean, default=True)
    is_hidden = Column(Boolean, default=False)
    view_count = Column(Integer, default=0)
    like_count = Column(Integer, default=0)
    comment_count = Column(Integer, default=0)
    share_count = Column(Integer, default=0)
    spiritual_reward = Column(Integer, default=0)
    knowledge_embedding = Column(Text)
    is_del = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(TIMESTAMP, onupdate='CURRENT_TIMESTAMP')

    user = relationship("UserModel")
    jewelry = relationship("JewelryItemModel")
    fortune_record = relationship("DivinationRecordModel")


class PostTagModel(Base):
    __tablename__ = 'post_tags'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    knowledge_vector = Column(Text)
    is_del = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(TIMESTAMP, onupdate='CURRENT_TIMESTAMP')


class PostTagRelationModel(Base):
    __tablename__ = 'post_tag_relations'

    post_id = Column(Integer, ForeignKey('posts.id'), primary_key=True)
    tag_id = Column(Integer, ForeignKey('post_tags.id'), primary_key=True)
    relation_strength = Column(DECIMAL(5, 2), default=1.0)
    is_del = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')

    post = relationship("PostModel")
    tag = relationship("PostTagModel")


class CommentModel(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)
    parent_comment_id = Column(Integer, ForeignKey('comments.id'))
    content = Column(Text, nullable=False)
    like_count = Column(Integer, default=0)
    knowledge_embedding = Column(Text)
    is_del = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(TIMESTAMP, onupdate='CURRENT_TIMESTAMP')

    user = relationship("UserModel")
    post = relationship("PostModel")
    parent_comment = relationship("CommentModel", remote_side=[id])


class LikeModel(Base):
    __tablename__ = 'likes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    target_type = Column(String(20))
    target_id = Column(Integer)
    relation_strength = Column(DECIMAL(5, 2), default=1.0)
    is_del = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(TIMESTAMP, onupdate='CURRENT_TIMESTAMP')

    user = relationship("UserModel")


class FavoriteModel(Base):
    __tablename__ = 'favorites'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    target_type = Column(String(20))
    target_id = Column(Integer)
    relation_strength = Column(DECIMAL(5, 2), default=1.0)
    is_del = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(TIMESTAMP, onupdate='CURRENT_TIMESTAMP')

    user = relationship("UserModel")