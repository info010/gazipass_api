from .database import engine, Base

from .models.comment import Comment, Reply, comment_replies
from .models.post import Post, post_comments, post_tags
from .models.tag import Tag
from .models.user import User, user_followed_tags, user_upvoted_posts
from .models.refresh_token import RefreshToken

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)