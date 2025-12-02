from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class AuthException(Exception):
    """Base class for authentication and authorization errors."""
    pass

class InvalidToken(AuthException):
    """Raised when a token is invalid."""
    pass

class TokenExpired(AuthException):
    """Raised when a token is expired."""
    pass

class InvalidCredentials(AuthException):
    """Raised when the credentials are incorrect."""
    pass

class UserAlreadyExists(AuthException):
    """Raised when trying to register with an existing email."""
    pass

class PasswordsDoNotMatch(AuthException):
    """Raised when password and confirm_password do not match."""
    pass

class UserException(Exception):
    """Base class for user-related exceptions."""
    pass

class UserNotFound(UserException):
    """Raised when a user is not found."""
    pass

class ResetCodeInvalid(AuthException):
    """Raised when a password reset code is invalid or expired."""
    pass

class InsufficientPrivileges(AuthException):
    """Raised when user lacks admin/superuser rights."""
    pass

class FileNotFound(Exception):
    """Base class for file upload exceptions."""
    pass

def _create_handler(status_code: int, detail: dict):
    async def handler(request: Request, exc: Exception):
        return JSONResponse(status_code=status_code, content=detail)
    return handler


def register_auth_exception_handlers(app: FastAPI):
    app.add_exception_handler(FileNotFound, _create_handler(404, {
        "message": "File not found",
        "error_code": "file_not_found",
    }))

    app.add_exception_handler(InvalidToken, _create_handler(401, {
        "message": "Invalid token",
        "error_code": "invalid_token",
    }))

    app.add_exception_handler(UserAlreadyExists, _create_handler(409, {
        "message": "User already exists",
        "error_code": "user_already_exists",
    }))

    app.add_exception_handler(UserNotFound, _create_handler(404, {
        "message": "User not found",
        "error_code": "user_not_found",
    }))

    app.add_exception_handler(InvalidCredentials, _create_handler(401, {
        "message": "Invalid email or password",
        "error_code": "invalid_credentials",
    }))

    app.add_exception_handler(PasswordsDoNotMatch, _create_handler(400, {
        "message": "Passwords do not match",
        "error_code": "passwords_mismatch",
    }))

    app.add_exception_handler(ResetCodeInvalid, _create_handler(400, {
        "message": "Invalid or expired reset code",
        "error_code": "invalid_reset_code",
    }))

    app.add_exception_handler(InsufficientPrivileges, _create_handler(403, {
        "message": "You do not have sufficient privileges",
        "error_code": "insufficient_privileges",
    }))