from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: float


class UserID(BaseModel):
    id: int


class ResponseUser(UserID):
    name: str
    email: EmailStr
    password: float
