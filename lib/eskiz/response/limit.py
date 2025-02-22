"""
the limit response
"""
from pydantic import BaseModel


class GetLimitResponse(BaseModel):
    """
    Response model for the /api/user/get-limit endpoint.
    """
    data: dict
    status: str
