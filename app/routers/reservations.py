from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.reservation import Reservation, ReservationCreate
from app.services.reservation_service import service_create_reservation, service_delete_reservation, service_get_reservation, service_get_reservations
from app.database import get_async_db

router = APIRouter(
    prefix="/reservations",
    tags=["reservations"],
)

@router.get("/", response_model=List[Reservation])
async def read_reservations(db: AsyncSession = Depends(get_async_db)):
    reservations = await service_get_reservations(db)
    return reservations

@router.post("/", response_model=Reservation)
async def create_reservation(reservation: ReservationCreate, db: AsyncSession = Depends(get_async_db)):
    try:
        return await service_create_reservation(db=db, reservation=reservation)
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Ошибка при создании брони")

@router.delete("/{reservation_id}", response_model=bool)
async def delete_reservation(reservation_id: int, db: AsyncSession = Depends(get_async_db)):
    if not await service_get_reservation(db, reservation_id=reservation_id):
        raise HTTPException(status_code=404, detail="Бронь не найдена")
    return await service_delete_reservation(db=db, reservation_id=reservation_id)