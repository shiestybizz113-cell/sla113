"""
Authentication API routes.
Handles signup, login, token refresh, logout, and password management.
"""

from fastapi import APIRouter, Depends, HTTPException, Request
from typing import Optional

from models import (
    UserCreate,
    UserLogin,
    UserResponse,
    UserWithTeams,
    TokenRefresh,
    AuthResponse,
    ChangePassword,
)
from services.auth_service import (
    register_user,
    login_user,
    refresh_tokens,
    logout_user,
    get_user_with_teams,
    AuthError,
)
from core.dependencies import get_current_user, get_client_info
from core.security import hash_password, verify_password, get_token_expiry_seconds
from database import users_collection
from services.audit_service import create_audit_log


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/signup", response_model=AuthResponse)
async def signup(user_data: UserCreate, request: Request):
    """
    Register a new user account.
    
    - Creates user with hashed password
    - Creates personal team automatically
    - Returns access and refresh tokens
    """
    try:
        client_info = await get_client_info(request)
        result = await register_user(
            user_data,
            ip_address=client_info.get("ip_address"),
            user_agent=client_info.get("user_agent"),
        )
        return result
    except AuthError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.post("/login", response_model=AuthResponse)
async def login(credentials: UserLogin, request: Request):
    """
    Authenticate with email and password.
    
    Returns access token (15 min) and refresh token (7 days).
    """
    try:
        client_info = await get_client_info(request)
        result = await login_user(
            credentials,
            ip_address=client_info.get("ip_address"),
            user_agent=client_info.get("user_agent"),
        )
        return result
    except AuthError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.post("/refresh")
async def refresh(token_data: TokenRefresh, request: Request):
    """
    Refresh access token using refresh token.
    
    Returns new access and refresh token pair.
    Old refresh token is invalidated.
    """
    try:
        client_info = await get_client_info(request)
        access_token, refresh_token = await refresh_tokens(
            token_data.refresh_token,
            ip_address=client_info.get("ip_address"),
            user_agent=client_info.get("user_agent"),
        )
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": get_token_expiry_seconds(),
        }
    except AuthError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.post("/logout")
async def logout(
    request: Request,
    logout_all: bool = False,
    refresh_token: Optional[str] = None,
    user: dict = Depends(get_current_user),
):
    """
    Logout user and revoke session(s).
    
    - If refresh_token provided, revokes that specific session
    - If logout_all is True, revokes all user sessions
    """
    client_info = await get_client_info(request)
    await logout_user(
        user_id=user["_id"],
        refresh_token=refresh_token,
        logout_all=logout_all,
        ip_address=client_info.get("ip_address"),
        user_agent=client_info.get("user_agent"),
    )
    return {"message": "Logged out successfully"}


@router.get("/me", response_model=UserWithTeams)
async def get_current_user_info(user: dict = Depends(get_current_user)):
    """
    Get current authenticated user's info with team memberships.
    """
    try:
        return await get_user_with_teams(user["_id"])
    except AuthError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.put("/password")
async def change_password(
    password_data: ChangePassword,
    request: Request,
    user: dict = Depends(get_current_user),
):
    """
    Change current user's password.
    
    Requires current password for verification.
    """
    # Verify current password
    if not verify_password(password_data.current_password, user["password_hash"]):
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    
    # Update password
    new_hash = hash_password(password_data.new_password)
    await users_collection().update_one(
        {"_id": user["_id"]},
        {"$set": {"password_hash": new_hash}}
    )
    
    # Audit log
    client_info = await get_client_info(request)
    await create_audit_log(
        user_id=user["_id"],
        action="auth.password_change",
        ip_address=client_info.get("ip_address"),
        user_agent=client_info.get("user_agent"),
    )
    
    return {"message": "Password changed successfully"}


@router.get("/sessions")
async def list_sessions(user: dict = Depends(get_current_user)):
    """
    List all active sessions for current user.
    """
    from database import sessions_collection
    from datetime import datetime, timezone
    
    sessions = await sessions_collection().find({
        "user_id": user["_id"],
        "is_active": True,
        "expires_at": {"$gt": datetime.now(timezone.utc)}
    }).to_list(length=50)
    
    return [
        {
            "id": str(s["_id"]),
            "device_info": s.get("device_info"),
            "ip_address": s.get("ip_address"),
            "created_at": s["created_at"].isoformat(),
            "last_used_at": s["last_used_at"].isoformat(),
        }
        for s in sessions
    ]


@router.delete("/sessions/{session_id}")
async def revoke_session(
    session_id: str,
    request: Request,
    user: dict = Depends(get_current_user),
):
    """
    Revoke a specific session.
    """
    from database import sessions_collection
    from bson import ObjectId
    from datetime import datetime, timezone
    
    if not ObjectId.is_valid(session_id):
        raise HTTPException(status_code=400, detail="Invalid session ID")
    
    result = await sessions_collection().update_one(
        {"_id": ObjectId(session_id), "user_id": user["_id"]},
        {"$set": {"is_active": False, "revoked_at": datetime.now(timezone.utc)}}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return {"message": "Session revoked"}
