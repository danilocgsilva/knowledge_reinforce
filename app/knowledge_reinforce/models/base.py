from sqlalchemy import Column, Integer, Table, ForeignKey
from database import DeclarativeBase

class Base(DeclarativeBase):
    pass

class_term_association = Table(
    "class_term_association",
    Base.metadata,
    Column("term_id", Integer, ForeignKey("term.id"), primary_key=True),
    Column("class_id", Integer, ForeignKey("class.id"), primary_key=True),
)