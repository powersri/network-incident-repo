# models.py - Pydantic models for user registration, incident creation, and response formatting
from datetime import datetime
# Literal and Optional are used for defining specific allowed values and optional fields in the models
from typing import Literal, Optional
# Pydantic is used for defining data models with validation and serialization capabilities
from pydantic import BaseModel, Field

# User registration model with username and password fields, including validation constraints
class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6, max_length=128)

# User model for storing user information in the database, including a hashed password and role
class UserInDB(BaseModel):
    username: str
    password_hash: str
    role: str = "engineer"

# Token response model for returning the access token and token type in the authentication response
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Incident creation model with fields for device name, location, incident type, severity, description, and status
class IncidentCreate(BaseModel):
    device_name: str = Field(..., min_length=1, max_length=100)
    location: str = Field(..., min_length=1, max_length=100)
    incident_type: str = Field(..., min_length=1, max_length=100)
    severity: Literal["low", "medium", "high", "critical"]
    description: str = Field(..., min_length=1, max_length=1000)
    status: Literal["open", "investigating", "resolved"]

# Incident update model with optional fields for updating existing incidents, allowing partial updates
class IncidentUpdate(BaseModel):
    device_name: Optional[str] = Field(None, min_length=1, max_length=100)
    location: Optional[str] = Field(None, min_length=1, max_length=100)
    incident_type: Optional[str] = Field(None, min_length=1, max_length=100)
    severity: Optional[Literal["low", "medium", "high", "critical"]] = None
    description: Optional[str] = Field(None, min_length=1, max_length=1000)
    status: Optional[Literal["open", "investigating", "resolved"]] = None

# Incident response model for formatting the incident data returned in API responses, including an ID field
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