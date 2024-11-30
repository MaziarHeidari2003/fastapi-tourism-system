from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm

from .. import schemas, database, models, token
from ..hashing import Hash

router = APIRouter(
    tags=['Authentication']
)

@router.post('/login')
async def login(request: schemas.Login, db: AsyncSession = Depends(database.get_db)):
    stmt = select(models.User).where(models.User.username == request.username)
    result = await db.execute(stmt)
    user = result.scalars().first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid credentials"
        )

    if not Hash.verify(user.password, request.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Password not right"
        )

    access_token_expires = timedelta(minutes=30)
    access_token = token.create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires,
    )

    return {"access_token": access_token, "token_type": "bearer"}
