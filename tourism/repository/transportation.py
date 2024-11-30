from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .. import models, schemas,utils
from fastapi import HTTPException, status

# Well I SHOULD LEARN MORE ABOUT ASYNCRONOUS METHODS, CHATGPT HANDLED A LOT!

async def create_airport(request: schemas.User, db: AsyncSession):
    new_airport = models.Airport(
        name=request.name,
        code=request.code,
    )
    db.add(new_airport)
    await db.commit()
    await db.refresh(new_airport)
    return new_airport


async def create_flight(request: schemas.Flight,db: AsyncSession):
    new_flight = models.Flight(
    flight_number=request.flight_number,
    origin_id=request.origin_id,
    destination_id = request.destination_id,
    departure_date = request.departure_date,
    arrival_date = request.arrival_date,
    price = request.price,
    provider = request.provider
    ) 
    db.add(new_flight)
    await db.commit()
    await db.refresh(new_flight)
    return new_flight   


async def show_airports(db: AsyncSession):
    result = await db.execute(select(models.Airport))
    airports = result.scalars().all()
    return airports

async def reserve_flight_for_passengers(user_id, passenger_ids, flight_price, flight_id, db: AsyncSession):
    user_result = await db.execute(select(models.User).filter_by(id=user_id))
    user = user_result.scalar()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with {user_id} not found")

    passengers = []

    for passenger_id in passenger_ids:
        result = await db.execute(
            select(models.Passenger.id, models.Passenger.name) 
            .filter_by(id=passenger_id, parent_user_id=user_id)
        )
        passenger = result.first()  

        if passenger:
            print(passenger.id, passenger.name)  # No lazy load expected
            passengers.append(passenger)
        else:
            raise HTTPException(404, detail=f"Passenger ID {passenger_id} invalid.")

    order_code = utils.generate_code()
    order = models.Order(code=order_code, price=flight_price, user_id=user.id)
    db.add(order)
    await db.commit()
    await db.refresh(order)
    print(passengers)
    
    tickets = []
    for passenger in passengers:
        ticket = models.Ticket(order_id=order.id,code=utils.generate_code(), flight_id=flight_id, passenger_id=passenger.id)
        tickets.append(ticket)
        db.add(ticket)

    await db.commit()
    for ticket in tickets:
        await db.refresh(ticket)

    return {
       "order_code":order_code,
    "tickets": [
        {
            "id": ticket.id,
           
            "passenger_id": ticket.passenger_id
        } 
        for ticket in tickets
    ],
        "passengers": [p.name for p in passengers],
    }




async def create_passenger(parent_user_id, name, national_id, age, gender, db: AsyncSession):
    passenger = models.Passenger(
        name=name, national_id=national_id, age=age, gender=gender, parent_user_id=parent_user_id
    )
    db.add(passenger)
    await db.commit()
    await db.refresh(passenger)
    return passenger


async def show_flights(origin_id: int, destination_id: int, departure_date: str, db: AsyncSession):
    result = await db.execute(
        select(models.Flight).filter(
            models.Flight.origin_id == origin_id,
            models.Flight.destination_id == destination_id,
            models.Flight.departure_date == departure_date,
        )
    )
    flights = result.scalars().all()

    if not flights:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No flights found")
    return flights

