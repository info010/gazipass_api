from typing import Generic, TypeVar
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")

class BaseController(Generic[T]):
    def __init__(self, service_cls: type[T]):
        self.service_cls = service_cls

    def with_service(self, db: AsyncSession) -> T:
        return self.service_cls(db)
