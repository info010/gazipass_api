import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Table, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from database.database import Base

comment_replies =  Table(
    "comment_replies",
    Base.metadata,
    Column("comment_id", UUID(as_uuid=True), ForeignKey("comments.id")),
    Column("reply_id", UUID(as_uuid=True), ForeignKey("replies.id"))
)

class Comment(Base):
    __tablename__ = "comments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    creator_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    post_id = Column(UUID(as_uuid=True), ForeignKey("posts.id", ondelete="CASCADE"))

    creator = relationship("User", backref="comments")
    post = relationship("Post", backref="comments")
    replies = relationship(
        "Reply",
        secondary=comment_replies,
        back_populates="comments"
    )

class Reply(Base):
    __tablename__ = "replies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    creator_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    comment_id = Column(UUID(as_uuid=True), ForeignKey("comments.id", ondelete="CASCADE"))

    creator = relationship("User", backref="replies")
    comments = relationship(
        "Comment",
        secondary=comment_replies,
        back_populates="replies"
    )
