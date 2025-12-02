from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base, class_term_association

class Term(Base):
    __tablename__ = "term"

    id = Column(Integer, primary_key=True, autoincrement=True)
    term = Column(String(255), nullable=False, unique=True)
    translation = Column(String(255), nullable=False)

    classes = relationship(
        "Class",
        secondary=class_term_association,
        back_populates="terms",
    )

    def __repr__(self):
        return f"<Term(term={self.term!r}, translation={self.translation!r})>"