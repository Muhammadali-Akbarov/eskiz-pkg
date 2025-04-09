"""
Response models for reports
"""
from typing import List, Optional, Any
from pydantic import BaseModel


class TotalsData(BaseModel):
    """
    Data model for totals
    """
    ad_parts: int
    ad_spent: int
    parts: int
    spent: int
    total_parts: int
    total_spent: int


class TotalsResponse(BaseModel):
    """
    Response model for totals
    """
    data: TotalsData


class UserTotalsItem(BaseModel):
    """
    Item in user totals response
    """
    month: str
    status: str
    packets: int
    sent_packets: int


class UserTotalsResponse(BaseModel):
    """
    Response model for user totals
    """
    status: str
    data: List[UserTotalsItem]
    id: Optional[Any] = None
