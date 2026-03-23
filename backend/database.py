# database.py - MongoDB connection and collections setup for network incident reporting backend
import os
from dotenv import load_dotenv # Load environment variables from .env file
from pymongo import MongoClient # MongoDB client for database connection
from pymongo.errors import ConnectionFailure # Exception for handling connection failures

# Load environment variables from .env file
load_dotenv()

# MongoDB connection parameters from environment variables
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "network_incidents_db")

# Ensure MONGO_URI is set, otherwise raise an error
if not MONGO_URI:
    raise ValueError("MONGO_URI is not set in the .env file.")

# Initialize MongoDB client and database connection
client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# Define collections for users and incidents
users_collection = db["users"]
incidents_collection = db["incidents"]

# Function to check MongoDB connection
def check_db_connection() -> bool:
    try: # Attempt to ping the MongoDB server to check connection
        client.admin.command("ping")
        return True
    except ConnectionFailure: # If connection fails, catch the exception and return False
        return False