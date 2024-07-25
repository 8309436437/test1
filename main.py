from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from pydantic_settings import BaseSettings
from models.user import User
from pydantic import BaseModel, EmailStr
from fastapi.staticfiles import StaticFiles

class Settings(BaseSettings):
    mongodb_url: str = "mongodb://localhost:27017"

settings = Settings()

app = FastAPI()

class UserCreate(BaseModel):
    username: str
    email: EmailStr

@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(settings.mongodb_url)
    app.mongodb = app.mongodb_client["test_database"]
    await init_beanie(database=app.mongodb, document_models=[User])

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()

@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI application!"}

@app.post("/users/", response_model=User)
async def create_user(user: UserCreate):
    user_dict = user.dict()
    user_doc = User(**user_dict)
    await user_doc.insert()
    return user_doc

# Mount the static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

