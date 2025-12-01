from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database.models.user import User
from utils.security import hash_pwd, verify_pwd

async def create_user(
    db: AsyncSession,
    username: str,
    email: str,
    password: str,
    first_name: str,
    last_name: str
) -> User:
    hashed = hash_pwd(password)
    user = User(
        username=username,
        email=email,
        hashed_password=hashed,
        first_name=first_name,
        last_name=last_name
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    q = select(User).where(User.email == email)
    res = await db.execute(q)
    return res.scalar_one_or_none()

async def get_user_by_username(db: AsyncSession, username: str) -> User | None:
    q = select(User).where(User.username == username)
    res = await db.execute(q)
    return res.scalar_one_or_none()

async def get_user_by_id(db: AsyncSession, user_id) -> User | None:
    q = select(User).where(User.id == user_id)
    res = await db.execute(q)
    return res.scalar_one_or_none()

async def verify_users_pwd(db: AsyncSession, email, pwd) -> User | None:
    user = await get_user_by_email(db=db, email=email)
    if user and verify_pwd(pwd=pwd, hash=user.hashed_password):
        return user
    return None

async def update_user(db: AsyncSession, user: User, **fields) -> User:
    for key, value in fields.items():
        if hasattr(user, key):
            setattr(user, key, value)

    await db.commit()
    await db.refresh(user)
    return user

async def delete_user(db: AsyncSession, user: User) -> None:
    await db.delete(user)
    await db.commit()