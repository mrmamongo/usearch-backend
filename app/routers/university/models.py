import uuid

from pydantic import BaseModel, validator

from app.core.utils import as_form

translations = {
    "budget": "БЮДЖЕТ",
    "paid": "ПЛАТНОЕ",
    "state": "ГОСУДАРСТВЕННЫЙ",
    "nostate": "НЕГОСУДАРСТВЕННЫЙ",
    "hostel": "ОБЩЕЖИТИЕ",
    "license": "ЛИЦЕНЗИЯ",
    "vuz": "ЖОПА"
}


class UniversityRead(BaseModel):
    id: uuid.UUID
    long_name: str
    url: str
    tags: list[tuple[str, str]]

    @validator('tags', pre=True)
    def validate_tags(cls, v):
        values = [m.strip().replace('\'', '') for m in v[-1].split(', ')]
        return [(m, translations[m]) for m in values]

    class Config:
        orm_mode = True


@as_form
class UniversityCreate(BaseModel):
    long_name: str
    url: str
    tags: list[str]


class UniversityUpdate(BaseModel):
    long_name: str | None
    url: str | None
    tags: list[str] | None
