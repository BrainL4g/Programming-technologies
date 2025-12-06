import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from backend.src.core.security import get_password_hash
from backend.src.db.models import User
from backend.src.schema.user import UserCreateVerify, UserUpdate, UserUpdatePassword

class UserCRUDRepository():
    async def create_user(self, user_create: UserCreateVerify, db: AsyncSession) -> User:
        user = User(email=user_create.email, password=get_password_hash(user_create.password), username=user_create.username)
        db.add(user)
        await db.commit()
        return user

    async def get_user_by_email(self, email: str , db: AsyncSession) -> User:
        stmt = sqlalchemy.select(User).where(User.email == email)
        query = await db.execute(statement=stmt)
        return query.scalar_one_or_none()

    async def get_user_by_id(self, user_id: int, db: AsyncSession) -> User:
        stmt = sqlalchemy.select(User).where(User.id == user_id)
        query = await db.execute(statement=stmt)
        return query.scalar_one_or_none()

    async def get_users(self, db: AsyncSession, skip: int, limit: int):
        stmt = sqlalchemy.select(User).offset(skip).limit(limit)
        query = await db.execute(statement=stmt)
        return query.scalars().all()

    async def update_user(self, user: User, user_update: UserUpdate, db: AsyncSession) -> User:
        user_data = user_update.model_dump(exclude_unset=True)
        for k, v in user_data.items():
            setattr(user, k, v)
        await db.commit()
        return user

    async def update_user_password(self, user: User, password: str, db: AsyncSession) -> User:
        setattr(user, "hashed_password", get_password_hash(password))
        await db.commit()
        return user

    async def delete(self, db: AsyncSession, user_id: int) -> None:
        stmt = sqlalchemy.select(User).where(User.id == user_id)
        query = await db.execute(statement=stmt)
        user = query.scalar_one_or_none()

        if user is None:
            raise ValueError(f"User with id {user_id} does not exist.")
        stmt = sqlalchemy.delete(User).where(User.id == user_id)
        await db.execute(statement=stmt)
        await db.commit()

UserCrud = UserCRUDRepository()