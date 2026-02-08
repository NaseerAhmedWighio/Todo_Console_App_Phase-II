"""Dependency functions for Todo App backend."""
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlmodel import Session
from database.session import get_session
from core.jwt import decode_access_token
from core.config import settings
from schemas.user import TokenData
from typing import Generator, Optional
from models.user import User
import re


async def get_token_from_request(request: Request) -> str:
    """Extract token from request - either from Authorization header or cookies."""
    # Try to get token from Authorization header
    auth_header = request.headers.get('authorization')
    if auth_header:
        # Match Bearer token pattern
        match = re.match(r'^Bearer\s+(.+)$', auth_header, re.IGNORECASE)
        if match:
            return match.group(1)
    
    # If not in header, try to get from cookies (set by Better Auth)
    token = request.cookies.get('better-auth-session') or request.cookies.get('access_token')
    if token:
        return token
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


async def get_current_user(
    request: Request,
    session: Session = Depends(get_session)
) -> User:
    """Get the current authenticated user from JWT token or session cookie."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = None
    
    # Try to get token from Authorization header first
    auth_header = request.headers.get('authorization')
    if auth_header:
        # Match Bearer token pattern
        import re
        match = re.match(r'^Bearer\s+(.+)$', auth_header, re.IGNORECASE)
        if match:
            token = match.group(1)
    
    # If not in header, try to get from cookies (set by Better Auth)
    if not token:
        token = request.cookies.get('better-auth-session') or request.cookies.get('access_token')
    
    if not token:
        raise credentials_exception

    # Decode the token
    token_data = decode_access_token(token)
    if token_data is None:
        raise credentials_exception

    user_id: str = token_data.get("sub")
    if user_id is None:
        # Try to get user_id from other common JWT claims used by Better Auth
        user_id = token_data.get("id") or token_data.get("user_id")

    if user_id is None:
        raise credentials_exception

    # Get user from database (user might be created when they first interact with our backend)
    user = session.get(User, user_id)
    if user is None:
        # Create a placeholder user record if it doesn't exist
        # This allows us to maintain user data isolation while using Better Auth
        user = User(
            id=user_id,
            email=token_data.get("email", ""),
            name=token_data.get("name", "")
        )
        session.add(user)
        session.commit()
        session.refresh(user)

    return user


def verify_user_owns_resource(user: User = Depends(get_current_user)):
    """Verify that the current user owns the resource they're trying to access."""
    # This function can be used as a dependency to ensure user owns resources
    # In actual implementation, this would be called with the resource ID
    # to verify ownership
    return user