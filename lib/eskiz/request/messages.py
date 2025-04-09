"""
Request models for retrieving user messages
"""
from typing import Optional
from pydantic import BaseModel


class GetUserMessagesRequest(BaseModel):
    """
    Request model for retrieving user messages
    """
    start_date: str
    end_date: str
    page_size: str = "20"
    count: str = "0"
    is_ad: str = ""
    status: Optional[str] = None

    def to_file(self):
        """
        Convert to file format for API request
        """
        data = {
            'start_date': (None, self.start_date),
            'end_date': (None, self.end_date),
            'page_size': (None, self.page_size),
            'count': (None, self.count),
            'is_ad': (None, self.is_ad),
        }
        
        if self.status is not None:
            data['status'] = (None, self.status)
            
        return data


class GetUserMessagesByDispatchRequest(BaseModel):
    """
    Request model for retrieving user messages by dispatch ID
    """
    dispatch_id: str
    count: str = "0"
    is_ad: str = ""
    status: Optional[str] = None

    def to_file(self):
        """
        Convert to file format for API request
        """
        data = {
            'dispatch_id': (None, self.dispatch_id),
            'count': (None, self.count),
            'is_ad': (None, self.is_ad),
        }
        
        if self.status is not None:
            data['status'] = (None, self.status)
            
        return data


class GetDispatchStatusRequest(BaseModel):
    """
    Request model for retrieving dispatch status
    """
    user_id: str
    dispatch_id: str

    def to_file(self):
        """
        Convert to file format for API request
        """
        return {
            'user_id': (None, self.user_id),
            'dispatch_id': (None, self.dispatch_id),
        }


class ExportMessagesRequest(BaseModel):
    """
    Request model for exporting messages
    """
    year: str
    month: str
    status: str = "all"

    def to_file(self):
        """
        Convert to file format for API request
        """
        return {
            'year': (None, self.year),
            'month': (None, self.month),
        }
