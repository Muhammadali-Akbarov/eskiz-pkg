"""
the login response
"""
from pydantic import BaseModel


class LoginRequest(BaseModel):
    """
    the login request for getting token
    """
    email: str
    password: str
