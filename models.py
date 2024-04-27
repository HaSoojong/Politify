# models.py
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import JSON  # Import JSON type specific to PostgreSQL

Base = declarative_base()

class Trend(Base):
    __tablename__ = 'trends'
    
    id = Column(Integer, primary_key=True, index=True)
    keyword = Column(String, index=True)
    top1 = Column(JSON)
    top2 = Column(JSON)
    top3 = Column(JSON)
    top4 = Column(JSON)
    top5 = Column(JSON)