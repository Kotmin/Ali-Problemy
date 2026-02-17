from datetime import date, datetime

from pydantic import BaseModel, Field, field_validator


class OwnershipRecordCreate(BaseModel):
    owner_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        examples=["Ala"],
        description="Name of the owner",
    )
    animal_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        examples=["kot"],
        description="Name or type of the animal",
    )
    since_date: date = Field(
        ...,
        examples=["2024-10-31"],
        description="Date since the owner has the animal (YYYY-MM-DD)",
    )

    @field_validator("owner_name", "animal_name", mode="before")
    @classmethod
    def strip_whitespace(cls, v: str) -> str:
        if isinstance(v, str):
            stripped = v.strip()
            if not stripped:
                raise ValueError("Must not be empty or whitespace-only")
            return stripped
        return v


class OwnershipRecordUpdate(BaseModel):
    owner_name: str | None = Field(None, min_length=1, max_length=100)
    animal_name: str | None = Field(None, min_length=1, max_length=100)
    since_date: date | None = None

    @field_validator("owner_name", "animal_name", mode="before")
    @classmethod
    def strip_whitespace(cls, v: str | None) -> str | None:
        if isinstance(v, str):
            stripped = v.strip()
            if not stripped:
                raise ValueError("Must not be empty or whitespace-only")
            return stripped
        return v


class OwnershipRecordResponse(BaseModel):
    id: int
    owner_name: str
    animal_name: str
    since_date: date
    created_at: datetime | None = None

    model_config = {"from_attributes": True}


class OwnershipRecordList(BaseModel):
    total: int
    records: list[OwnershipRecordResponse]
