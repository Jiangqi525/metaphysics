# src/domain/compliance/repositories.py
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from src.domain.compliance.entities import ComplianceCheck, CompliancePolicy


class ComplianceCheckRepository(ABC):
    """合规检查存储库接口"""

    @abstractmethod
    def save(self, check: ComplianceCheck) -> None:
        """保存合规检查信息"""
        pass

    @abstractmethod
    def find_by_id(self, check_id: UUID) -> Optional[ComplianceCheck]:
        """根据ID查找合规检查信息"""
        pass

    @abstractmethod
    def find_all(self) -> List[ComplianceCheck]:
        """查找所有合规检查信息"""
        pass

    @abstractmethod
    def update(self, check: ComplianceCheck) -> None:
        """更新合规检查信息"""
        pass


class CompliancePolicyRepository(ABC):
    """合规政策存储库接口"""

    @abstractmethod
    def save(self, policy: CompliancePolicy) -> None:
        """保存合规政策信息"""
        pass

    @abstractmethod
    def find_by_id(self, policy_id: UUID) -> Optional[CompliancePolicy]:
        """根据ID查找合规政策信息"""
        pass

    @abstractmethod
    def find_all_active(self) -> List[CompliancePolicy]:
        """查找所有活跃的合规政策信息"""
        pass

    @abstractmethod
    def update(self, policy: CompliancePolicy) -> None:
        """更新合规政策信息"""
        pass
