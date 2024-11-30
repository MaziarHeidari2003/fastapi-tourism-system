from pydantic import BaseModel
from typing import List
from datetime import date

class AvailableFlights(BaseModel):
    flight_number: str
    price: float
    provider: str


class ChooseFlightRequest(BaseModel):
    parent_user_id: int
    passenger_ids: List[int] 
    flight_price: float
    flight_id: int


class TicketInUserOrders(BaseModel):
    code: str

    class Config:
        orm_mode = True    

class OrderInUserOrders(BaseModel):
    id: int
    code: str
    price: float
    tickets: list[TicketInUserOrders]  

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
    departure_date: date
    arrival_date: date
    price: float
    provider: str

    class Config:
        form_attributes = True

class TicketResponse(BaseModel):
    id: int
    order_id: int
    flight_id: int
    passenger_id: int

    class Config:
        from_attributes = True  
        
class OrderResponse(BaseModel):
    id: int
    code: str
    price: float
    user_id: int

    class Config:
        from_attributes = True  
        

class ReserveFlightResponse(BaseModel):
    order: OrderResponse
    tickets: List[TicketResponse]
    passengers: List[str]
