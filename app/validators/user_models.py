from typing import List, Optional
from pydantic import BaseModel

class UserResponse(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    roles: List[str]
    created_at: str

class UpdateUserRequest(BaseModel):
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    roles: Optional[List[str]] = []