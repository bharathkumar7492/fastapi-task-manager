# Import SQLAlchemy tools for database connection and sessions
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Load environment variables from .env
from dotenv import load_dotenv
import os



# Load environment variables from .env
load_dotenv()

# Get database URL from environment variables
SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")


# Create database engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)


# Create database session factory
SessionLocal = sessionmaker(
                            autocommit=False, 
                            autoflush=False,       
                            bind=engine            
                            )

# Create base class for database models
Base = declarative_base()


# Create a database session for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
