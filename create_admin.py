from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
from datetime import datetime

# Update these values as needed
MONGO_URI = "mongodb://localhost:27017"
ADMIN_ID = "admin1"
ADMIN_PASSWORD = "adminpassword"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def create_admin():
    client = AsyncIOMotorClient(MONGO_URI)
    db = client["assessment_db"]
    employee_collection = db["employees"]
    password_hash = pwd_context.hash(ADMIN_PASSWORD)
    admin_doc = {
        "employee_id": ADMIN_ID,
        "name": "Admin User",
        "department": "HR",
        "joining_date": datetime(2023, 1, 1),
        "salary": 100000.0,
        "skills": ["Management"],
        "password_hash": password_hash,
        "role": "admin"
    }
    existing = await employee_collection.find_one({"employee_id": ADMIN_ID})
    if not existing:
        await employee_collection.insert_one(admin_doc)
        print("Admin user created.")
    else:
        print("Admin user already exists.")

if __name__ == "__main__":
    import asyncio
    asyncio.run(create_admin())
