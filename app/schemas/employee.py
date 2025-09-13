from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

class EmployeeBase(BaseModel):
	employee_id: str = Field(..., example="E123")
	name: str
	department: str
	joining_date: date
	salary: float
	skills: List[str]

class EmployeeCreate(EmployeeBase):
	password: str

class EmployeeUpdate(BaseModel):
	name: Optional[str]
	department: Optional[str]
	joining_date: Optional[date]
	salary: Optional[float]
	skills: Optional[List[str]]

class EmployeeResponse(EmployeeBase):
	model_config = {
		"from_attributes": True,
		"json_schema_extra": {
			"example": {
				"employee_id": "E123",
				"name": "John Doe",
				"department": "IT",
				"joining_date": "2022-01-01",
				"salary": 50000,
				"skills": ["Python", "FastAPI"]
			}
		}
	}
