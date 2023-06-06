from typing import Annotated, Sequence

from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.database.db import active_session
from app.database.university import University
from app.routers.auth.dependencies import get_current_admin_user
from app.routers.university.models import (
    UniversityCreate,
    UniversityRead,
    UniversityUpdate,
)

router = APIRouter(prefix="/university")


@router.get("/", response_model=list[UniversityRead])
async def get_universities(
        session: Annotated[AsyncSession, Depends(active_session)]
):
    return (await session.execute(select(University))).scalars().fetchall()


@router.get("/{id}", response_model=UniversityRead)
async def get_university_by_id(
        univ_id: int, session: Annotated[AsyncSession, Depends(active_session)]
):
    univ = await session.get(University, univ_id)
    if univ is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="University not found"
        )
    return univ


@router.post(
    "/", response_model=UniversityRead, dependencies=[Depends(get_current_admin_user)]
)
async def create_university(
        university: Annotated[UniversityCreate, Depends(UniversityCreate.as_form)],
        session: Annotated[AsyncSession, Depends(active_session)],
):
    try:
        univ = University(
            long_name=university.long_name,
            url=university.url,
            tags=university.tags
        )
        session.add(univ)
        await session.commit()
        await session.refresh(univ)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="University already exists"
        )
    return univ


@router.put(
    "/{id}",
    response_model=UniversityRead,
    dependencies=[Depends(get_current_admin_user)],
)
async def update_university(
        univ_id: int,
        university: UniversityUpdate,
        session: Annotated[AsyncSession, Depends(active_session)],
):
    univ = await session.get(University, univ_id)
    if univ is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="University not found"
        )

    for key, value in university.dict(exclude_none=True).items():
        setattr(univ, key, value)

    await session.commit()
    await session.refresh(univ)
    return univ


@router.delete(
    "/{id}",
    response_model=UniversityRead,
    dependencies=[Depends(get_current_admin_user)],
)
async def delete_university(
        univ_id: int, session: Annotated[AsyncSession, Depends(active_session)]
):
    univ = session.get(University, univ_id)

    if not univ:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="University not found"
        )

    await session.delete(univ)
    await session.commit()
