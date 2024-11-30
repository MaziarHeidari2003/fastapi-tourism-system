# Here I  want to write about the challenges and solutions

**MissingGreenlet while using asyncronous code**

- This was my code

```python 

async def reserve_flight_for_passengers(user_id, passenger_ids, flight_price, flight_id, db: AsyncSession):
    user = await db.execute(select(models.User).filter_by(id=user_id))
    user = user.scalar()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with {user_id} not found")

    passengers = []
    for passenger_id in passenger_ids:
        result = await db.execute(select(models.Passenger).filter_by(id=passenger_id, user_id=user_id))
        passenger = result.scalar()

        if passenger:
            print(passenger.id)  # Access ID safely if passenger is fetched.
        else:
            print(f"Passenger with {passenger_id} not found.")
            raise HTTPException(404, detail=f"Passenger with ID {passenger_id} does not exist.")
        passengers.append(passenger)

    # order_code = f"ORD{str(len(user.orders) + 1)}"
    order_code = utils.generate_code()
    order = models.Order(code=order_code, price=flight_price, user_id=user.id)
    db.add(order)
    await db.commit()
    await db.refresh(order)

    tickets = []
    for passenger in passengers:
        print(111)
        print(passenger.id)
        ticket = models.Ticket(order_id=order.id, flight_id=flight_id, passenger_id=2)
        tickets.append(ticket)
        db.add(ticket)

    await db.commit()
    await db.refresh(order)

    return {
        "order": order,
        "tickets": tickets,
        "passengers": [passenger.name for passenger in passengers],
    }


```

- And it was solved by this code

```python


async def reserve_flight_for_passengers(user_id, passenger_ids, flight_price, flight_id, db: AsyncSession):
    user_result = await db.execute(select(models.User).filter_by(id=user_id))
    user = user_result.scalar()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with {user_id} not found")

    passengers = []
    for passenger_id in passenger_ids:
        result = await db.execute(
            select(models.Passenger.id, models.Passenger.name) 
            .filter_by(id=passenger_id, user_id=user_id)
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
        ticket = models.Ticket(order_id=order.id, flight_id=flight_id, passenger_id=passenger.id)
        tickets.append(ticket)
        db.add(ticket)

    await db.commit()

    return {
        "order": order,
        "tickets": tickets,
        "passengers": [p.name for p in passengers]
    }

```