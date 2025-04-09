"""
Response models for user messages and reports
"""
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class Link(BaseModel):
    """
    Pagination link model
    """
    url: Optional[str] = None
    label: str
    active: bool


class MessagePart(BaseModel):
    """
    Message part details
    """
    group: int
    accepted: bool
    dlr_time: str
    dlr_state: str
    part_index: int
    accept_time: str
    template_tag: Optional[str] = None
    accept_status: int


class MessageResult(BaseModel):
    """
    Individual message result
    """
    id: Any  # Can be int or str
    user_id: Any  # Can be int or str
    country_id: Optional[Any] = None  # Can be int or str
    connection_id: Any  # Can be int or str
    smsc_id: Any  # Can be int or str
    dispatch_id: Optional[str] = None
    user_sms_id: Optional[str] = None
    request_id: str
    price: int
    total_price: int
    is_ad: bool
    nick: str
    to: str
    message: str
    encoding: int
    parts_count: int
    parts: Dict[str, MessagePart]
    status: str
    smsc_data: Dict[str, List[str]]
    template_tag: Optional[str] = None
    sent_at: str
    submit_sm_resp_at: str
    delivery_sm_at: str
    created_at: str
    updated_at: str


class MessageData(BaseModel):
    """
    Message data with pagination
    """
    current_page: int
    path: str
    prev_page_url: Optional[str] = None
    first_page_url: str
    last_page_url: str
    next_page_url: Optional[str] = None
    per_page: int
    last_page: int
    from_: int = Field(..., alias="from")
    to: int
    total: int
    result: List[MessageResult]
    links: List[Link]


class GetUserMessagesResponse(BaseModel):
    """
    Response model for user messages
    """
    data: MessageData
    status: str


class DispatchStatusItem(BaseModel):
    """
    Status item for dispatch
    """
    status: str
    total: int


class GetDispatchStatusResponse(BaseModel):
    """
    Response model for dispatch status
    """
    status: str
    data: List[DispatchStatusItem]
    id: Optional[Any] = None


class MessageStatusResponse(BaseModel):
    """
    Response model for message status by ID
    """
    status: str
    data: MessageResult
