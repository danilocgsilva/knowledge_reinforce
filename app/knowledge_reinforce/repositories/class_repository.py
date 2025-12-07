from typing import List
from sqlalchemy.orm import Session
from ..repositories.base_repository import BaseRepository
from ..models.class_model import Class

class ClassRepository(BaseRepository[Class]):
    def __init__(self, session: Session):
        super().__init__(session, Class)

    def get_by_class_name(self, class_name: str) -> Class | None:
        """Get a class by its name."""
        return self.session.query(Class).filter(Class.class_name == class_name).first()

    def get_all(self) -> List[Class]:
        """Get all classes."""
        return super().get_all()

