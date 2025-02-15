from datetime import datetime, timedelta, timezone

import jwt
from fastapi.security import OAuth2PasswordBearer

from app.core import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/token")


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return encoded_jwt
