from typing import TypeVar, List, Generic
from sqlalchemy.orm import Session
from .RepositoryInterface import RepositoryInterface
from ..models.base import Base

T = TypeVar('T', bound=Base)

class BaseRepository(Generic[T], RepositoryInterface):
    def __init__(self, session: Session, model: type[T]):
        self.session = session
        self.model = model

    def get_by_id(self, id: int) -> T | None:
        """Get an entity by its ID."""
        return self.session.query(self.model).filter(self.model.id == id).first()

    def get_all(self) -> List[T]:
        """Get all entities."""
        return self.session.query(self.model).all()

    def create(self, obj: T) -> T:
        """Create a new entity."""
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def update(self, obj: T) -> T | None:
        """Update an existing entity."""
        if obj.id is None:
            return None
        existing = self.get_by_id(obj.id)
        if existing is None:
            return None
        self.session.merge(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def delete(self, obj: T) -> bool:
        """Delete an entity."""
        if obj.id is None:
            return False
        existing = self.get_by_id(obj.id)
        if existing is None:
            return False
        self.session.delete(existing)
        self.session.commit()
        return True

