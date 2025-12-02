from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base, class_term_association

class Class(Base):
    __tablename__ = "class"

    id = Column(Integer, primary_key=True, autoincrement=True)
    class_name = Column("class", String(255), nullable=False, unique=True)

    terms = relationship(
        "Term",
        secondary=class_term_association,
        back_populates="classes",
    )

    def __repr__(self):
        return f"<Class(class={self.class_name!r})>"