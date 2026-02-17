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
    assert result is not None, "record should be persisted in the database"
    assert result.owner_name == "Ala", "owner_name should match inserted value"
    assert result.animal_name == "kot", "animal_name should match inserted value"
    assert result.since_date == date(2024, 10, 31), "since_date should match"


def test_ownership_record_has_auto_id(db_session: Session) -> None:
    record = OwnershipRecord(
        owner_name="Ala",
        animal_name="kot",
        since_date=date(2024, 10, 31),
    )
    db_session.add(record)
    db_session.commit()
    db_session.refresh(record)
    assert record.id is not None, "id should be auto-generated"
    assert record.id > 0, "id should be a positive integer"


def test_created_at_auto_populated(db_session: Session) -> None:
    record = OwnershipRecord(
        owner_name="Ala",
        animal_name="kot",
        since_date=date(2024, 10, 31),
    )
    db_session.add(record)
    db_session.commit()
    db_session.refresh(record)
    assert record.created_at is not None, "created_at should be auto-populated"


def test_multiple_records_independent(db_session: Session) -> None:
    r1 = OwnershipRecord(owner_name="Ala", animal_name="kot", since_date=date(2024, 1, 1))
    r2 = OwnershipRecord(owner_name="Bartek", animal_name="pies", since_date=date(2025, 6, 15))
    db_session.add_all([r1, r2])
    db_session.commit()

    results = db_session.query(OwnershipRecord).all()
    assert len(results) == 2, "both records should be stored independently"
    names = {r.owner_name for r in results}
    assert names == {"Ala", "Bartek"}, "each record should retain its own data"
