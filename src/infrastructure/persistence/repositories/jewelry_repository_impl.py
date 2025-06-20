from sqlalchemy.orm import Session
from src.domain.compliance.entities import ComplianceCheck, CompliancePolicy
from src.domain.compliance.repositories import ComplianceCheckRepository, CompliancePolicyRepository


class ComplianceCheckRepositoryImpl(ComplianceCheckRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, check: ComplianceCheck) -> None:
        self.session.add(check)
        self.session.commit()

    def find_by_id(self, check_id) -> ComplianceCheck:
        return self.session.query(ComplianceCheck).filter(ComplianceCheck.id == check_id).first()

    def find_all(self) -> list[ComplianceCheck]:
        return self.session.query(ComplianceCheck).all()

    def update(self, check: ComplianceCheck) -> None:
        self.session.merge(check)
        self.session.commit()


class CompliancePolicyRepositoryImpl(CompliancePolicyRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, policy: CompliancePolicy) -> None:
        self.session.add(policy)
        self.session.commit()

    def find_by_id(self, policy_id) -> CompliancePolicy:
        return self.session.query(CompliancePolicy).filter(CompliancePolicy.id == policy_id).first()

    def find_all_active(self) -> list[CompliancePolicy]:
        return self.session.query(CompliancePolicy).filter(CompliancePolicy.is_active == True).all()

    def update(self, policy: CompliancePolicy) -> None:
        self.session.merge(policy)
        self.session.commit()