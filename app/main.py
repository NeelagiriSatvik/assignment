from fastapi import FastAPI
from app.routes import employee_router, auth_router
from app.db.mongo import init_db

app = FastAPI()

async def lifespan(app):
	await init_db()
	yield

app = FastAPI(lifespan=lifespan)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(employee_router, prefix="/employees", tags=["employees"])
