"""
Better Auth Integration for Todo App Backend
This module integrates Better Auth with the existing backend system.
"""
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from typing import Optional, Dict, Any
import json
import os
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from core.config import settings
from sqlmodel import Session, select
from models.user import User
from services.user_service import UserService
from database.session import get_session
from core.jwt import create_access_token, decode_access_token

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def setup_better_auth_routes(app: FastAPI):
    """
    Setup Better Auth compatible routes
    """

    # Helper function for session implementation
    async def _get_session_impl(request: Request, session: Session):
        try:
            # Extract token from Authorization header or cookies
            token = None
            
            # First, try to get token from Authorization header
            auth_header = request.headers.get('authorization')
            if auth_header and auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
            
            # If not in header, try to get from cookies (using Better Auth's expected cookie name)
            if not token:
                token = request.cookies.get('better-auth-session') or request.cookies.get('access_token') or request.cookies.get('token')
            
            if not token:
                return JSONResponse({"data": None})

            # Decode the token
            payload = decode_access_token(token)
            if not payload or 'sub' not in payload:
                return JSONResponse({"data": None})

            user_id = payload['sub']

            # Get user from database
            user_service = UserService(session)
            user_data = user_service.get_user_by_id(user_id)

            if not user_data:
                return JSONResponse({"data": None})

            # Return session data
            access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)

            return JSONResponse({
                "data": {
                    "user": {
                        "id": user_data.id,
                        "email": user_data.email,
                        "name": user_data.name,
                    },
                    "token": token,
                    "expires": (datetime.utcnow() + access_token_expires).isoformat()
                }
            })

        except Exception as e:
            return JSONResponse({"data": None})

    # Sign up endpoint - compatible with Better Auth
    @app.post("/api/auth/sign-up/email")
    async def better_auth_signup(request: Request, session: Session = Depends(get_session)):
        data = await request.json()
        email = data.get('email')
        password = data.get('password')
        name = data.get('name', '')

        if not email or not password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email and password are required"
            )

        user_service = UserService(session)

        try:
            # Use the existing user creation method
            from schemas.user import UserCreate
            user_data = UserCreate(email=email, password=password, name=name or email.split('@')[0])

            # Create user through the existing service
            created_user = user_service.create_user(user_data)

            # Create a JWT token (similar to what Better Auth would do)
            access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
            access_token = create_access_token(
                data={"sub": created_user.id}, expires_delta=access_token_expires
            )

            response = JSONResponse({
                "data": {
                    "user": {
                        "id": created_user.id,
                        "email": created_user.email,
                        "name": created_user.name,
                    },
                    "token": access_token,
                    "expires": (datetime.utcnow() + access_token_expires).isoformat()
                }
            })
            
            # Set the token in cookies for Better Auth compatibility
            # Use the same cookie name that Better Auth expects
            response.set_cookie(
                key="better-auth-session",
                value=access_token,
                httponly=True,
                secure=False,  # Set to True in production with HTTPS
                samesite="lax",
                max_age=access_token_expires.total_seconds()  # Use the same expiration as the token
            )
            
            return response

        except HTTPException as e:
            # Re-raise HTTP exceptions with their details
            raise e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Registration failed: {str(e)}"
            )

    # Sign in endpoint - compatible with Better Auth
    @app.post("/api/auth/sign-in/credentials")
    async def better_auth_signin(request: Request, session: Session = Depends(get_session)):
        data = await request.json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email and password are required"
            )

        user_service = UserService(session)

        try:
            # Authenticate user through the existing service
            authenticated_user = user_service.authenticate_user(email, password)

            if not authenticated_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid email or password"
                )

            # Create a JWT token (similar to what Better Auth would do)
            access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
            access_token = create_access_token(
                data={"sub": authenticated_user.id}, expires_delta=access_token_expires
            )

            # Create response with proper headers for Better Auth
            response = JSONResponse({
                "data": {
                    "user": {
                        "id": authenticated_user.id,
                        "email": authenticated_user.email,
                        "name": authenticated_user.name,
                    },
                    "token": access_token,
                    "expires": (datetime.utcnow() + access_token_expires).isoformat()
                }
            })
            
            # Set the token in cookies for Better Auth compatibility
            # Use the same cookie name that Better Auth expects
            response.set_cookie(
                key="better-auth-session",
                value=access_token,
                httponly=True,
                secure=False,  # Set to True in production with HTTPS
                samesite="lax",
                max_age=access_token_expires.total_seconds()  # Use the same expiration as the token
            )
            
            return response

        except HTTPException as e:
            # Re-raise HTTP exceptions with their details
            raise e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Login failed: {str(e)}"
            )

    # Get session endpoint - compatible with Better Auth (support both GET and POST)
    @app.post("/api/auth/get-session")
    async def better_auth_get_session_post(request: Request, session: Session = Depends(get_session)):
        return await _get_session_impl(request, session)

    @app.get("/api/auth/get-session")
    async def better_auth_get_session_get(request: Request, session: Session = Depends(get_session)):
        return await _get_session_impl(request, session)

    # Sign out endpoint - compatible with Better Auth
    @app.post("/api/auth/sign-out")
    async def better_auth_signout():
        # For a stateless JWT system, sign out is mostly client-side
        # Clear the cookie for Better Auth compatibility
        response = JSONResponse({
            "data": {}
        })
        response.set_cookie(
            key="better-auth-session",
            value="",
            httponly=True,
            max_age=0,  # Expire immediately
            samesite="lax"
        )
        return response

def integrate_better_auth(app: FastAPI):
    """
    Integrate Better Auth with the FastAPI application
    """
    setup_better_auth_routes(app)
    return app

print("Better Auth integration module created successfully.")
print("This module provides Better Auth-compatible endpoints for the frontend.")