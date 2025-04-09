"""
Response models for templates
"""
from typing import List
from pydantic import BaseModel


class TemplateItem(BaseModel):
    """
    Individual template item
    """
    id: int
    template: str
    original_text: str
    status: str


class TemplatesResponse(BaseModel):
    """
    Response model for templates
    """
    success: bool
    result: List[TemplateItem]
