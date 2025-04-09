"""
Request models for batch SMS operations
"""
from typing import List, Optional
from pydantic import BaseModel, Field


class BatchSMSMessage(BaseModel):
    """
    Individual message in a batch SMS request
    """
    user_sms_id: str
    to: int
    text: str


class SendBatchSMSRequest(BaseModel):
    """
    Request model for sending batch SMS messages
    """
    messages: List[BatchSMSMessage]
    from_: str = Field(..., alias="from")
    dispatch_id: Optional[int] = None

    def to_json(self):
        """
        Convert to JSON format for API request
        """
        data = self.model_dump(by_alias=True)
        return data


class SendGlobalSMSRequest(BaseModel):
    """
    Request model for sending SMS to international numbers
    """
    mobile_phone: str
    message: str
    country_code: str
    callback_url: str = ""
    unicode: str = "0"

    def to_file(self):
        """
        Convert to file format for API request
        """
        return {
            'mobile_phone': (None, self.mobile_phone),
            'message': (None, self.message),
            'country_code': (None, self.country_code),
            'callback_url': (None, self.callback_url),
            'unicode': (None, self.unicode),
        }
