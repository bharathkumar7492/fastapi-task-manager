from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

import schemas, models, database, utils


# Create a router for user-related endpoints
router = APIRouter(prefix="/users", tags= ["Users"])


# CREATE USER    

# Create a new user
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.CreateUser, db: Session=Depends(database.get_db)):
    
    # Hash the user's password before storing it
    user.password = utils.hash(user.password)
    # Create a new user object
    new_user = models.User(**user.dict())
    
    # Add user to database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user
    
# GET USER

# Get a user by ID
@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session=Depends(database.get_db)):
    # Find the user by ID
    user = db.query(models.User).filter(models.User.id == id).first()
    
    # Check if the user exists
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id:  {id} does not exist")
    
    
    return user


