from beanie import Document, Indexed
from pydantic import Field, EmailStr
from datetime import datetime

class User(Document):
    username: Indexed(str, unique=True)
    email: Indexed(EmailStr, unique=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        collection = "users"

