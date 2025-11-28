import uuid

from sqlalchemy import Column, DateTime, ForeignKey, String, ARRAY, Table, func 
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from ..database import Base
from enum import Enum

class UserRole(Enum):
    DEFAULT = 1
    STUDENT = 2
    TEACHER = 3
    ADMIN = 4

user_upvoted_posts = Table(
    "user_upvoted_posts",
    Base.metadata,
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True),
    Column("post_id", UUID(as_uuid=True), ForeignKey("posts.id"), primary_key=True),
)

user_followed_users = Table(
    "user_followed_users",
    Base.metadata,
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True),
    Column("creator_id", UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True),
)

user_followed_tags = Table(
    "user_followed_tags",
    Base.metadata,
    Column("tag_id", UUID(as_uuid=True), ForeignKey("tags.id")),
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id"))
)

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    roles = Column(ARRAY(String), nullable=False, default=[UserRole.DEFAULT.name])
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    posts = relationship("Post", back_populates="creator")

    upvoted_posts = relationship(
        "Post",
        secondary=user_upvoted_posts,
        back_populates="upvoted_by"
    )

    followed_tags = relationship(
        "Tag",
        secondary=user_followed_tags,
        back_populates="followers"
    )

    followed_users = relationship(
        "User",
        secondary=user_followed_users,
        primaryjoin=id == user_followed_users.c.user_id,
        secondaryjoin=id == user_followed_users.c.creator_id,
        back_populates="followers"
    )

    followers = relationship(
        "User",
        secondary=user_followed_users,
        primaryjoin=id == user_followed_users.c.creator_id,
        secondaryjoin=id == user_followed_users.c.user_id,
        back_populates="followed_users"
    )
