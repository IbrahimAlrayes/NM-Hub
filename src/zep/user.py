import asyncio
import logging
from zep_python import ZepClient, Session
from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, List
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_URL = "http://localhost:8000"

class UserRequest(BaseModel):
    user_id: str
    email: EmailStr
    first_name: str
    last_name: str
    metadata: Optional[Dict] = None

class SessionRequest(BaseModel):
    user_id: str
    session_data: Dict


def get_client() -> ZepClient:
    return ZepClient(API_URL)

# User Management
async def create_user(request: UserRequest) -> None:
    async with get_client() as client:
        try:
            await client.user.aadd(request)
            logger.info("User created successfully.")
        except Exception as e:
            logger.error(f"Error creating user: {e}")

async def get_user(user_id: str) -> Optional[Dict]:
    async with get_client() as client:
        try:
            return await client.user.aget(user_id)
        except Exception as e:
            logger.error(f"Error fetching user: {e}")
            return None

async def get_all_users() -> Optional[List[Dict]]:
    async with get_client() as client:
        try:
            return await client.user.alist()
        except Exception as e:
            logger.error(f"Error fetching users: {e}")
            return None

async def update_user(request: UserRequest) -> None:
    async with get_client() as client:
        try:
            await client.user.aupdate(request)
            logger.info("User updated successfully.")
        except Exception as e:
            logger.error(f"Error updating user: {e}")

async def delete_user(user_id: str) -> None:
    async with get_client() as client:
        try:
            await client.user.adelete(user_id)
            logger.info("User deleted successfully.")
        except Exception as e:
            logger.error(f"Error deleting user: {e}")

# Session Management
async def add_session(user_id: str, metadata: dict = {}) -> None:
    async with get_client() as client:
        session_id = uuid.uuid4().hex
        session = Session(
            session_id=session_id,
            user_id=user_id,
            metadata=metadata
        )
        try:
            await client.memory.aadd_session(session)
            logger.info(f"Session added successfully with ID: {session_id}")
        except Exception as e:
            logger.error(f"Error adding session: {e}")

async def get_session(session_id: str) -> Optional[Dict]:
    async with get_client() as client:
        try:
            return await client.memory.aget_session(session_id)
        except Exception as e:
            logger.error(f"Error fetching session: {e}")
            return None

async def get_all_session_messages(session_id: str) -> None:
    async with get_client() as client:
        try:
            messages = await client.message.aget_session_messages(session_id)
            for message in messages:
                logger.info(message.to_dict())
        except Exception as e:
            logger.error(f"Error fetching session messages: {e}")
