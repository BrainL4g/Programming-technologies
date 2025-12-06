from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from src.api.dependecies.database import get_db_session
from src.api.dependecies.user import oauth2_scheme
from src.schema.auth import Message, Token
from src.schema.user import UserCreate, UserPasswordReset, UserResponse
from src.service.auth import AuthService

router = APIRouter(prefix="", tags=["auth"])


@router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session=Depends(get_db_session),
):
    access_token = await AuthService.login(form_data, session)
    return Token(access_token=access_token, token_type="bearer")


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(token=Depends(oauth2_scheme)):
    await AuthService.logout(token)


@router.post(
    "/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse
)
async def register(user_create: UserCreate, session=Depends(get_db_session)):
    return await AuthService.register(user_create, session)


@router.post("/password-reset", response_model=Message, status_code=status.HTTP_200_OK)
async def reset_password(email: str, session=Depends(get_db_session)) -> Message:
    await AuthService.reset_password(email, session)
    return Message(message="Password recovery email sent")


@router.post(
    "/password-reset/verify", response_model=Message, status_code=status.HTTP_200_OK
)
async def confirm_password_reset(
    user_reset: UserPasswordReset, session=Depends(get_db_session)
) -> Message:
    await AuthService.confirm_password_reset(user_reset, session)
    return Message(message="Password reset successful")
