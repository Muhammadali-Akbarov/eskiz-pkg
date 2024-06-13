"""
sending sms response
"""
from pydantic import BaseModel


class SendSMSResponse(BaseModel):
    """
    sending sms response
    """
    id: str
    message: str
    status: str
