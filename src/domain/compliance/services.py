# src/domain/compliance/services.py
from typing import List, Optional
from uuid import UUID
from src.domain.compliance.entities import ComplianceCheck, CompliancePolicy
from src.domain.compliance.repositories import ComplianceCheckRepository, CompliancePolicyRepository


class ComplianceService:
    def __init__(self,
                 check_repository: ComplianceCheckRepository,
                 policy_repository: CompliancePolicyRepository):
        self.check_repo = check_repository
        self.policy_repo = policy_repository

    def create_compliance_check(self, check_name: str, check_type: str) -> ComplianceCheck:
        """创建合规检查"""
        check = ComplianceCheck(check_name=check_name, check_type=check_type)
        self.check_repo.save(check)
        return check

    def get_compliance_check_by_id(self, check_id: UUID) -> Optional[ComplianceCheck]:
        """根据ID获取合规检查"""
        return self.check_repo.find_by_id(check_id)

    def get_all_compliance_checks(self) -> List[ComplianceCheck]:
        """获取所有合规检查"""
        return self.check_repo.find_all()

    def start_compliance_check(self, check_id: UUID) -> ComplianceCheck:
        """开始合规检查"""
        check = self.get_compliance_check_by_id(check_id)
        if not check:
            raise ValueError("Compliance check not found.")
        check.start_check()
        self.check_repo.update(check)
        return check

    def complete_compliance_check(self, check_id: UUID, result: str, details: str) -> ComplianceCheck:
        """完成合规检查"""
        check = self.get_compliance_check_by_id(check_id)
        if not check:
            raise ValueError("Compliance check not found.")
        check.complete_check(result, details)
        self.check_repo.update(check)
        return check

    def fail_compliance_check(self, check_id: UUID, details: str) -> ComplianceCheck:
        """使合规检查失败"""
        check = self.get_compliance_check_by_id(check_id)
        if not check:
            raise ValueError("Compliance check not found.")
        check.fail_check(details)
        self.check_repo.update(check)
        return check

    def create_compliance_policy(self, policy_name: str, policy_description: str, policy_type: str) -> CompliancePolicy:
        """创建合规政策"""
        policy = CompliancePolicy(policy_name=policy_name, policy_description=policy_description,
                                  policy_type=policy_type)
        self.policy_repo.save(policy)
        return policy

    def get_active_compliance_policies(self) -> List[CompliancePolicy]:
        """获取所有活跃的合规政策"""
        return self.policy_repo.find_all_active()

    def deactivate_compliance_policy(self, policy_id: UUID) -> CompliancePolicy:
        """停用合规政策"""
        policy = self.policy_repo.find_by_id(policy_id)
        if not policy:
            raise ValueError("Compliance policy not found.")
        policy.deactivate_policy()
        self.policy_repo.update(policy)
        return policy

    def activate_compliance_policy(self, policy_id: UUID) -> CompliancePolicy:
        """启用合规政策"""
        policy = self.policy_repo.find_by_id(policy_id)
        if not policy:
            raise ValueError("Compliance policy not found.")
        policy.activate_policy()
        self.policy_repo.update(policy)
        return policy
