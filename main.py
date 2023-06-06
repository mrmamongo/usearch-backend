from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import config
from app.routers import auth_router, university_router, user_router


def get_application():
    _app = FastAPI(title=config.PROJECT_NAME)

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in config.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    _app.include_router(auth_router, prefix=config.API_V1_STR)
    _app.include_router(university_router, prefix=config.API_V1_STR)
    _app.include_router(user_router, prefix=config.API_V1_STR)

    return _app


app = get_application()
