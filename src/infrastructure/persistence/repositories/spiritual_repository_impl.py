from sqlalchemy.orm import Session
from src.domain.spiritual.entities import SpiritualAccount, SpiritualTransaction


class SpiritualRepositoryImpl:
    def __init__(self, session: Session):
        self.session = session

    def save_account(self, account: SpiritualAccount) -> None:
        self.session.add(account)
        self.session.commit()

    def find_account_by_user_id(self, user_id) -> SpiritualAccount:
        return self.session.query(SpiritualAccount).filter(SpiritualAccount.user_id == user_id).first()

    def update_account(self, account: SpiritualAccount) -> None:
        self.session.merge(account)
        self.session.commit()

    def save_transaction(self, transaction: SpiritualTransaction) -> None:
        self.session.add(transaction)
        self.session.commit()