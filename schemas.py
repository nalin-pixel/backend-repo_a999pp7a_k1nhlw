"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import date

# Example schemas (replace with your own):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: EmailStr = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Car rental app schemas

class Car(BaseModel):
    """
    Cars available for rent
    Collection name: "car"
    """
    make: str = Field(..., description="Car brand, e.g., Tesla")
    model: str = Field(..., description="Model, e.g., Model 3")
    year: int = Field(..., ge=1990, le=2100, description="Model year")
    image: Optional[str] = Field(None, description="Image URL")
    daily_rate: float = Field(..., ge=0, description="Daily rental rate in USD")
    transmission: Optional[str] = Field(None, description="Automatic or Manual")
    fuel: Optional[str] = Field(None, description="Fuel type: Electric, Gas, Hybrid")
    seats: Optional[int] = Field(None, ge=1, le=9, description="Number of seats")
    available: bool = Field(True, description="Is the car currently available for rent")

class Booking(BaseModel):
    """
    Rental bookings made by customers
    Collection name: "booking"
    """
    car_id: str = Field(..., description="ID of the car being booked")
    name: str = Field(..., description="Renter full name")
    email: EmailStr = Field(..., description="Renter email")
    start_date: date = Field(..., description="Start date of rental (YYYY-MM-DD)")
    end_date: date = Field(..., description="End date of rental (YYYY-MM-DD)")
    pickup_location: Optional[str] = Field("Downtown", description="Pickup location")
    notes: Optional[str] = Field(None, description="Optional notes from renter")

# Note: The Flames database viewer will automatically:
# 1. Read these schemas from GET /schema endpoint
# 2. Use them for document validation when creating/editing
# 3. Handle all database operations (CRUD) directly
# 4. You don't need to create any database endpoints!
