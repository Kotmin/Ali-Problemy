"""Direct unit tests for Pydantic schemas — no API, no DB."""

from datetime import date

import pytest
from pydantic import ValidationError

from app.schemas import OwnershipRecordCreate, OwnershipRecordUpdate


# --- OwnershipRecordCreate ---


class TestOwnershipRecordCreate:
    def test_happy_path(self) -> None:
        record = OwnershipRecordCreate(
            owner_name="Ala", animal_name="kot", since_date=date(2024, 10, 31)
        )
        assert record.owner_name == "Ala", "owner_name should be preserved"
        assert record.animal_name == "kot", "animal_name should be preserved"
        assert record.since_date == date(2024, 10, 31), "since_date should match"

    def test_whitespace_is_stripped(self) -> None:
        record = OwnershipRecordCreate(
            owner_name="  Ala  ", animal_name="\tpies\n", since_date=date(2024, 1, 1)
        )
        assert record.owner_name == "Ala", "leading/trailing whitespace should be stripped"
        assert record.animal_name == "pies", "tabs and newlines should be stripped"

    @pytest.mark.parametrize(
        "owner, animal, reason",
        [
            ("", "kot", "empty owner_name"),
            ("Ala", "", "empty animal_name"),
            ("   ", "kot", "whitespace-only owner_name"),
            ("Ala", "\t\n", "whitespace-only animal_name"),
        ],
        ids=["empty_owner", "empty_animal", "ws_owner", "ws_animal"],
    )
    def test_rejects_empty_or_whitespace(
        self, owner: str, animal: str, reason: str
    ) -> None:
        with pytest.raises(ValidationError, match="Must not be empty|at least 1"):
            OwnershipRecordCreate(
                owner_name=owner, animal_name=animal, since_date=date(2024, 1, 1)
            )

    @pytest.mark.parametrize(
        "field",
        ["owner_name", "animal_name"],
        ids=["owner_too_long", "animal_too_long"],
    )
    def test_rejects_over_max_length(self, field: str) -> None:
        data = {
            "owner_name": "Ala",
            "animal_name": "kot",
            "since_date": date(2024, 1, 1),
        }
        data[field] = "x" * 101
        with pytest.raises(ValidationError, match="at most 100"):
            OwnershipRecordCreate(**data)

    def test_rejects_invalid_date_string(self) -> None:
        with pytest.raises(ValidationError):
            OwnershipRecordCreate(
                owner_name="Ala", animal_name="kot", since_date="not-a-date"  # type: ignore[arg-type]
            )

    def test_rejects_missing_fields(self) -> None:
        with pytest.raises(ValidationError) as exc_info:
            OwnershipRecordCreate()  # type: ignore[call-arg]
        errors = exc_info.value.errors()
        missing_fields = {e["loc"][0] for e in errors}
        assert missing_fields == {"owner_name", "animal_name", "since_date"}, (
            "all three fields should be required"
        )


# --- OwnershipRecordUpdate ---


class TestOwnershipRecordUpdate:
    def test_all_fields_optional(self) -> None:
        update = OwnershipRecordUpdate()
        assert update.owner_name is None, "owner_name should default to None"
        assert update.animal_name is None, "animal_name should default to None"
        assert update.since_date is None, "since_date should default to None"

    def test_partial_update(self) -> None:
        update = OwnershipRecordUpdate(owner_name="Bartek")
        assert update.owner_name == "Bartek", "provided field should be set"
        assert update.animal_name is None, "unset fields should remain None"

    def test_strips_whitespace(self) -> None:
        update = OwnershipRecordUpdate(owner_name="  Bartek  ")
        assert update.owner_name == "Bartek", "whitespace should be stripped"

    def test_rejects_whitespace_only(self) -> None:
        with pytest.raises(ValidationError, match="Must not be empty"):
            OwnershipRecordUpdate(owner_name="   ")

    def test_exclude_unset_serialization(self) -> None:
        update = OwnershipRecordUpdate(animal_name="pies")
        dumped = update.model_dump(exclude_unset=True)
        assert dumped == {"animal_name": "pies"}, (
            "only explicitly set fields should appear in exclude_unset dump"
        )
