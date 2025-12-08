from typing import List
from sqlalchemy.orm import Session
from ..repositories.base_repository import BaseRepository
from ..models.term import Term

class TermRepository(BaseRepository[Term]):
    def __init__(self, session: Session):
        super().__init__(session, Term)

    def get_by_term(self, term: str) -> Term | None:
        """Get a term by its term value."""
        return self.session.query(Term).filter(Term.term == term).first()

    def get_by_translation(self, translation: str) -> List[Term]:
        """Get all terms with a specific translation."""
        return self.session.query(Term).filter(Term.translation == translation).all()

    def get_all(self) -> List[Term]:
        """Get all terms."""
        return super().get_all()


