import uvicorn
from fastapi import FastAPI, Body, Depends, Response, status, HTTPException
from fastapi.responses import JSONResponse

from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import encode_jwt
from app.model import UserSchema, UserLoginSchema

app = FastAPI()

users = []


def check_user(data: UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
    return False


@app.get('/')
async def index(
        user: dict[str, str] = Depends(JWTBearer()),
):
    return {'details': user}


@app.post("/users/signup", tags=["user"])
def create_user(response: Response, user: UserSchema = Body(...)):
    users.append(user)
    access_token = encode_jwt(user.email)
    response.set_cookie('access_token', access_token)
    return {'access_token': access_token}


@app.post(
    path="/users/login",
    tags=["user"],
    responses={
        status.HTTP_200_OK: {
            "content": {
                "application/json": {
                    "example": {
                        'access_token': 'access_token'
                    }
                }
            }
        },
        status.HTTP_403_FORBIDDEN: {
            "content": {
                "application/json": {
                    "example": {
                        'detail': 'Wrong login details!'
                    }
                }
            }
        }
    }
)
def user_login(response: Response, user: UserLoginSchema = Body(...)):
    if check_user(user):
        access_token = encode_jwt(user.email)
        response.set_cookie('access_token', access_token)
        return JSONResponse(status_code=status.HTTP_200_OK, content={'access_token': access_token})
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Wrong login details!')


if __name__ == '__main__':
    uvicorn.run(app, host='192.168.0.104')
