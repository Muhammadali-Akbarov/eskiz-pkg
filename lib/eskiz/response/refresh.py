"""
the login response
"""
from pydantic import BaseModel


class TokenData(BaseModel):
    """
    The token data response
    """
    token: str


class RefreshTokenResponse(BaseModel):
    """
    The login response
    """
    message: str
    data: TokenData
    token_type: str
