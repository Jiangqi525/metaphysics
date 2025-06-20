from sqlalchemy.orm import Session
from src.domain.fortune.entities import FortuneAnalysis
from src.domain.fortune.repositories import FortuneAnalysisRepository


class FortuneAnalysisRepositoryImpl(FortuneAnalysisRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, analysis: FortuneAnalysis) -> None:
        self.session.add(analysis)
        self.session.commit()

    def find_by_id(self, analysis_id) -> FortuneAnalysis:
        return self.session.query(FortuneAnalysis).filter(FortuneAnalysis.id == analysis_id).first()

    def find_by_user_id(self, user_id) -> list[FortuneAnalysis]:
        return self.session.query(FortuneAnalysis).filter(FortuneAnalysis.user_id == user_id).all()

    def update(self, analysis: FortuneAnalysis) -> None:
        self.session.merge(analysis)
        self.session.commit()

    def delete(self, analysis_id) -> None:
        analysis = self.find_by_id(analysis_id)
        if analysis:
            self.session.delete(analysis)
            self.session.commit()