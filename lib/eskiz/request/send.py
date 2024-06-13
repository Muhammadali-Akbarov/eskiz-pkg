"""
the send sms request model
"""
from pydantic import BaseModel


class SendSMSRequest(BaseModel):
    """
    the login request for getting token
    """
    phone_number: int
    message: str
    from_: str
    callback_url: str

    def to_file(self):
        """
        returning file format
        """
        return {
            'mobile_phone': (None, self.phone_number),
            'message': (None, self.message),
            'from': (None, self.from_),
            'callback_url': (None, self.callback_url),
        }
