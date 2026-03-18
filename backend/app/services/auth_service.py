import bcrypt
import jwt
from datetime import datetime, timedelta
from app.models.user import User, UserCreate
from app.database.connection import get_database

SECRET_KEY = "your_secret_key_here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def register_user(user_data: UserCreate):
    db = get_database()
    hashed = hash_password(user_data.password)
    user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed,
        role=user_data.role,
        is_active=True
    )
    db["users"].insert_one(user.dict(by_alias=True, exclude_none=True))
    return user

def authenticate_user(username: str, password: str):
    db = get_database()
    user_doc = db["users"].find_one({"username": username})
    if not user_doc:
        return None
    user = User(**user_doc)
    if not verify_password(password, user.hashed_password):
        return None
    return user
