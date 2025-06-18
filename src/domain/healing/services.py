# src/domain/healing/services.py
from typing import List, Optional
from uuid import UUID
from src.domain.healing.entities import HealingSession, HealingPackage
from src.domain.healing.repositories import HealingSessionRepository, HealingPackageRepository
from src.domain.user.services import UserService


class HealingService:
    def __init__(self,
                 session_repository: HealingSessionRepository,
                 package_repository: HealingPackageRepository,
                 user_service: UserService):
        self.session_repo = session_repository
        self.package_repo = package_repository
        self.user_service = user_service

    def create_healing_session(self,
                               user_id: UUID,
                               session_type: str,
                               start_time: str,
                               end_time: str,
                               jewelry_ids: List[int]) -> HealingSession:
        """创建疗愈会话"""
        user = self.user_service.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found.")
        duration = (datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S") -
                    datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")).total_seconds() // 60
        session = HealingSession(
            user_id=user_id,
            session_type=session_type,
            start_time=start_time,
            end_time=end_time,
            duration=duration,
            jewelry_ids=jewelry_ids
        )
        self.session_repo.save(session)
        return session

    def get_healing_session_by_id(self, session_id: UUID) -> Optional[HealingSession]:
        """根据ID获取疗愈会话"""
        return self.session_repo.find_by_id(session_id)

    def get_healing_sessions_by_user_id(self, user_id: UUID) -> List[HealingSession]:
        """根据用户ID获取疗愈会话列表"""
        return self.session_repo.find_by_user_id(user_id)

    def start_healing_session(self, session_id: UUID) -> HealingSession:
        """开始疗愈会话"""
        session = self.get_healing_session_by_id(session_id)
        if not session:
            raise ValueError("Session not found.")
        session.start_session()
        self.session_repo.update(session)
        return session

    def complete_healing_session(self, session_id: UUID, feedback: str) -> HealingSession:
        """完成疗愈会话"""
        session = self.get_healing_session_by_id(session_id)
        if not session:
            raise ValueError("Session not found.")
        session.complete_session(feedback)
        self.session_repo.update(session)
        return session

    def cancel_healing_session(self, session_id: UUID) -> HealingSession:
        """取消疗愈会话"""
        session = self.get_healing_session_by_id(session_id)
        if not session:
            raise ValueError("Session not found.")
        session.cancel_session()
        self.session_repo.update(session)
        return session

    def create_healing_package(self,
                               name: str,
                               description: str,
                               session_types: List[str],
                               price: Money,
                               session_count: int) -> HealingPackage:
        """创建疗愈套餐"""
        package = HealingPackage(
            name=name,
            description=description,
            session_types=session_types,
            price=price,
            session_count=session_count
        )
        self.package_repo.save(package)
        return package

    def get_active_healing_packages(self) -> List[HealingPackage]:
        """获取所有活跃的疗愈套餐"""
        return self.package_repo.find_all_active()

    def deactivate_healing_package(self, package_id: UUID) -> HealingPackage:
        """停用疗愈套餐"""
        package = self.package_repo.find_by_id(package_id)
        if not package:
            raise ValueError("Package not found.")
        package.deactivate_package()
        self.package_repo.update(package)
        return package

    def activate_healing_package(self, package_id: UUID) -> HealingPackage:
        """启用疗愈套餐"""
        package = self.package_repo.find_by_id(package_id)
        if not package:
            raise ValueError("Package not found.")
        package.activate_package()
        self.package_repo.update(package)
        return package
