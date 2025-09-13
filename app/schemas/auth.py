from pydantic import BaseModel, EmailStr

class RegisterRequest(BaseModel):
	employee_id: str
	name: str
	department: str
	joining_date: str
	salary: float
	skills: list[str]
	password: str
	model_config = {
		"json_schema_extra": {
			"example": {
				"employee_id": "123",
				"name": "John Doe",
				"department": "IT",
				"joining_date": "2023-01-01",
				"salary": 50000,
				"skills": ["Python", "FastAPI"],
				"password": "yourpassword"
			}
		}
	}

class LoginRequest(BaseModel):
	employee_id: str
	password: str
	model_config = {
		"json_schema_extra": {
			"example": {
				"employee_id": "123",
				"password": "yourpassword"
			}
		}
	}

class TokenResponse(BaseModel):
	access_token: str
	token_type: str = "bearer"
	model_config = {
		"json_schema_extra": {
			"example": {
				"access_token": "abc123",
				"token_type": "bearer"
			}
		}
	}
