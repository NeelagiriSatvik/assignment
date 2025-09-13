from fastapi import APIRouter, Depends, HTTPException, status, Query
from app.schemas.employee import EmployeeCreate, EmployeeUpdate, EmployeeResponse
from app.models.employee import create_employee, get_employee_by_id, update_employee, delete_employee
from app.db.mongo import employee_collection
from app.core.security import get_current_user
from typing import List, Optional

router = APIRouter()


# Create employee
@router.post("/", response_model=EmployeeResponse, status_code=201)
async def create(data: EmployeeCreate, user=Depends(get_current_user)):
	existing = await employee_collection.find_one({"employee_id": data.employee_id})
	if existing:
		raise HTTPException(status_code=400, detail="Employee ID already exists")
	employee = await create_employee(data)
	return employee


# Average salary grouped by department
from pydantic import BaseModel

class DepartmentAverageSalary(BaseModel):
	department: str
	average_salary: float

@router.get("/average-salary", response_model=List[DepartmentAverageSalary])
async def average_salary_by_department(user=Depends(get_current_user)):
	pipeline = [
		{"$group": {
			"_id": "$department",
			"average_salary": {"$avg": "$salary"}
		}}
	]
	results = await employee_collection.aggregate(pipeline).to_list(length=None)
	return [DepartmentAverageSalary(department=r["_id"], average_salary=r["average_salary"]) for r in results]

# Search employees by skill
@router.get("/search", response_model=List[EmployeeResponse])
async def search(skill: str, user=Depends(get_current_user)):
	# Normalize skill for case-insensitive search
	normalized_skill = skill.strip().lower()
	cursor = employee_collection.find({"skills": {"$elemMatch": {"$regex": f"^{normalized_skill}$", "$options": "i"}}})
	employees = [emp async for emp in cursor]
	if not employees:
		return []
	return [
		{
			"employee_id": emp["employee_id"],
			"name": emp["name"],
			"department": emp["department"],
			"joining_date": emp["joining_date"].strftime("%Y-%m-%d"),
			"salary": emp["salary"],
			"skills": emp["skills"]
		}
		for emp in employees
	]

# Get employee by ID
@router.get("/{employee_id}", response_model=EmployeeResponse)
async def get(employee_id: str, user=Depends(get_current_user)):
	employee = await get_employee_by_id(employee_id)
	if not employee:
		raise HTTPException(status_code=404, detail="Employee not found")
	return employee

# Update employee
@router.put("/{employee_id}", response_model=EmployeeResponse)
async def update(employee_id: str, data: EmployeeUpdate, user=Depends(get_current_user)):
	# Fetch current employee data first
	current_employee = await get_employee_by_id(employee_id)
	if not current_employee:
		raise HTTPException(status_code=404, detail="Employee not found")
	updated_employee = await update_employee(employee_id, data)
	if not updated_employee:
		raise HTTPException(status_code=404, detail="Employee not updated")
	# Add header to indicate partial update support
	from fastapi import Response
	response = Response()
	response.headers["X-Partial-Update-Supported"] = "true"
	return updated_employee

# Delete employee
@router.delete("/{employee_id}", status_code=204)
async def delete(employee_id: str, user=Depends(get_current_user)):
	deleted = await delete_employee(employee_id)
	if not deleted:
		raise HTTPException(status_code=404, detail="Employee not found")

# List employees by department, sorted by joining_date desc, with pagination
@router.get("/", response_model=List[EmployeeResponse])
async def list_employees(
	department: Optional[str] = Query(None),
	skip: int = 0,
	limit: int = 10,
	user=Depends(get_current_user)
):
	query = {"department": department} if department else {}
	cursor = employee_collection.find(query).sort("joining_date", -1).skip(skip).limit(limit)
	employees = [emp async for emp in cursor]
	return [
		{
			"employee_id": emp["employee_id"],
			"name": emp["name"],
			"department": emp["department"],
			"joining_date": emp["joining_date"].strftime("%Y-%m-%d"),
			"salary": emp["salary"],
			"skills": emp["skills"]
		}
		for emp in employees
	]
