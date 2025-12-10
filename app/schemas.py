from pydantic import BaseModel, EmailStr
from typing import Optional

# ========================
# User Base Schema
# ========================
class UserBase(BaseModel):
    email: EmailStr
    name: str
    bio: Optional[str] = None
    avatar_url: Optional[str] = None

# ========================
# User Create Schema
# ========================
class UserCreate(UserBase):
    password: str

# ========================
# User Login Schema
# ========================
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# ========================
# User Response Schema
# ========================
class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True