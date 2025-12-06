from typing import Optional

from pydantic import (BaseModel, ConfigDict, EmailStr, model_validator)
from src.exceptions import PasswordsDoNotMatch


def validate_password(password: str):
    # re_for_pw: re.Pattern[str] = re.compile(r"[A-Za-z0-9\d@$!%*#?&]{8,16}$")
    # if not re_for_pw.match(password):
    #     raise ValueError("Not acceptable password")
    return password


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    confirm_password: str
    username: str = None

    @model_validator(mode="after")
    def pass_validation(self):
        password = validate_password(self.password)
        confirm_password = self.confirm_password
        if password != confirm_password:
            raise PasswordsDoNotMatch()
        return self


class UserCreateVerify(UserCreate):
    code: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None


class UserUpdatePassword(BaseModel):
    password: Optional[str]
    new_password: Optional[str]
    confirm_new_password: Optional[str]

    @model_validator(mode="after")
    def pass_validation(self):
        confirm_new_password = self.confirm_new_password
        new_password = validate_password(self.new_password)
        if new_password != confirm_new_password:
            raise PasswordsDoNotMatch()
        return self


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserPasswordReset(BaseModel):
    email: str
    code: str
    new_password: str
    confirm_new_password: str

    @model_validator(mode="after")
    def pass_validation(self):
        confirm_new_password = self.confirm_new_password
        new_password = validate_password(self.new_password)
        if new_password != confirm_new_password:
            raise PasswordsDoNotMatch()
        return self


class UserResponse(BaseModel):
    id: int
    email: EmailStr = None
    username: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)
