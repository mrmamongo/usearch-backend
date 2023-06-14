from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.database.colleague import Colleague
from app.database.db import active_session
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
    return (await session.execute(select(Colleague))).scalars().fetchall()


@router.get("/{id}", response_model=UniversityRead)
async def get_university_by_id(
        univ_id: int, session: Annotated[AsyncSession, Depends(active_session)]
):
    univ = await session.get(Colleague, univ_id)
    if univ is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="University not found"
        )
    return univ


@router.post(
    "/", response_model=UniversityRead, dependencies=[Depends(get_current_admin_user)]
)
async def create_university(
        colleague: Annotated[UniversityCreate, Depends(UniversityCreate.as_form)],
        session: Annotated[AsyncSession, Depends(active_session)],
):
    try:
        coll = Colleague(
            long_name=colleague.long_name,
            url=colleague.url,
            tags=colleague.tags
        )
        session.add(coll)
        await session.commit()
        await session.refresh(coll)
        return coll
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="University already exists"
        )



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
    univ = await session.get(Colleague, univ_id)
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
    univ = session.get(Colleague, univ_id)

    if not univ:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="University not found"
        )

    await session.delete(univ)
    await session.commit()
