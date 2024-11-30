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

The key changes in the second piece of code that resolved the MissingGreenlet issue are:

1. Explicitly Selecting Columns
In the second code:

```python

result = await db.execute(
    select(models.Passenger.id, models.Passenger.name).filter_by(id=passenger_id, user_id=user_id)
)
passenger = result.first()
```

Here, only the required fields (id and name) are explicitly selected. This ensures that no lazy loading is triggered, as only these specific columns are fetched immediately from the database.

2. Avoiding Full Object Fetch
In the original code:

```python
result = await db.execute(select(models.Passenger).filter_by(id=passenger_id, user_id=user_id))
passenger = result.scalar()
This fetched the entire Passenger object, which includes lazy-loaded relationships or deferred columns, leading to the MissingGreenlet error when accessing those fields.
```

By selecting specific columns in the second code, you bypass lazy-loading and directly fetch only the data you need.

3. Using first() Instead of scalar()
In the second code:

```python

passenger = result.first()

```
This method safely extracts the first row of the query without returning a coroutine object, avoiding potential async context issues.

**Why It Works:**

Eager Loading: Ensures data is fully loaded during query execution, avoiding access to unloaded fields.
Safer Field Access: By explicitly selecting fields, you reduce the chances of lazy-loading errors in async environments.