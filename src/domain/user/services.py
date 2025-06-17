# src/domain/user/services.py
from typing import Optional
from uuid import UUID
from src.domain.user.entities import User
from src.domain.core.exceptions import EntityNotFound
from src.domain.user.repositories import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def register_user(self, username: str, email: str, password_hash: str, salt: str, birthdate: str) -> User:
        # 检查用户名和邮箱是否已存在
        if self.user_repository.find_by_username(username):
            raise ValueError("Username already exists")
        if self.user_repository.find_by_email(email):
            raise ValueError("Email already exists")

        # 创建新用户
        user = User(
            username=username,
            email=email,
            password_hash=password_hash,
            salt=salt,
            birthdate=birthdate
        )

        # 保存到存储库
        self.user_repository.save(user)
        return user

    def authenticate_user(self, username: str, password_hash: str) -> Optional[User]:
        user = self.user_repository.find_by_username(username)
        if not user:
            return None
        if user.password_hash != password_hash:
            return None
        return user

    def get_user_by_id(self, user_id: UUID) -> User:
        user = self.user_repository.find_by_id(user_id)
        if not user:
            raise EntityNotFound("User", str(user_id))
        return user

    def update_user_profile(self, user_id: UUID, profile_data: dict) -> User:
        user = self.get_user_by_id(user_id)

        # 更新用户资料
        from src.domain.user.entities import UserProfile
        profile = UserProfile(
            zodiac_id=profile_data.get("zodiac_id"),
            chinese_zodiac_id=profile_data.get("chinese_zodiac_id"),
            birth_time=profile_data.get("birth_time"),
            birth_location=profile_data.get("birth_location", {}),
            constellation_element=profile_data.get("constellation_element"),
            character_traits=profile_data.get("character_traits", []),
            fortune_preferences=profile_data.get("fortune_preferences", []),
            jewelry_style_preferences=profile_data.get("jewelry_style_preferences", []),
            wuxing_attribute=profile_data.get("wuxing_attribute"),
            emotion_tags=profile_data.get("emotion_tags", [])
        )

        user.update_profile(profile)
        self.user_repository.save(user)
        return user

    def add_spiritual_power(self, user_id: UUID, amount: int) -> User:
        user = self.get_user_by_id(user_id)
        user.add_spiritual_power(amount)
        self.user_repository.save(user)
        return user

    def consume_spiritual_power(self, user_id: UUID, amount: int) -> User:
        user = self.get_user_by_id(user_id)
        user.consume_spiritual_power(amount)
        self.user_repository.save(user)
        return user
