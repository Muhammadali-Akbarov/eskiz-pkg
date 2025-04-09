"""
Response models for batch SMS operations
"""
from typing import List, Union
from pydantic import BaseModel


class SendBatchSMSResponse(BaseModel):
    """
    Response model for batch SMS sending
    """
    id: str
    message: str
    status: Union[List[str], str]


class SendGlobalSMSResponse(BaseModel):
    """
    Response model for global SMS sending
    """
    # Since the API returns 200 OK without a specific response body,
    # we'll create a simple model to handle this case
    success: bool = True
