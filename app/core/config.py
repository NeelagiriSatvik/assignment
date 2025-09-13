from pydantic_settings import BaseSettings

class Settings(BaseSettings):
	MONGO_URI: str = "mongodb://localhost:27017"
	JWT_SECRET_KEY: str = "your_jwt_secret"
	JWT_ALGORITHM: str = "HS256"
	ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

settings = Settings()
