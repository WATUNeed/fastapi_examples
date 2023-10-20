from fastapi import Request, Response, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .auth_handler import decode_jwt


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request, response: Response):
        cookie_credentials = request.cookies.get('access_token')
        if cookie_credentials:
            payload = decode_jwt(cookie_credentials)
            if not payload:
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
        else:
            credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
            if credentials:
                if not credentials.scheme == "Bearer":
                    raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
                payload = decode_jwt(credentials.credentials)
                if not payload:
                    raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            else:
                raise HTTPException(status_code=403, detail="Invalid authorization code.")
        return payload
