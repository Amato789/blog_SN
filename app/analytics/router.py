from fastapi import APIRouter, Query
from datetime import date, datetime
from app.posts.dao import PostDAO, CommentDAO
from app.analytics.schemas import DailyPostAnalytics, DailyCommentAnalytics

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)


@router.get("/posts/daily-breakdown")
async def get_posts_analytics(

        date_from: date = Query(..., description=f"Например, {datetime.now().date()}"),
        date_to: date = Query(..., description=f"Например, {datetime.now().date()}")
) -> list[DailyPostAnalytics]:
    return await PostDAO.get_analytics(date_from=date_from, date_to=date_to)


@router.get("/comments/daily-breakdown")
async def get_comments_analytics(

        date_from: date = Query(..., description=f"Например, {datetime.now().date()}"),
        date_to: date = Query(..., description=f"Например, {datetime.now().date()}")
) -> list[DailyCommentAnalytics]:
    return await CommentDAO.get_analytics(date_from=date_from, date_to=date_to)
