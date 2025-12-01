from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from database import DeclarativeBase

class Base(DeclarativeBase):
    pass

class_term_association = Table(
    "class_term_association",
    Base.metadata,
    Column("term_id", Integer, ForeignKey("term.id"), primary_key=True),
    Column("class_id", Integer, ForeignKey("class.id"), primary_key=True),
)

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
