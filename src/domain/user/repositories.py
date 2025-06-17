# src/domain/user/repositories.py
from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID
from src.domain.user.entities import User


class UserRepository(ABC):
    """用户存储库接口"""

    @abstractmethod
    def save(self, user: User) -> None:
        """保存用户"""
        pass

    @abstractmethod
    def find_by_id(self, user_id: UUID) -> Optional[User]:
        """根据ID查找用户"""
        pass

    @abstractmethod
    def find_by_username(self, username: str) -> Optional[User]:
        """根据用户名查找用户"""
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]:
        """根据邮箱查找用户"""
        pass

    @abstractmethod
    def update(self, user: User) -> None:
        """更新用户"""
        pass

    @abstractmethod
    def delete(self, user_id: UUID) -> None:
        """删除用户"""
        pass
