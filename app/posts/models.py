from datetime import date
from typing import Optional
from sqlalchemy import Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Posts(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(nullable=False)
    text: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[date] = mapped_column(Date)
    autoresponder_enabled: Mapped[bool] = mapped_column(nullable=False, default=False)
    autoresponder_delay: Mapped[int] = mapped_column(nullable=True, default=0)
    is_blocked: Mapped[bool] = mapped_column(nullable=False, default=False)
    is_checked: Mapped[bool] = mapped_column(nullable=False, default=False)

    users = relationship("Users", back_populates="posts")
    comments = relationship("Comments", back_populates="posts", cascade="all, delete")

    def __str__(self):
        return f"Post #{self.id}"


class Comments(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id", ondelete="CASCADE"))
    text: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[date] = mapped_column(Date)
    is_blocked: Mapped[bool] = mapped_column(nullable=False, default=False)
    is_checked: Mapped[bool] = mapped_column(nullable=False, default=False)
    parent_id: Mapped[Optional[int]] = mapped_column(ForeignKey("comments.id"), nullable=True)

    users = relationship("Users", back_populates="comments")
    posts = relationship("Posts", back_populates="comments")
    parent = relationship("Comments", remote_side=[id], back_populates="children")
    children = relationship("Comments", back_populates="parent")

    def __str__(self):
        return f"Comment #{self.id}"
