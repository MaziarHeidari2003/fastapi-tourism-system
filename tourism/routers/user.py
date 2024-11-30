from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from .. import schemas, database, models, utils
from tourism.repository import user

router = APIRouter(
    tags=['User'],
    prefix='/user'
)


@router.post('/', response_model=schemas.User)
async def create_user(request: schemas.User, db: AsyncSession = Depends(database.get_db)):
    return await user.create(request, db)


@router.get("/orders", response_model=List[schemas.Order])
async def user_orders(
    current_user: models.User = Depends(utils.get_current_user),
    db: AsyncSession = Depends(database.get_db),
):
    return await user.get_user_orders(current_user, db)




# @router.post('/',response_model=schemas.User)
# def create_user(request:schemas.User,db: Session = Depends(database.get_db)):
#     return user.create(request,db)



# @router.get("/orders", response_model=list[schemas.Order])
# def user_orders(current_user: models.User = Depends(utils.get_current_user), db: Session = Depends(database.get_db)):
#     return user.get_user_orders(current_user,db) 


# @router.get('/{id}',response_model=schemas.ShowUser)
# def get_user(id:int,db: Session = Depends(database.get_db)):
#    return user.show(id,db)