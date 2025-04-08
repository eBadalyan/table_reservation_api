from fastapi import FastAPI
from app.routers.tables import router as router_table
from app.routers.reservations import router as router_reservations

app = FastAPI()

app.include_router(router_table)
app.include_router(router_reservations)