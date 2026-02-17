from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models import OwnershipRecord
from app.rate_limiter import limiter
from app.schemas import (
    OwnershipRecordCreate,
    OwnershipRecordList,
    OwnershipRecordResponse,
    OwnershipRecordUpdate,
)

router = APIRouter(prefix="/api/v1", tags=["ownership"])


@router.post("/records", response_model=OwnershipRecordResponse, status_code=201)
@limiter.limit(settings.rate_limit_write)
def create_record(
    request: Request,
    payload: OwnershipRecordCreate,
    db: Session = Depends(get_db),
) -> OwnershipRecord:
    record = OwnershipRecord(
        owner_name=payload.owner_name,
        animal_name=payload.animal_name,
        since_date=payload.since_date,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("/records", response_model=OwnershipRecordList)
@limiter.limit(settings.rate_limit_read)
def list_records(
    request: Request,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    owner_name: str | None = Query(None),
    db: Session = Depends(get_db),
) -> OwnershipRecordList:
    query = db.query(OwnershipRecord)
    if owner_name:
        query = query.filter(
            OwnershipRecord.owner_name.ilike(f"%{owner_name}%")
        )
    total = query.count()
    records = query.offset(skip).limit(limit).all()
    return OwnershipRecordList(total=total, records=records)


@router.get("/records/{record_id}", response_model=OwnershipRecordResponse)
@limiter.limit(settings.rate_limit_read)
def get_record(
    request: Request,
    record_id: int,
    db: Session = Depends(get_db),
) -> OwnershipRecord:
    record = db.query(OwnershipRecord).filter(
        OwnershipRecord.id == record_id
    ).first()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return record


@router.put("/records/{record_id}", response_model=OwnershipRecordResponse)
@limiter.limit(settings.rate_limit_write)
def update_record(
    request: Request,
    record_id: int,
    payload: OwnershipRecordUpdate,
    db: Session = Depends(get_db),
) -> OwnershipRecord:
    record = db.query(OwnershipRecord).filter(
        OwnershipRecord.id == record_id
    ).first()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(record, field, value)
    db.commit()
    db.refresh(record)
    return record


@router.delete("/records/{record_id}")
@limiter.limit(settings.rate_limit_write)
def delete_record(
    request: Request,
    record_id: int,
    db: Session = Depends(get_db),
) -> dict[str, str]:
    record = db.query(OwnershipRecord).filter(
        OwnershipRecord.id == record_id
    ).first()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    db.delete(record)
    db.commit()
    return {"detail": "deleted"}


@router.get("/health", tags=["health"])
@limiter.limit(settings.rate_limit_read)
def health_check(request: Request) -> dict[str, str]:
    return {"status": "healthy"}
