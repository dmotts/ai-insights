from sqlalchemy import Column, Integer, String, create_engine, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging
from config import Config

Base = declarative_base()

class Report(Base):
    __tablename__ = 'reports'

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_name = Column(String(100), nullable=False)
    client_email = Column(String(150), nullable=False, unique=True)
    industry = Column(String(100), nullable=False)
    pdf_url = Column(String(255), nullable=False, unique=True)
    doc_url = Column(String(255), nullable=False, unique=True)

    __table_args__ = (
        Index('idx_client_email', 'client_email'),
        Index('idx_industry', 'industry'),
    )

# Initialize logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create the database engine using the SQLALCHEMY_DATABASE_URI from the config
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)

# Create tables if they don't exist
try:
    Base.metadata.create_all(engine)
    logger.info('Database tables created successfully or already exist.')
except Exception as e:
    logger.error(f'Error creating database tables: {e}')
