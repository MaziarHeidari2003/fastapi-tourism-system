from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .. import models, schemas, hashing
from fastapi import HTTPException

async def create(request: schemas.User, db: AsyncSession):
    new_user = models.User(
        name=request.name,
        username=request.username,
        phone_number=request.phone_number,
        password=hashing.Hash.bcrypt(request.password),
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user



from sqlalchemy.future import select
from sqlalchemy.orm import selectinload 
# it is a part of the eagerloading techniques helping two load the related data in a seperate query
# options modifies the query by adding query-specific configurations 
# it comes in handy while using selectinjoinT joinedloadT subqueryload 

async def get_user_orders(current_user, db: AsyncSession):
    result = await db.execute(
        select(models.Order)
        .options(selectinload(models.Order.tickets))  # Example: Eagerly load related tickets
        .filter(models.Order.user_id == current_user.id)
    )
    orders = result.scalars().all()
    
    if not orders:
        raise HTTPException(status_code=404, detail="No orders found for the current user")
    
    return orders



# async def get_user_orders(current_user, db: AsyncSession):
#     result = await db.execute(select(models.Order).filter(models.Order.user_id == current_user.id))
#     orders = result.scalars().all()
    
#     if not orders:
#         raise HTTPException(status_code=404, detail="No orders found for the current user")
    
#     return orders




# def create(request: schemas.User, db:Session):
#     new_user = models.User(name=request.name,username=request.username,phone_number=request.phone_number,password=hashing.Hash.bcrypt(request.password))
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user


# def get_user_orders(current_user,db):
#     orders = db.query(models.Order).filter(models.Order.user_id == current_user.id).all()
#     if not orders:
#         raise HTTPException(status_code=404, detail="No orders found for the current user")
#     return orders



# def show(id:int, db:Session):
#     user = db.query(models.User).filter(models.User.id == id).first() 
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                                 detail=f"User with {id} not found")

#     return user