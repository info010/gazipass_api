from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from core.common.api_models import APIResponse

class BaseService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def commit(self):
        try:
            await self.db.commit()
        except Exception:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail="Database commit failed")

    def success(self, message: str, data=None):
        return APIResponse(
            success=True,
            message=message,
            data=data
        )

    def error(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        raise HTTPException(status_code=status_code, detail=message)
