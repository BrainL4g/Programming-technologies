from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from src.api.dependecies.database import get_db_session
from src.core.security import verify_token
from src.crud.user import user_crud
from src.db.models import User
from src.exceptions import UserNotFound, InactiveUser, InsufficientPrivileges

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

async def get_current_user(session=Depends(get_db_session), token=Depends(oauth2_scheme)) -> User:
    id = await verify_token(token)
    user = await user_crud.get_user_by_id(user_id=int(id), db=session)
    if not user:
        raise UserNotFound()
    if not user.is_active:
        raise InactiveUser()
    return user

async def get_current_active_superuser(user=Depends(get_current_user)) -> User:
    if not user.is_superuser:
        raise InsufficientPrivileges()
    return user