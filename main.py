import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from bson import ObjectId
from datetime import datetime

from database import db, create_document, get_documents
from schemas import Car, Booking

app = FastAPI(title="Car Rental API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Car Rental API is running"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    return response

# Utilities

def to_object_id(id_str: str) -> ObjectId:
    try:
        return ObjectId(id_str)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ObjectId")

# Seed sample cars if collection empty
@app.post("/seed")
def seed_cars():
    if db is None:
        raise HTTPException(status_code=500, detail="Database not configured")
    count = db["car"].count_documents({})
    if count > 0:
        return {"inserted": 0, "message": "Cars already seeded"}
    cars = [
        {
            "make": "Tesla", "model": "Model 3", "year": 2023, "image": "https://images.unsplash.com/photo-1549924231-f129b911e442?q=80&w=1200&auto=format&fit=crop", "daily_rate": 129, "transmission": "Automatic", "fuel": "Electric", "seats": 5, "available": True
        },
        {
            "make": "BMW", "model": "M4", "year": 2022, "image": "https://images.unsplash.com/photo-1617814074183-9110b50a2b50?q=80&w=1200&auto=format&fit=crop", "daily_rate": 159, "transmission": "Automatic", "fuel": "Gas", "seats": 4, "available": True
        },
        {
            "make": "Toyota", "model": "RAV4", "year": 2021, "image": "https://images.unsplash.com/photo-1590362891991-f776e747a588?q=80&w=1200&auto=format&fit=crop", "daily_rate": 79, "transmission": "Automatic", "fuel": "Hybrid", "seats": 5, "available": True
        },
    ]
    for c in cars:
        c["created_at"] = datetime.utcnow()
        c["updated_at"] = datetime.utcnow()
    result = db["car"].insert_many(cars)
    return {"inserted": len(result.inserted_ids)}

# Car Endpoints
@app.get("/cars")
def list_cars():
    items = get_documents("car")
    for it in items:
        it["_id"] = str(it["_id"])
    return items

@app.post("/cars")
def add_car(car: Car):
    inserted_id = create_document("car", car)
    return {"_id": inserted_id}

# Booking Endpoints
@app.post("/bookings")
def create_booking(booking: Booking):
    # Basic validation: car must exist and be available
    car_oid = to_object_id(booking.car_id)
    car = db["car"].find_one({"_id": car_oid})
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")

    # Create the booking
    data = booking.model_dump()
    data["created_at"] = datetime.utcnow()
    data["updated_at"] = datetime.utcnow()
    res = db["booking"].insert_one(data)

    return {"_id": str(res.inserted_id), "message": "Booking confirmed"}

@app.get("/bookings")
def list_bookings():
    items = get_documents("booking")
    for it in items:
        it["_id"] = str(it["_id"])
    return items

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
