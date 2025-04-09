from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime
import uuid


class User(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    email: EmailStr
    username: str
    hashed_password: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)