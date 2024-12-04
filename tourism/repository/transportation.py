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
    # proocesses the result of a query and returns a single value of obj
    #  you can even use scalars to have collection of scalar values
    # or i could use scalar_one() => raises exception when more that one result is found
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




async def create_passenger(name, national_id, age, gender,parent_user, db: AsyncSession):
    passenger = models.Passenger(
        name=name, national_id=national_id, age=age, gender=gender, parent_user_id=parent_user.id
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

#This part is the something like the show_flight function but with the usage
# of caching . It had some errors I couldn't resolve so I had comment it!


# import httpx
# import asyncio
# import aioredis
# import json

# redis = aioredis.from_url("redis://localhost")

# PROVIDERS = [
#     "https://provider1.com/flights",
#     "https://provider2.com/flights"
# ]

# # to be  honest i used chatgpt for this part. Right now I understand what is happening 
# # but the implementation is not mine!

# async def fetch_flights_from_provider(url: str, params: dict):
#     async with httpx.AsyncClient(timeout=10) as client:
#         try:
#             response = await client.get(url, params=params)
#             response.raise_for_status() 
#             return response.json()
#         except httpx.RequestError as e:
#             return {"error": f"Failed to fetch from {url}: {str(e)}"}
#         except httpx.HTTPStatusError as e:
#             return {"error": f"Provider error: {str(e)}"}

# async def get_cached_flights(key: str):
#     cached_data = await redis.get(key)
#     if cached_data:
#         return json.loads(cached_data)
#     return None

# async def cache_flights(key: str, data: list, ttl: int = 3600):
#     await redis.setex(key, ttl, json.dumps(data))

# async def show_flights(origin_id: int, destination_id: int, departure_date: str):
#     params = {
#         "origin_id": origin_id,
#         "destination_id": destination_id,
#         "departure_date": departure_date,
#     }
#     # Generate a unique cache key based on params
#     cache_key = f"flights_{origin_id}_{destination_id}_{departure_date}"

#     # Check Redis cache
#     cached_flights = await get_cached_flights(cache_key)
#     if cached_flights:
#         return cached_flights

#     # Fetch from providers if not in cache
#     tasks = [fetch_flights_from_provider(url, params) for url in PROVIDERS]
#     try:
#         responses = await asyncio.gather(*tasks)
#     except:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Endpoints may be wrong")
    
#     flights = []
#     for response in responses:
#         if isinstance(response, dict) and "error" in response:
#             continue
#         flights.extend(response)
    
#     if not flights:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No flights found")
    
#     # Cache the fetched flights
#     await cache_flights(cache_key, flights)

#     return flights







# create task in asyncronous 
# design pattern
# providers and other 
# runnig nmultiple workers in one project while using django

# how to use multiple frameworks in one project => search
# log the requests and the time of each reaquest and see what happens to the time of the response when the users increase

# load test!!!