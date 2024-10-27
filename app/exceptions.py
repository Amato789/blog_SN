from fastapi import HTTPException, status


class BlogException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(BlogException):
    status_code = status.HTTP_409_CONFLICT
    detail = "The user already exists"


class IncorrectEmailOrPasswordException(BlogException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Invalid email or password"


class TokenExpiredException(BlogException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "The token has expired"


class TokenAbsentException(BlogException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "The token is missing"


class IncorrectTokenFormatException(BlogException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Incorrect token format"


class UserIsNotPresentException(BlogException):
    status_code = status.HTTP_401_UNAUTHORIZED


class CommentNotFoundException(BlogException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Comment not found"


class PostNotFoundException(BlogException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Post not found"


class ModerateByOpenAIError(BlogException):
    status_code = status.HTTP_408_REQUEST_TIMEOUT
    detail = "Failed to moderate the string"

