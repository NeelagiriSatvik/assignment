from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

client = AsyncIOMotorClient(settings.MONGO_URI)
db = client["assessment_db"]
employee_collection = db["employees"]

# MongoDB schema validation for employees
employee_schema = {
	"bsonType": "object",
	"required": ["employee_id", "name", "department", "joining_date", "salary", "skills", "password_hash"],
	"properties": {
		"employee_id": {"bsonType": "string"},
		"name": {"bsonType": "string"},
		"department": {"bsonType": "string"},
		"joining_date": {"bsonType": "date"},
		"salary": {"bsonType": "double"},
		"skills": {"bsonType": "array", "items": {"bsonType": "string"}},
		"password_hash": {"bsonType": "string"}
	}
}

async def init_db():
	# Create collection with validation if not exists
	coll_names = await db.list_collection_names()
	if "employees" not in coll_names:
		await db.create_collection(
			"employees",
			validator={"$jsonSchema": employee_schema}
		)
	# Ensure unique index on employee_id, avoid name conflict
	indexes = await employee_collection.index_information()
	if "employee_id_unique" not in indexes:
		await employee_collection.create_index("employee_id", unique=True, name="employee_id_unique")
