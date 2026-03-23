# incidents.py - API endpoints for managing incidents in the PowerNAS system
from datetime import datetime, timezone

# bson is used for handling MongoDB ObjectIds and related errors
from bson import ObjectId
# InvalidId is raised when an invalid ObjectId string is provided
from bson.errors import InvalidId
# FastAPI imports for creating API routes, handling dependencies, and managing HTTP exceptions
from fastapi import APIRouter, Depends, HTTPException, status

# Local imports for authentication, database access, and data models
from auth import get_current_user
# database import incidents_collection
from database import incidents_collection
# models for creating and updating incidents
from models import IncidentCreate, IncidentUpdate

# Create an API router for incidents with the tag "Incidents"
router = APIRouter(tags=["Incidents"])

# Helper function to serialize MongoDB incident documents into a format suitable for API responses
def serialize_incident(incident: dict) -> dict:
    return {
        "id": str(incident["_id"]),
        "device_name": incident["device_name"],
        "location": incident["location"],
        "incident_type": incident["incident_type"],
        "severity": incident["severity"],
        "description": incident["description"],
        "status": incident["status"],
        "created_at": incident["created_at"],
        "updated_at": incident["updated_at"],
    }

# API endpoint to retrieve all incidents, sorted by creation date in descending order
@router.get("/incidents")
def get_all_incidents():
    incidents = incidents_collection.find().sort("created_at", -1)
    return [serialize_incident(incident) for incident in incidents]


# API endpoint to retrieve a specific incident by its ID
@router.get("/incidents/{incident_id}")
def get_incident_by_id(incident_id: str):
    try:
        object_id = ObjectId(incident_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid incident ID")

    incident = incidents_collection.find_one({"_id": object_id})
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")

    return serialize_incident(incident)

# API endpoint to create a new incident, requiring authentication and returning the created incident
@router.post("/incidents", status_code=status.HTTP_201_CREATED)
def create_incident(
    incident: IncidentCreate,
    current_user: dict = Depends(get_current_user)
):
    now = datetime.now(timezone.utc)

    incident_data = {
        "device_name": incident.device_name,
        "location": incident.location,
        "incident_type": incident.incident_type,
        "severity": incident.severity,
        "description": incident.description,
        "status": incident.status,
        "created_at": now,
        "updated_at": now,
        "created_by": current_user["username"],
    }

    result = incidents_collection.insert_one(incident_data)
    new_incident = incidents_collection.find_one({"_id": result.inserted_id})

    return serialize_incident(new_incident) # Return the newly created incident in the response

# API endpoint to update an existing incident by its ID, requiring authentication and returning the updated incident
@router.put("/incidents/{incident_id}")
def update_incident(
    incident_id: str,
    incident_update: IncidentUpdate,
    current_user: dict = Depends(get_current_user)
):
    try: # Validate the incident ID and convert it to an ObjectId
        object_id = ObjectId(incident_id)
    except InvalidId: # If the ID is invalid, raise a 400 Bad Request error
        raise HTTPException(status_code=400, detail="Invalid incident ID")

    existing_incident = incidents_collection.find_one({"_id": object_id})
    if not existing_incident:
        raise HTTPException(status_code=404, detail="Incident not found")

    update_data = {k: v for k, v in incident_update.model_dump().items() if v is not None}

    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided for update")

    update_data["updated_at"] = datetime.now(timezone.utc)
    update_data["updated_by"] = current_user["username"]

# Update the incident in the database with the new data
    incidents_collection.update_one(
        {"_id": object_id},
        {"$set": update_data}
    )
# Retrieve the updated incident from the database and return it in the response
    updated_incident = incidents_collection.find_one({"_id": object_id})
    return serialize_incident(updated_incident)

# API endpoint to delete an incident by its ID, requiring authentication and returning a success message
@router.delete("/incidents/{incident_id}")
def delete_incident(
    incident_id: str,
    current_user: dict = Depends(get_current_user)
):
    try: # Validate the incident ID and convert it to an ObjectId
        object_id = ObjectId(incident_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid incident ID")

# Check if the incident exists before attempting to delete it
    existing_incident = incidents_collection.find_one({"_id": object_id})
    if not existing_incident:
        raise HTTPException(status_code=404, detail="Incident not found")

    incidents_collection.delete_one({"_id": object_id})

    return {"message": "Incident deleted successfully"}