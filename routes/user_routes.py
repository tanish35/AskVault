from middleware.auth import check_auth
from fastapi import APIRouter, Depends, HTTPException, status, Response
from lib.config import settings
from engine import db
from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

router = APIRouter()
SECRET_KEY = settings.secret_key
ALGORITHM = "HS256"


@router.post("/signup")
async def signup(email: str, password: str, name: str):
    if not email or not password or not name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email,password and Name are required",
        )

    existing_user = await db.user.find_unique(where={"email": email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists"
        )

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    password = pwd_context.hash(password)
    user = await db.user.create(
        data={"email": email, "password": password, "name": name}
    )
    return {"message": "User created successfully", "user_id": user.id}


@router.post("/login")
async def login(email: str, password: str, response: Response):
    if not email or not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email and password are required",
        )

    user = await db.user.find_unique(where={"email": email})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    if not pwd_context.verify(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    token_payload = {
        "sub": user.id,
        "exp": datetime.now() + timedelta(days=30),
    }
    access_token = jwt.encode(token_payload, SECRET_KEY, algorithm=ALGORITHM)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=30 * 24 * 60 * 60,
    )

    return {"message": "Login successful", "user_id": user.id}


@router.get("/me")
async def get_current_user(current_user=Depends(check_auth)):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )
    user = await db.user.find_unique(where={"id": current_user.id})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return {"id": user.id, "email": user.email, "name": user.name}
