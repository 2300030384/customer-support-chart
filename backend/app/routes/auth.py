from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.models.user import UserCreate, UserLogin
from app.services.auth_service import register_user, authenticate_user, create_access_token

router = APIRouter(tags=["Auth"], prefix="/auth")

@router.post("/register")
def register(user: UserCreate):
    user_obj = register_user(user)
    return {"username": user_obj.username, "email": user_obj.email, "role": user_obj.role}

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user.username, "role": user.role})
    return {"access_token": token, "token_type": "bearer", "role": user.role}
