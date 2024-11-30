from jose import jwt, JWTError
from typing import List
from fastapi import Depends,status,HTTPException,Response
from sqlalchemy.orm import Session
from .oauth2 import oauth2_scheme
from . import database,models



def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    try:
        payload = jwt.decode(token, "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7", algorithms=["HS256"])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = db.query(models.User).filter(models.User.username == username).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")


import uuid

def generate_code():
    code = str(uuid.uuid4()).replace('-', '').upper()[:6]
    return code