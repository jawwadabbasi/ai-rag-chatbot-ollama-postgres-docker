from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, func
from pgvector.sqlalchemy import Vector

Base = declarative_base()

class Documents(Base):

    __tablename__ = "documents"
    # __table_args__ = {"schema": "alfred"}

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    embedding = Column(Vector(768))
    date = Column(DateTime, server_default=func.now())