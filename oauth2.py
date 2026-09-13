from jose import JWTError, jwt
from fastapi import Depends, status, HTTPException
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from dotenv import load_dotenv
import os

import database, schemas, models


# Load environment variables
load_dotenv()

# Configure OAuth2 bearer token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# JWT configuration

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))



# Create a JWT access token
def create_access_token(data: dict):
    # Copy data for the token
    to_encode = data.copy()
    
    # Set token expiration time    
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # Add expiration time to token
    to_encode.update({"exp": expire})
    
    # Encode and sign the JWT    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt


# Verify JWT access token
def verify_access_token(token: str, credential_exception):

    try:
        # Decode and verify the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # Get user ID from token
        id: str = payload.get("user_id")

        # Check if user ID exists
        if id is None:
            raise credential_exception

        # Store user ID in TokenData
        token_data = schemas.TokenData(id=id)

    except JWTError:
        # Handle invalid or expired token
        raise credential_exception

    return token_data



# Get the current logged-in user
def get_current_user(token: str = Depends(oauth2_scheme), db: Session=Depends(database.get_db)):
    
    # Authentication error response
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                          detail="Could not validate credentials", 
                                          headers={"WWW-Authenticate": "Bearer"})
    
    # Verify the access token    
    token = verify_access_token(token, credentials_exception)
    
    # Find the user from the token ID       
    user = db.query(models.User).filter(models.User.id == token.id).first()
    
    if user is None:
        raise credentials_exception
    
    return user