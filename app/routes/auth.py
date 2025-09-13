
from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.auth import RegisterRequest, TokenResponse
from app.models.employee import create_employee
from app.db.mongo import employee_collection
from app.utils.hashing import verify_password
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import create_access_token, get_current_user
from datetime import timedelta

router = APIRouter()


# Self-registration
@router.post("/register", response_model=TokenResponse)
async def register(data: RegisterRequest):
	existing = await employee_collection.find_one({"employee_id": data.employee_id})
	if existing:
		raise HTTPException(status_code=400, detail="Employee ID already exists")
	await create_employee(data)
	token = create_access_token({"sub": data.employee_id})
	return TokenResponse(access_token=token)

@router.post("/login", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
	employee = await employee_collection.find_one({"employee_id": form_data.username})
	if not employee or not verify_password(form_data.password, employee["password_hash"]):
		raise HTTPException(status_code=401, detail="Invalid credentials")
	token = create_access_token({"sub": form_data.username})
	return TokenResponse(access_token=token)
