from pydantic import BaseModel, Field
from datetime import date
from typing import Optional, List


class PostSchema(BaseModel):
    id: int
    user_id: int
    title: str
    text: str
    created_at: date
    autoresponder_enabled: bool
    autoresponder_delay: int
    is_blocked: bool
    is_checked: bool


class NewPostSchema(BaseModel):
    title: str
    text: str
    created_at: date
    autoresponder_enabled: bool
    autoresponder_delay: int
    is_blocked: bool
    is_checked: bool


class UpdatePostSchema(BaseModel):
    title: Optional[str] = Field(None)
    text: Optional[str]
    autoresponder_enabled: Optional[bool]
    autoresponder_delay: Optional[int]



class CommentSchema(BaseModel):
    id: int
    user_id: int
    post_id: int
    text: str
    created_at: date
    is_blocked: bool
    is_checked: bool
    parent_id: Optional[int] = None
    children: List["CommentSchema"] = []

    class Config:
        from_attributes = True


class NewCommentSchema(BaseModel):
    text: str
    created_at: date
    parent_id: Optional[int] = None


class CurrentCommentSchema(BaseModel):
    id: int
    user_id: int
    post_id: int
    text: str
    created_at: date
    is_blocked: bool
    is_checked: bool
    parent_id: Optional[int] = None


class UpdateCommentSchema(BaseModel):
    text: Optional[str]
