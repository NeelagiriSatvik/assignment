from app.db.mongo import employee_collection
from app.schemas.employee import EmployeeCreate, EmployeeUpdate
from app.utils.hashing import hash_password
from bson import ObjectId
from datetime import datetime

def employee_helper(employee: dict) -> dict:
	return {
		"employee_id": employee["employee_id"],
		"name": employee["name"],
		"department": employee["department"],
		"joining_date": employee["joining_date"].strftime("%Y-%m-%d"),
		"salary": employee["salary"],
		"skills": employee["skills"]
	}

async def create_employee(data: EmployeeCreate):
	employee = data.dict()
	employee["joining_date"] = datetime.strptime(employee["joining_date"], "%Y-%m-%d")
	employee["password_hash"] = hash_password(employee.pop("password"))
	result = await employee_collection.insert_one(employee)
	return employee_helper(employee)

async def get_employee_by_id(employee_id: str):
	employee = await employee_collection.find_one({"employee_id": employee_id})
	if employee:
		return employee_helper(employee)
	return None

async def update_employee(employee_id: str, data: EmployeeUpdate):
		update_data = {k: v for k, v in data.dict(exclude_unset=True).items()}
		if "joining_date" in update_data:
			jd = update_data["joining_date"]
			if isinstance(jd, str):
				try:
					# Try ISO format first
					dt = datetime.fromisoformat(jd)
				except Exception:
					try:
						dt = datetime.strptime(jd, "%Y-%m-%d")
					except Exception:
						dt = None
				update_data["joining_date"] = dt
			elif isinstance(jd, datetime):
				update_data["joining_date"] = jd
			elif hasattr(jd, "year") and hasattr(jd, "month") and hasattr(jd, "day"):
				# Convert date to datetime
				update_data["joining_date"] = datetime(jd.year, jd.month, jd.day)
		result = await employee_collection.update_one({"employee_id": employee_id}, {"$set": update_data})
		if result.modified_count:
			employee = await employee_collection.find_one({"employee_id": employee_id})
			return employee_helper(employee)
		return None

async def delete_employee(employee_id: str):
	result = await employee_collection.delete_one({"employee_id": employee_id})
	return result.deleted_count > 0
