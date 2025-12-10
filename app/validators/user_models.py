from typing import List
from pydantic import BaseModel

class UserResponse(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    roles: List[str]
    # posts: List[str]
    # upvoted_posts: List[str]
    # followers: List[str]
    # followed_users: List[str]
    # followed_tags: List[str]
    created_at: str

class UpdateUserRequest(BaseModel):
    email: str
    first_name: str
    last_name: str