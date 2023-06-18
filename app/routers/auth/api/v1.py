from typing import Annotated

from app.routers.auth.dependencies import (
    get_current_user,
)
from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from starlette import status

from app.routers.auth.models import UserRead

router = APIRouter()


@router.post('/login')
def login(user: UserRead, Authorize: AuthJWT = Depends()):
    if user.username != "test" or user.password != "test":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Bad username or password")

    return {"access_token": Authorize.create_access_token(subject=user.username), "refresh_token": Authorize.create_refresh_token(subject=user.username)}


@router.post('/refresh')
def refresh(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()

    return {"access_token": Authorize.create_access_token(subject=Authorize.get_jwt_subject())}


@router.get("/profile/", response_model=UserRead)
async def read_users_me(current_user: Annotated[UserRead, Depends(get_current_user)]):
    return current_user
