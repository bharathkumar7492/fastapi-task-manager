# Import CryptContext for password hashing
from passlib.context import CryptContext


# Configure bcrypt password hashing
pwd_context = CryptContext(schemes=["bcrypt"],  # Use bcrypt to hash passwords
                           deprecated="auto")   # Automatically handle old hashing schemes


# Hash the password
def hash(password: str):
    return pwd_context.hash(password)

# Verify the password
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)