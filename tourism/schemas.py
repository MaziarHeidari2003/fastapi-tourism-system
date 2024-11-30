from pydantic import BaseModel
from typing import Optional,List
from datetime import datetime

from pydantic import BaseModel


class ShowAirport(BaseModel):
    name: str
    class Config:
        orm_mode = True


class AvailableFlights(BaseModel):
    flight_number: str
    price: float
    provider: str


class ChooseFlightRequest(BaseModel):
    user_id: int
    passenger_ids: List[int] 
    flight_price: float
    flight_id: int


class Ticket(BaseModel):
    id: int

    class Config:
        orm_mode = True    

class Order(BaseModel):
    id: int
    code: str
    price: float
    tickets: list[Ticket]  

    class Config:
        orm_mode = True

class Passengers(BaseModel):
    name: str
    national_id: str




class User(BaseModel):
    name: str
    phone_number: str
    password: str
    username: str


class Airport(BaseModel):
    name: str
    code: str


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None
    scopes: list[str] = []


class Flight(BaseModel):
    flight_number: str
    origin_id: int
    destination_id: int
    departure_date: datetime
    arrival_date: datetime
    price: float
    provider: str

    class Config:
        orm_mode = True

