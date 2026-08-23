from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    username: str
    email: EmailStr

class LoginUser(BaseModel):
    email: EmailStr
    password: str

class RegisterUser(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    model_config = {"from_attributes": True}