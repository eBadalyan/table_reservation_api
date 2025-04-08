from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.table import Table
from app.schemas.table import TableCreate

async def service_get_tables(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Table).offset(skip).limit(limit))
    return result.scalars().all()

async def service_create_table(db: AsyncSession, table: TableCreate):
    db_table = Table(name=table.name, seats=table.seats, location=table.location)
    db.add(db_table)
    await db.commit()
    await db.refresh(db_table)
    return db_table

async def service_get_table(db: AsyncSession, table_id: int):
    result = await db.execute(select(Table).filter(Table.id == table_id))
    return result.scalars().first()

async def service_delete_table(db: AsyncSession, table_id: int):
    table = await service_get_table(db, table_id)
    if table:
        await db.delete(table)
        await db.commit()
        return True
    return False