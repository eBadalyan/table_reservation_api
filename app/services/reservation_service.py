from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_
from datetime import datetime, timedelta
from fastapi import HTTPException
from app.models.reservation import Reservation
from app.models.table import Table
from app.schemas.reservation import ReservationCreate

async def service_get_reservations(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Reservation).offset(skip).limit(limit))
    return result.scalars().all()

async def service_create_reservation(db: AsyncSession, reservation: ReservationCreate):
    result = await db.execute(select(Table).filter(Table.id == reservation.table_id))
    table = result.scalars().first()
    if not table:
        raise HTTPException(status_code=404, detail="Столик не найден")

    start_time = reservation.reservation_time
    print(f"start_time type: {type(start_time)}, value: {start_time}")
    print(f"reservation.duration_minutes type: {type(reservation.duration_minutes)}, value: {reservation.duration_minutes}")
    end_time = start_time + timedelta(minutes=reservation.duration_minutes)

    existing_reservation_result = await db.execute(
        select(Reservation).filter(
            and_(
                Reservation.table_id == reservation.table_id,
                Reservation.reservation_time < end_time,
            )
        )
    )
    existing_reservation = existing_reservation_result.scalars().all()

    for r in existing_reservation:
        r_end_time = r.reservation_time + timedelta(minutes=r.duration_minutes)
        if r_end_time > start_time:
            raise HTTPException(status_code=400, detail="Столик занят на выбранное время")

    db_reservation = Reservation(**reservation.dict())
    db.add(db_reservation)
    await db.commit()
    await db.refresh(db_reservation)
    return db_reservation

async def service_get_reservation(db: AsyncSession, reservation_id: int):
    result = await db.execute(select(Reservation).filter(Reservation.id == reservation_id))
    return result.scalars().first()

async def service_delete_reservation(db: AsyncSession, reservation_id: int):
    reservation = await service_get_reservation(db, reservation_id)
    if reservation:
        await db.delete(reservation)
        await db.commit()
        return True
    return False