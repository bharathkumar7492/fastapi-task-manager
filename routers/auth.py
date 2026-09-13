from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

# Import OAuth2 form to receive username and password from the login form
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

import database, models, utils, oauth2



# Create a router for authentication-related endpoints
router = APIRouter(tags=["Authentication"])


# Login user and generate JWT access token
@router.post("/login")
def login(user_credentials: OAuth2PasswordRequestForm=Depends(), db: Session=Depends(database.get_db)):
    
    # Find the user by email
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    
    # Check if user exists
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Invalid Credentials")
    
    # Verify the entered password with the hashed password
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Invalid Credentials")
    
    # Create JWT access token for the logged-in user
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    
    return {"access_token": access_token, "token_type": "bearer"}


