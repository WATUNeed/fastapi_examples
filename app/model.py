from pydantic import BaseModel, Field, EmailStr


class UserSchema(BaseModel):
    fullname: str = Field(example='Joe Doe')
    email: EmailStr = Field(example='joe@xyz.com')
    password: str = Field(example='any')


class UserLoginSchema(BaseModel):
    email: EmailStr = Field(example='joe@xyz.com')
    password: str = Field(example='any')

