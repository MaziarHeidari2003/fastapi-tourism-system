from fastapi import APIRouter, Depends, status
from .. import schemas, database, oauth2
from sqlalchemy.ext.asyncio import AsyncSession
from tourism.repository import transportation
from typing import List

router = APIRouter(tags=["Airports"], prefix="/airports")

@router.post("/create-airport", status_code=status.HTTP_201_CREATED)
async def create_airport_route(
    request: schemas.Airport, db: AsyncSession = Depends(database.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)
):
    return await transportation.create_airport(request, db)

@router.post("/create-flight", status_code=status.HTTP_201_CREATED)
async def create_flight_route(
    request: schemas.Flight, db: AsyncSession = Depends(database.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)
):
    return await transportation.create_flight(request, db)

@router.get("/", response_model=List[schemas.Airport])
async def all_airport(db: AsyncSession = Depends(database.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return await transportation.show_airports(db)

@router.get("/desired-flight", response_model=List[schemas.AvailableFlights])
async def available_flights(origin_id: int, destination_id: int, departure_date: str, db: AsyncSession = Depends(database.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return await transportation.show_flights(origin_id, destination_id, departure_date, db)




@router.post("/add-passengers", response_model=schemas.Passengers)
async def new_passenger(
    parent_user_id: int, name: str, national_id: str, age: int, gender: str, current_user: schemas.User = Depends(oauth2.get_current_user), db: AsyncSession = Depends(database.get_db)
):
    return await transportation.create_passenger(parent_user_id, name, national_id, age, gender, db)




@router.post("/choose-flight")
async def choose_flight(
    request: schemas.ChooseFlightRequest,
    db: AsyncSession = Depends(database.get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    return await transportation.reserve_flight_for_passengers(
        request.parent_user_id, request.passenger_ids, request.flight_price, request.flight_id,db
    )

# a guide for me =>
"""
To convert my APIs to asynchronous, I need to:

Use asynchronous database sessions (AsyncSession from SQLAlchemy).
Replace def with async def for both repository functions and routes.
Use await for all database operations.
Modify your database configuration to support asynchronous operations.
"""