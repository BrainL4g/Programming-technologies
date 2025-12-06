from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.repository.user import UserCrud
from backend.src.schema.user import UserCreateVerify, UserUpdate, UserUpdatePassword
from backend.src.core.security import verify_password
from backend.src.db.models import User
from backend.src.exceptions import UserNotFound, InsufficientPrivileges

class UserService:
    async def create_user(self, db: AsyncSession, user_data: UserCreateVerify) -> User:
        return await UserCrud.create_user(user_data, db)

    async def get_user_by_email(self, db: AsyncSession, email: str) -> User:
        user = await UserCrud.get_user_by_email(email, db)
        if not user:
            raise UserNotFound()
        return user

    async def get_user_by_id(self, db: AsyncSession, user_id: int) -> User:
        user = await UserCrud.get_user_by_id(user_id, db)
        if not user:
            raise UserNotFound()
        return user

    async def get_users(self, db: AsyncSession, skip: int, limit: int) -> list[User]:
        return await UserCrud.get_users(db, skip, limit)

    async def update_user(self, db: AsyncSession, user: User, update_data: UserUpdate) -> User:
        return await UserCrud.update_user(user, update_data, db)

    async def update_password(self, db: AsyncSession, user: User, update_data: UserUpdatePassword) -> User:
        if not verify_password(update_data.password, user.hashed_password):
            raise InsufficientPrivileges()
        return await UserCrud.update_user_password(user, password=update_data.new_password, db=db)


    async def delete_user(self, db: AsyncSession, user_id: int) -> None:
        try:
            await UserCrud.delete(db, user_id)
        except ValueError:
            raise UserNotFound()


UserService = UserService()