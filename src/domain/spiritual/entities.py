# src/domain/spiritual/entities.py
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from uuid import UUID
from src.domain.core.entities import AggregateRoot
from src.domain.core.value_objects import Money


@dataclass
class SpiritualTransaction:
    user_id: UUID
    transaction_type: str  # recharge, consume, reward, transfer
    amount: int
    source_type: str  # payment, post, healing, divination, referral
    source_id: int = None
    transaction_time: str = field(default_factory=lambda: str(datetime.datetime.now()))
    description: str = None

    def to_dict(self) -> Dict:
        return {
            "user_id": str(self.user_id),
            "transaction_type": self.transaction_type,
            "amount": self.amount,
            "source_type": self.source_type,
            "source_id": self.source_id,
            "transaction_time": self.transaction_time,
            "description": self.description
        }


@dataclass
class SpiritualAccount(AggregateRoot):
    user_id: UUID
    balance: int = 0
    transaction_history: List[SpiritualTransaction] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: str(datetime.datetime.now()))

    def recharge(self, amount: int, source_type: str, source_id: int = None,
                 description: str = None) -> SpiritualTransaction:
        if amount <= 0:
            raise ValueError("Recharge amount must be positive")

        transaction = SpiritualTransaction(
            user_id=self.user_id,
            transaction_type="recharge",
            amount=amount,
            source_type=source_type,
            source_id=source_id,
            description=description
        )

        self.balance += amount
        self.transaction_history.append(transaction)
        self.updated_at = str(datetime.datetime.now())
        return transaction

    def consume(self, amount: int, source_type: str, source_id: int = None,
                description: str = None) -> SpiritualTransaction:
        if amount <= 0:
            raise ValueError("Consume amount must be positive")
        if self.balance < amount:
            raise ValueError("Insufficient balance")

        transaction = SpiritualTransaction(
            user_id=self.user_id,
            transaction_type="consume",
            amount=amount,
            source_type=source_type,
            source_id=source_id,
            description=description
        )

        self.balance -= amount
        self.transaction_history.append(transaction)
        self.updated_at = str(datetime.datetime.now())
        return transaction

    def transfer(self, to_user_id: UUID, amount: int, description: str = None) -> SpiritualTransaction:
        if amount <= 0:
            raise ValueError("Transfer amount must be positive")
        if self.balance < amount:
            raise ValueError("Insufficient balance")

        transaction = SpiritualTransaction(
            user_id=self.user_id,
            transaction_type="transfer",
            amount=amount,
            source_type="transfer",
            description=description
        )

        self.balance -= amount
        self.transaction_history.append(transaction)
        self.updated_at = str(datetime.datetime.now())
        return transaction