import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from starlette import status

from app.database import active_session, User
from app.routers.auth.dependencies import get_password_hash
from app.routers.auth.models import UserRead
from app.routers.user.models import UserUpdate, UserCreate

router = APIRouter(prefix="/user")


@router.get("/", response_model=list[UserRead])
async def get_users(session: Annotated[AsyncSession, Depends(active_session)]):
    # TODO: Implement search logic
    return (await session.scalars(select(User))).fetchall()


@router.get("/{id}", response_model=UserRead)
async def get_user(id: int, session: Annotated[AsyncSession, Depends(active_session)]):
    user = await session.get(User, id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.post("/", response_model=UserRead)
async def create_user(
    user: Annotated[UserCreate, Depends(UserCreate.as_form)], session: Annotated[AsyncSession, Depends(active_session)]
):
    try:
        new_user = User(
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            scores=user.scores,
            hashed_password=get_password_hash(user.password),
        )
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)

    except IntegrityError as e:
        logging.error(e)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User already exists"
        )

    return new_user


@router.put("/{id}", response_model=UserRead)
async def update_user(
    id: int,
    user_update: UserUpdate,
    session: Annotated[AsyncSession, Depends(active_session)],
):
    user = session.get(User, id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User is not exist"
        )

    for key, value in user_update.dict(exclude_none=True).items():
        setattr(user, key, value)

    await session.commit()
    await session.refresh(user)

    return user
