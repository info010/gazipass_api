import uuid

from sqlalchemy import Column, ForeignKey, String, DateTime, Table, Text, Integer, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from ..database import Base
from database.models.user import user_upvoted_posts

post_tags = Table(
    "post_tags",
    Base.metadata,
    Column("tag_id", UUID(as_uuid=True), ForeignKey("tags.id"), primary_key=True),
    Column("post_id", UUID(as_uuid=True), ForeignKey("posts.id"), primary_key=True)
)

post_comments = Table(
    "post_comments",
    Base.metadata,
    Column("comment_id", UUID(as_uuid=True), ForeignKey("comments.id"), primary_key=True),
    Column("post_id", UUID(as_uuid=True), ForeignKey("posts.id"), primary_key=True)
)

class Post(Base):
    __tablename__ = "posts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    upvotes = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    creator_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))


    creator = relationship("User", back_populates="posts")
    tags = relationship(
        "Tag",
        secondary=post_tags,
        back_populates="posts"
    )
    upvoted_by = relationship(
        "User",
        secondary=user_upvoted_posts,
        back_populates="upvoted_posts"
    )