from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr = Field(max_length=120)


class LoginUser(BaseModel):
    email: EmailStr = Field(max_length=120)
    password: str = Field(min_length=8, max_length=120)


class RegisterUser(UserBase):
    password: str = Field(min_length=8, max_length=120)


class UserResponse(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
