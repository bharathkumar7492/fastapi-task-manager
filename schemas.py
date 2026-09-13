# Pydantic schemas for data validation and response structure

from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional


# TASK SCHEMAS  

# Common fields for tasks
class TaskBase(BaseModel):
    title: str
    description: str
    completed: Optional[bool]=False
        
        
class CreateTask(TaskBase):
    pass


# Schema for returning user data
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# Schema for returning task data
class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    completed: bool=False
    created_at: datetime
    owner_id: int
    owner: UserResponse 
    
    model_config = ConfigDict(from_attributes=True)
    
    
    
class TaskUpdate(BaseModel):
    completed: Optional[bool]=None




# USER SCHEMAS

class CreateUser(BaseModel):
    email: EmailStr
    password: str
    
    
# for validating login credentials
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    


# TOKEN SCHEMAS

# for JWT token response
class Token(BaseModel):
    access_token: str
    token_type: str
    
#  for storing user ID from JWT
class TokenData(BaseModel):
    id: Optional[int] = None