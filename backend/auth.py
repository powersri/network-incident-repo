# auth.py - Authentication and Authorization logic for the Network Incidents API
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext

# Local imports for database and models
from database import users_collection
from jwt_utils import create_access_token, decode_access_token
from models import TokenResponse, UserRegister
from jose import JWTError

# Initialize the authentication router
router = APIRouter(tags=["Authentication"])

# Password hashing context using Argon2 algorithm
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
# OAuth2 scheme for token-based authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

# Helper functions for password hashing, verification, and user authentication
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Verify a plain password against its hashed version
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Authenticate user by verifying username and password against the database
def authenticate_user(username: str, password: str):
    user = users_collection.find_one({"username": username})
    if not user:
        return None

    if not verify_password(password, user["password_hash"]):
        return None

    return user

# Dependency to get the current user from the access token
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_access_token(token)
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = users_collection.find_one({"username": username})
    if not user:
        raise credentials_exception

    return {
        "username": user["username"],
        "role": user.get("role", "engineer")
    }


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user: UserRegister):
    existing_user = users_collection.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )

    new_user = {
        "username": user.username,
        "password_hash": get_password_hash(user.password),
        "role": "engineer"
    }

    users_collection.insert_one(new_user)

    return {"message": "User registered successfully"}


@router.post("/token", response_model=TokenResponse)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user["username"]})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }