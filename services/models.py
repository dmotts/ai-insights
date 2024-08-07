from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
import os

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql+psycopg2://username:password@your-instance-ip/dbname')

Base = declarative_base()

class Report(Base):
    __tablename__ = 'reports'
    id = Column(Integer, primary_key=True, index=True)
    client_name = Column(String)
    client_email = Column(String)
    industry = Column(String)
    pdf_url = Column(String)
    doc_url = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

engine = create_engine(
    DATABASE_URL,
    pool_size=3,
    max_overflow=0,
    connect_args={"options": "-c timezone=utc"}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)
