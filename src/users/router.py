from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from core.schemas import Token

from .auth import CurrentUser, create_access_token, hash_password, verify_password
from .models import User
from .schemas import LoginUser, RegisterUser, UserResponse
from .service import get_user_by_email, get_user_by_username

router = APIRouter()


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def register(user: RegisterUser, db: Annotated[AsyncSession, Depends(get_db)]):
    username_exists = await get_user_by_username(db, user.username)
    if username_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
        )

    email_exists = await get_user_by_email(db, user.email)
    if email_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists",
        )

    new_user = User(
        username=user.username,
        email=user.email.lower(),
        password=hash_password(user.password),
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user


@router.post("/login", response_model=Token)
async def login(user: LoginUser, db: Annotated[AsyncSession, Depends(get_db)]):
    db_user = await get_user_by_email(db, user.email)
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": str(db_user.id)})
    return Token(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=UserResponse)
async def get_current_user(current_user: CurrentUser):
    return current_user
