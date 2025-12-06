from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.dependecies.database import get_db_session
from src.api.dependecies.user import (get_current_active_superuser,
                                      get_current_user)
from src.schema.user import (UserResponse,
                             UserUpdate, UserUpdatePassword)
from src.service.user import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[UserResponse])
async def get_users(
        skip: int = 0,
        limit: int = 10,
        db: AsyncSession = Depends(get_db_session),
        admin=Depends(get_current_active_superuser),
):
    return await UserService.get_users(db, skip, limit)


@router.get("/me", response_model=UserResponse)
async def get_current_user_data(current_user=Depends(get_current_user)):
    return current_user


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db_session)):
    return await UserService.get_user_by_id(db, user_id)


@router.patch("/me", response_model=UserResponse)
async def update_me_user(
        update_data: UserUpdate,
        db: AsyncSession = Depends(get_db_session),
        current_user=Depends(get_current_user),
):
    return await UserService.update_user(db, current_user, update_data)


@router.patch("/me/password", response_model=UserResponse)
async def update_me_password(
        update_data: UserUpdatePassword,
        db: AsyncSession = Depends(get_db_session),
        current_user=Depends(get_current_user),
):
    return await UserService.update_password(db, current_user, update_data)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
        user_id: int,
        db: AsyncSession = Depends(get_db_session),
        admin=Depends(get_current_active_superuser),
):
    await UserService.delete_user(db, user_id)
