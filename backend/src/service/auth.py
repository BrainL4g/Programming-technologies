from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.security import (create_access_token,
                               generate_random_code, verify_password)
from src.db.models import User
from src.db.redis_client.service import redis_service
from src.exceptions import (InvalidCredentials, ResetCodeInvalid, UserAlreadyExists,
                            UserNotFound)
from src.repository.user import UserCrud
from src.schema.user import (UserCreate, UserPasswordReset)
from src.utils.celery_tasks import send_password_reset_email


class AuthService:
    async def login(
            self, form_data: OAuth2PasswordRequestForm, session: AsyncSession
    ) -> str:
        user = await UserCrud.get_user_by_email(email=form_data.username, db=session)
        if user and verify_password(form_data.password, user.password):
            access_token = create_access_token(subject=user.id)
            return access_token
        raise InvalidCredentials()

    async def logout(self, token: str) -> None:
        await redis_service.blacklist_token(access_token=token)

    async def register(self, user_create: UserCreate, session: AsyncSession) -> User:
        user = await UserCrud.get_user_by_email(email=user_create.email, db=session)
        if user:
            raise UserAlreadyExists()
        return await UserCrud.create_user(user_create=user_create, db=session)

    async def reset_password(self, email: str, session: AsyncSession) -> None:
        user = await UserCrud.get_user_by_email(email=email, db=session)
        if not user:
            raise UserNotFound()
        reset_code = await redis_service.create_reset_code(
            email=user.email, code=generate_random_code()
        )
        send_password_reset_email.delay(recipient=email, code=reset_code)

    async def confirm_password_reset(
            self, user_reset: UserPasswordReset, session: AsyncSession
    ) -> None:
        user = await UserCrud.get_user_by_email(email=user_reset.email, db=session)
        if not user:
            raise UserNotFound()
        stored_code = await redis_service.get_reset_code(email=user_reset.email)
        if not stored_code or stored_code != user_reset.code:
            raise ResetCodeInvalid()
        await UserCrud.update_user_password(
            user=user, password=user_reset.new_password, db=session
        )
        await redis_service.delete_reset_code(user.email)


AuthService = AuthService()
