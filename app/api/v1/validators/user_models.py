from typing import List
from pydantic import BaseModel

class UserResponse(BaseModel):
    username: str
    email: str
    first_name: str | None
    last_name: str | None
    roles: List[str]
    created_at: str