from datetime import datetime, timezone

from bson import ObjectId
from bson.errors import InvalidId
from fastapi import APIRouter, Depends, HTTPException, status

from auth import get_current_user
from database import incidents_collection
from models import IncidentCreate, IncidentUpdate


router = APIRouter(tags=["Incidents"])


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


@router.get("/incidents")
def get_all_incidents():
    incidents = incidents_collection.find().sort("created_at", -1)
    return [serialize_incident(incident) for incident in incidents]


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

    return serialize_incident(new_incident)


@router.put("/incidents/{incident_id}")
def update_incident(
    incident_id: str,
    incident_update: IncidentUpdate,
    current_user: dict = Depends(get_current_user)
):
    try:
        object_id = ObjectId(incident_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid incident ID")

    existing_incident = incidents_collection.find_one({"_id": object_id})
    if not existing_incident:
        raise HTTPException(status_code=404, detail="Incident not found")

    update_data = {k: v for k, v in incident_update.model_dump().items() if v is not None}

    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided for update")

    update_data["updated_at"] = datetime.now(timezone.utc)
    update_data["updated_by"] = current_user["username"]

    incidents_collection.update_one(
        {"_id": object_id},
        {"$set": update_data}
    )

    updated_incident = incidents_collection.find_one({"_id": object_id})
    return serialize_incident(updated_incident)


@router.delete("/incidents/{incident_id}")
def delete_incident(
    incident_id: str,
    current_user: dict = Depends(get_current_user)
):
    try:
        object_id = ObjectId(incident_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid incident ID")

    existing_incident = incidents_collection.find_one({"_id": object_id})
    if not existing_incident:
        raise HTTPException(status_code=404, detail="Incident not found")

    incidents_collection.delete_one({"_id": object_id})

    return {"message": "Incident deleted successfully"}