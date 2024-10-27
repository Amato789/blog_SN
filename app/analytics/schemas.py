from pydantic import BaseModel
from datetime import date


class DailyPostAnalytics(BaseModel):
    date: date
    total_posts: int
    blocked_posts: int


class DailyCommentAnalytics(BaseModel):
    date: date
    total_comments: int
    blocked_comments: int
