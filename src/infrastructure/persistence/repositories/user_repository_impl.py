from sqlalchemy.orm import Session
from src.domain.user.entities import User
from src.domain.user.repositories import UserRepository


class UserRepositoryImpl(UserRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, user: User) -> None:
        self.session.add(user)
        self.session.commit()

    def find_by_id(self, user_id) -> User:
        return self.session.query(User).filter(User.id == user_id).first()

    def find_by_username(self, username: str) -> User:
        return self.session.query(User).filter(User.username == username).first()

    def find_by_email(self, email: str) -> User:
        return self.session.query(User).filter(User.email == email).first()

    def update(self, user: User) -> None:
        self.session.merge(user)
        self.session.commit()

    def delete(self, user_id) -> None:
        user = self.find_by_id(user_id)
        if user:
            self.session.delete(user)
            self.session.commit()