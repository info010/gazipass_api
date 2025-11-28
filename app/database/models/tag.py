import uuid

from sqlalchemy import Column, DateTime, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from ..database import Base
from database.models.post import post_tags
from database.models.user import user_followed_tags

class Tag(Base):
    __tablename__ = "tags"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tag = Column(String(50), nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    posts = relationship(
        "Post",
        secondary=post_tags,
        back_populates="tags"
    )
    followers = relationship(
        "User",
        secondary=user_followed_tags,
        back_populates="followed_tags"
    )