from datetime import date

from sqlalchemy.orm import Session

from app.models import OwnershipRecord


def test_create_ownership_record_in_db(db_session: Session) -> None:
    record = OwnershipRecord(
        owner_name="Ala",
        animal_name="kot",
        since_date=date(2024, 10, 31),
    )
    db_session.add(record)
    db_session.commit()
    db_session.refresh(record)

    result = db_session.query(OwnershipRecord).first()
    assert result is not None
    assert result.owner_name == "Ala"
    assert result.animal_name == "kot"
    assert result.since_date == date(2024, 10, 31)


def test_ownership_record_has_auto_id(db_session: Session) -> None:
    record = OwnershipRecord(
        owner_name="Ala",
        animal_name="kot",
        since_date=date(2024, 10, 31),
    )
    db_session.add(record)
    db_session.commit()
    db_session.refresh(record)
    assert record.id is not None
    assert record.id > 0


def test_created_at_auto_populated(db_session: Session) -> None:
    record = OwnershipRecord(
        owner_name="Ala",
        animal_name="kot",
        since_date=date(2024, 10, 31),
    )
    db_session.add(record)
    db_session.commit()
    db_session.refresh(record)
    assert record.created_at is not None
