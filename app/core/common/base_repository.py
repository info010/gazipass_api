from typing import Generic, TypeVar, Type, Optional, List, Union, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    model: Type[ModelType]

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, id) -> Optional[ModelType]:
        q = select(self.model).where(self.model.id == id)
        res = await self.db.execute(q)
        return res.scalar_one_or_none()
    
    async def get_by(self, **kwargs):
        q = select(self.model)
        for key, value in kwargs.items():
            q = q.where(getattr(self.model, key) == value)
        res = await self.db.execute(q)
        return res.scalar_one_or_none()

    async def create(self, data: Union[ModelType, Dict]) -> ModelType:
        if isinstance(data, dict):
            obj = self.model(**data)
        else:
            obj = data

        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def update(self, obj: ModelType, data: dict) -> ModelType:
        for key, value in data.items():
            setattr(obj, key, value)

        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def delete(self, obj: ModelType) -> bool:
        await self.db.delete(obj)
        await self.db.commit()
        return True
    
    async def list(self, size: int, offset: int) -> List[ModelType]:
        q = select(self.model).offset(offset).limit(size)
        res = await self.db.execute(q)
        return res.scalars().all()
    
    async def filter(self, size: int, offset: int, *criteria) -> List[ModelType]:
        q = select(self.model).where(*criteria).offset(offset).limit(size)
        res = await self.db.execute(q)
        return res.scalars().all()
