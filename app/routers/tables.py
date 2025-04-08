from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.table import Table, TableCreate
from app.services.table_service import service_create_table, service_delete_table, service_get_table, service_get_tables
from app.database import get_async_db

router = APIRouter(
    prefix="/tables",
    tags=["tables"],
)

@router.get("/", response_model=List[Table])
async def read_tables(db: AsyncSession = Depends(get_async_db)):
    tables = await service_get_tables(db)
    return tables

@router.post("/", response_model=Table)
async def create_table(table: TableCreate, db: AsyncSession = Depends(get_async_db)):
    return await service_create_table(db=db, table=table)

@router.delete("/{table_id}", response_model=bool)
async def delete_table(table_id: int, db: AsyncSession = Depends(get_async_db)):
    if not await service_get_table(db, table_id=table_id):
        raise HTTPException(status_code=404, detail="Столик не найден")
    return await service_delete_table(db=db, table_id=table_id)