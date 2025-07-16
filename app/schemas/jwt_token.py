from pydantic import BaseModel


class UserLogin(BaseModel):
    first_name: str
    password: str
    number: str


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
