from typing import Annotated
from pydantic import BaseModel, Field

class PostRequest(BaseModel):
    title: Annotated[str, Field(min_length=3 ,max_length=100)]
    content: Annotated[str, Field(min_length=10)]
    tags: list[str]