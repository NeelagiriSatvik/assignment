# FastAPI MongoDB Employee Management API

## Features
- MongoDB (Motor async driver)
- JWT authentication (python-jose)
- Password hashing (passlib)
- Pydantic models for validation
- CRUD, query, aggregation, and search APIs
- Pagination, index, schema validation
- Clean responses (hide _id)

## Project Structure
```
app/
  main.py
  models/
    employee.py
  schemas/
    employee.py
    auth.py
  routes/
    employee.py
    auth.py
  core/
    security.py
    config.py
  db/
    mongo.py
  utils/
    hashing.py
```

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start server:
   ```bash
   uvicorn app.main:app --reload
   ```
3. Configure MongoDB connection in `app/core/config.py`.

## API Endpoints
- Auth: `/auth/register`, `/auth/login`
- Employees: `/employees/...` (JWT protected)

See code for details.
