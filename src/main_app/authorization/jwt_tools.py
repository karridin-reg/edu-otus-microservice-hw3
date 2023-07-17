from fastapi import HTTPException, status
from jose import jwt
from jose.exceptions import ExpiredSignatureError


def get_token_user_name(token) -> str | None:
    try:
        jwt_data = jwt.decode(token=token, key='secret')
        return jwt_data.get('username')
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is expired")
