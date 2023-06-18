import secrets
from typing import Any, Dict, List, Optional, Union

from fastapi_jwt_auth import AuthJWT
from pydantic import AnyHttpUrl, BaseConfig, PostgresDsn, validator


class Config(BaseConfig):
    API_V1_STR: str = "/api/v1"
    authjwt_secret_key: str = "4138387b6e86a6d4d0347537b954b25aca8ff8644acc67214648b82559f714a6"
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost:8000", "https://localhost:8000", "http://localhost",
                                              "http://localhost:5173"]

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str = "usearch"
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "rootpw"
    POSTGRES_DB: str = "postgres"

    @property
    def DB_URL(self) -> str:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=f"/{self.POSTGRES_DB or ''}",
        )

    class Config:
        case_sensitive = True
        env_file = ".env"


config = Config()


@AuthJWT.load_config
def get_config():
    return config
