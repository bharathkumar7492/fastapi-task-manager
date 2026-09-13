from database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import Relationship


# User database model
class User(Base):
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    
    
# Task database model
class Task(Base):
    
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    completed = Column(Boolean, server_default=text("False"), nullable=False)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), nullable=False)
    
    # Store the user ID and link it to the users table - FOREIGN KEY
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    # Define relationship with User model
    owner = Relationship("User")