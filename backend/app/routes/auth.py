import jwt
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from app.config import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()

# Simulated user data
users_db = {
    "admin": {
        "username": "admin",
        "password": "adminpassword",  # In production, use hashed passwords
    }
}


# JWT Token Generation
def create_access_token(data: dict):
    expiration = timedelta(hours=1)
    to_encode = data.copy()
    to_encode.update({"exp": datetime.utcnow() + expiration})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# Auth endpoint
@router.post("/token")
def login_for_access_token(form_data: OAuth2PasswordBearer):
    user = users_db.get(form_data.username)
    if not user or user['password'] != form_data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(data={"sub": form_data.username})
    return {"access_token": token, "token_type": "bearer"}


# Protected route
@router.get("/admin")
def read_admin(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Token invalid")

    return {"message": "Welcome Admin"}
from datetime import datetime, timedelta
import jwt
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from app.config import SECRET_KEY, ALGORITHM
from pydantic import BaseModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Example model for token creation
class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str

def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=1)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict, expires_delta: timedelta = timedelta(days=7)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Token is invalid")

# Token route
def generate_tokens(user_data: dict):
    access_token = create_access_token(user_data)
    refresh_token = create_refresh_token(user_data)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
from fastapi import APIRouter, Depends, HTTPException
from app.auth import generate_tokens, verify_token
from app.config import SECRET_KEY, ALGORITHM

router = APIRouter()

# Token Refresh Endpoint
@router.post("/refresh")
def refresh_token(refresh_token: str):
    user_data = verify_token(refresh_token)
    new_tokens = generate_tokens(user_data)
    return new_tokens


from fastapi import APIRouter, HTTPException
from app.auth import generate_tokens
from app.config import SECRET_KEY
import bcrypt

router = APIRouter()


# Admin Login Route
@router.post("/token")
def login(username: str, password: str):
    if username != "admin":
        raise HTTPException(status_code=400, detail="Invalid username")

    # Hash the password (for security) and check against stored hash
    stored_password_hash = "$2b$12$8GmO5UqO52vGRLCKZd8FEe3qz0w1i/.ePb9Wom0uRnsrWppcGe1ii"  # Example hash for 'admin'
    if not bcrypt.checkpw(password.encode('utf-8'), stored_password_hash.encode('utf-8')):
        raise HTTPException(status_code=400, detail="Invalid password")

    user_data = {"sub": username}
    tokens = generate_tokens(user_data)
    return tokens
def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=1)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire, "role": data.get("role", "user")})  # Include role in payload
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=1)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire, "role": data.get("role", "student")})  # Default role is 'student'
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

import bcrypt
from fastapi import HTTPException

def hash_password(password: str) -> str:
    """Hashes the password using bcrypt"""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies the password by comparing the hashed password"""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_user(email: str, password: str):
    hashed_password = hash_password(password)
    # Store the hashed password in Firestore
    # Example: firestore.collection('users').add({'email': email, 'password': hashed_password})
