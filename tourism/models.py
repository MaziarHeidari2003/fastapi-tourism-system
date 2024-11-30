from sqlalchemy import Column, Integer, String, ForeignKey, Float,DATE
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True,index=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)    
    orders = relationship('Order', back_populates='user')
    passengers = relationship('Passenger', back_populates='user')

class Passenger(Base):
    __tablename__ = 'passengers'
    id = Column(Integer, primary_key=True,index=True)
    name = Column(String, nullable=False)
    national_id = Column(String, unique=True, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)
    parent_user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='passengers')

    # Passengers have multiple tickets
    tickets = relationship('Ticket', back_populates='passenger')

class Airport(Base):
    __tablename__ = 'airports'
    id = Column(Integer, primary_key=True,index=True)
    name = Column(String, nullable=False)
    code = Column(String, unique=True, nullable=False)

class Flight(Base):
    __tablename__ = 'flights'    
    id = Column(Integer, primary_key=True,index=True)
    flight_number = Column(String, unique=True, nullable=False)
    origin_id = Column(Integer, ForeignKey('airports.id'), nullable=False)
    destination_id = Column(Integer, ForeignKey('airports.id'), nullable=False)
    departure_date = Column(DATE, nullable=False)
    arrival_date = Column(DATE, nullable=False)
    price = Column(Float, nullable=False)
    provider = Column(String, nullable=False)
    origin = relationship('Airport', foreign_keys=[origin_id])
    destination = relationship('Airport', foreign_keys=[destination_id])
    tickets = relationship('Ticket', back_populates='flight')

class Order(Base):
    __tablename__ = 'orders'    
    id = Column(Integer, primary_key=True,index=True)
    code = Column(String, unique=True, nullable=False)
    price = Column(Float, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('User', back_populates='orders')
    tickets = relationship('Ticket', back_populates='order')
      
    def __repr__(self):
        return self.code
class Ticket(Base):
    __tablename__ = 'tickets'
    id = Column(Integer, primary_key=True,index=True)
    passenger_id = Column(Integer, ForeignKey('passengers.id'), nullable=False)
    code = Column(String, unique=True, nullable=False)
    flight_id = Column(Integer, ForeignKey('flights.id'), nullable=False)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    passenger = relationship('Passenger', back_populates='tickets')
    flight = relationship('Flight', back_populates='tickets')
    order = relationship('Order', back_populates='tickets')
