from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from backend.src.api.dependecies.database import get_db_session
from backend.src.core.security import verify_token
from backend.src.repository.user import UserCrud
from backend.src.db.models import User
from backend.src.exceptions import UserNotFound, InsufficientPrivileges

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

async def get_current_user(session=Depends(get_db_session), token=Depends(oauth2_scheme)) -> User:
    id = await verify_token(token)
    user = await UserCrud.get_user_by_id(user_id=int(id), db=session)
    if not user:
        raise UserNotFound()
    return user

async def get_current_active_superuser(user=Depends(get_current_user)) -> User:
    if not user.is_superuser:
        raise InsufficientPrivileges()
    return user