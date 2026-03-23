from datetime import datetime
from typing import Literal, Optional
from pydantic import BaseModel, Field


class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6, max_length=128)


class UserInDB(BaseModel):
    username: str
    password_hash: str
    role: str = "engineer"


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class IncidentCreate(BaseModel):
    device_name: str = Field(..., min_length=1, max_length=100)
    location: str = Field(..., min_length=1, max_length=100)
    incident_type: str = Field(..., min_length=1, max_length=100)
    severity: Literal["low", "medium", "high", "critical"]
    description: str = Field(..., min_length=1, max_length=1000)
    status: Literal["open", "investigating", "resolved"]


class IncidentUpdate(BaseModel):
    device_name: Optional[str] = Field(None, min_length=1, max_length=100)
    location: Optional[str] = Field(None, min_length=1, max_length=100)
    incident_type: Optional[str] = Field(None, min_length=1, max_length=100)
    severity: Optional[Literal["low", "medium", "high", "critical"]] = None
    description: Optional[str] = Field(None, min_length=1, max_length=1000)
    status: Optional[Literal["open", "investigating", "resolved"]] = None


class IncidentResponse(BaseModel):
    id: str
    device_name: str
    location: str
    incident_type: str
    severity: Literal["low", "medium", "high", "critical"]
    description: str
    status: Literal["open", "investigating", "resolved"]
    created_at: datetime
    updated_at: datetime