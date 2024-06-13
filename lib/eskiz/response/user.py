"""
getting user information of eskiz
"""
from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class UserData(BaseModel):
    """
    user data information model
    """
    id: int
    name: str
    email: str
    password: str
    role: str
    status: str
    is_vip: bool
    balance: int
    created_at: datetime
    updated_at: datetime


class UserResponse(BaseModel):
    """
    getting information response model
    """
    status: str
    data: UserData
    id: Optional[int] = None
