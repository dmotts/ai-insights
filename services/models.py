from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import Config

Base = declarative_base()

class Report(Base):
    __tablename__ = 'reports'

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_name = Column(String, nullable=False)
    client_email = Column(String, nullable=False)
    industry = Column(String, nullable=False)
    pdf_url = Column(String, nullable=False)
    doc_url = Column(String, nullable=False)

# Create the database engine using the SQLALCHEMY_DATABASE_URI from the config
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)

# Create tables if they don't exist
Base.metadata.create_all(engine)
