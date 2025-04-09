"""
Request models for reports
"""
from typing import Optional
from pydantic import BaseModel


class TotalsByRangeRequest(BaseModel):
    """
    Request model for getting totals by date range
    """
    start_date: str
    end_date: str
    is_ad: str = ""
    status: Optional[str] = None

    def to_file(self):
        """
        Convert to file format for API request
        """
        data = {
            'start_date': (None, self.start_date),
            'end_date': (None, self.end_date),
            'is_ad': (None, self.is_ad),
        }
        
        if self.status is not None:
            data['status'] = (None, self.status)
            
        return data


class TotalsByDispatchRequest(BaseModel):
    """
    Request model for getting totals by dispatch ID
    """
    dispatch_id: str
    is_ad: str = ""
    status: Optional[str] = None

    def to_file(self):
        """
        Convert to file format for API request
        """
        data = {
            'dispatch_id': (None, self.dispatch_id),
            'is_ad': (None, self.is_ad),
        }
        
        if self.status is not None:
            data['status'] = (None, self.status)
            
        return data


class UserTotalsRequest(BaseModel):
    """
    Request model for getting user totals
    """
    year: str
    month: str
    is_global: str = "0"

    def to_file(self):
        """
        Convert to file format for API request
        """
        return {
            'year': (None, self.year),
            'month': (None, self.month),
            'is_global': (None, self.is_global),
        }
