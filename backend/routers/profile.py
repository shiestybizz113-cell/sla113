"""
User Profile API endpoints.

Provides:
- Change password
- View active sessions
- Logout specific session
- Logout all sessions
- Get profile details with memberships
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import datetime, timezone
import bcrypt
import re

from core.dependencies import get_current_user
from database import users_collection, sessions_collection, memberships_collection, teams_collection

router = APIRouter(prefix="/profile", tags=["Profile"])


class ChangePasswordRequest(BaseModel):
    current_password: str = Field(..., min_length=1)
    new_password: str = Field(..., min_length=8)
    
    @field_validator('new_password')
    @classmethod
    def validate_new_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'[0-9]', v):
            raise ValueError('Password must contain at least one number')
        return v


class SessionResponse(BaseModel):
    id: str
    created_at: str
    expires_at: str
    is_current: bool
    user_agent: Optional[str] = None
    ip_address: Optional[str] = None


class ProfileResponse(BaseModel):
    id: str
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    system_role: str
    created_at: str
    teams: List[dict]


@router.get("/me", response_model=ProfileResponse)
async def get_profile(current_user: dict = Depends(get_current_user)):
    """Get current user's full profile with team memberships."""
    user_id = current_user["id"]
    
    # Get user details
    user = await users_collection().find_one(
        {"id": user_id},
        {"_id": 0, "hashed_password": 0}
    )
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get all memberships
    memberships = await memberships_collection().find(
        {"user_id": user_id},
        {"_id": 0}
    ).to_list(100)
    
    # Get team details for each membership
    teams = []
    for membership in memberships:
        team = await teams_collection().find_one(
            {"id": membership["team_id"]},
            {"_id": 0}
        )
        if team:
            teams.append({
                "id": team["id"],
                "name": team["name"],
                "type": team.get("type", "organization"),
                "role": membership["role"],
                "joined_at": membership.get("created_at", "")
            })
    
    return ProfileResponse(
        id=user["id"],
        email=user["email"],
        first_name=user.get("first_name"),
        last_name=user.get("last_name"),
        system_role=user.get("system_role", "user"),
        created_at=user.get("created_at", ""),
        teams=teams
    )


@router.post("/change-password")
async def change_password(
    request: ChangePasswordRequest,
    current_user: dict = Depends(get_current_user)
):
    """Change the current user's password."""
    user_id = current_user["id"]
    
    # Get user with password
    user = await users_collection().find_one({"id": user_id})
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Verify current password
    if not bcrypt.checkpw(
        request.current_password.encode('utf-8'),
        user["hashed_password"].encode('utf-8')
    ):
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    
    # Check new password is different
    if request.current_password == request.new_password:
        raise HTTPException(status_code=400, detail="New password must be different from current password")
    
    # Hash new password
    new_hashed = bcrypt.hashpw(
        request.new_password.encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')
    
    # Update password
    await users_collection().update_one(
        {"id": user_id},
        {"$set": {
            "hashed_password": new_hashed,
            "updated_at": datetime.now(timezone.utc).isoformat()
        }}
    )
    
    return {"message": "Password changed successfully"}


@router.get("/sessions", response_model=List[SessionResponse])
async def get_sessions(
    current_user: dict = Depends(get_current_user),
    current_session_id: Optional[str] = None
):
    """Get all active sessions for the current user."""
    user_id = current_user["id"]
    
    # Get all sessions
    sessions = await sessions_collection().find(
        {
            "user_id": user_id,
            "expires_at": {"$gt": datetime.now(timezone.utc).isoformat()}
        },
        {"_id": 0}
    ).to_list(100)
    
    # Get current session ID from user context if available
    current_sess_id = current_user.get("session_id", current_session_id)
    
    return [
        SessionResponse(
            id=s["id"],
            created_at=s.get("created_at", ""),
            expires_at=s.get("expires_at", ""),
            is_current=s["id"] == current_sess_id if current_sess_id else False,
            user_agent=s.get("user_agent"),
            ip_address=s.get("ip_address")
        )
        for s in sessions
    ]


@router.delete("/sessions/{session_id}")
async def revoke_session(
    session_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Revoke a specific session."""
    user_id = current_user["id"]
    
    # Verify session belongs to user
    session = await sessions_collection().find_one({
        "id": session_id,
        "user_id": user_id
    })
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Delete session
    await sessions_collection().delete_one({"id": session_id})
    
    return {"message": "Session revoked successfully"}


@router.delete("/sessions")
async def revoke_all_sessions(
    current_user: dict = Depends(get_current_user),
    keep_current: bool = True
):
    """Revoke all sessions for the current user."""
    user_id = current_user["id"]
    current_session_id = current_user.get("session_id")
    
    # Build query
    query = {"user_id": user_id}
    
    # Optionally keep current session
    if keep_current and current_session_id:
        query["id"] = {"$ne": current_session_id}
    
    # Delete sessions
    result = await sessions_collection().delete_many(query)
    
    return {
        "message": f"Revoked {result.deleted_count} session(s)",
        "count": result.deleted_count
    }
