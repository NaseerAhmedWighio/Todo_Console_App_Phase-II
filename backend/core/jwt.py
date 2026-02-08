"""JWT utilities for Todo App backend."""
from datetime import datetime, timedelta
from typing import Optional
import jwt
from fastapi import HTTPException, status
from passlib.context import CryptContext
from .config import settings


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)
# Password hashing context
# Configure bcrypt with proper settings to handle the 72-byte limitation gracefully
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Secret key for JWT encoding/decoding
# Use the Better Auth secret for validation (since Better Auth generates the tokens)
SECRET_KEY = settings.better_auth_secret if settings.better_auth_secret != "your-better-auth-secret-change-in-production" else settings.secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against its hash."""
    # For bcrypt compatibility, we need to truncate the password to 72 bytes before verification
    # since bcrypt only considers the first 72 bytes during hashing
    password_str = str(plain_password)

    # Convert to bytes to properly measure byte length
    password_bytes = password_str.encode('utf-8')

    # Truncate to 72 bytes to ensure bcrypt compatibility
    if len(password_bytes) > 72:
        # Find the proper cut-off point to avoid breaking multi-byte characters
        truncated_bytes = password_bytes[:72]
        # Decode with error handling to avoid issues with truncated multi-byte characters
        password_str = truncated_bytes.decode('utf-8', errors='ignore')
    else:
        password_str = password_bytes.decode('utf-8')

    return pwd_context.verify(password_str, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password."""
    # In a Better Auth integration, the password hashing is typically handled by Better Auth
    # However, if we need to store passwords locally, we'll hash them
    password_str = str(password)

    # Convert to bytes to properly measure byte length
    password_bytes = password_str.encode('utf-8')

    # For short passwords (under 72 bytes), use them directly
    # For longer ones, truncate to 72 bytes to ensure bcrypt compatibility
    if len(password_bytes) <= 72:
        safe_password = password_str
    else:
        print(f"Warning: Password longer than 72 bytes ({len(password_bytes)}), truncating for bcrypt compatibility.")
        # Find the proper cut-off point to avoid breaking multi-byte characters
        truncated_bytes = password_bytes[:72]
        # Decode with error handling to avoid issues with truncated multi-byte characters
        safe_password = truncated_bytes.decode('utf-8', errors='ignore')

    try:
        return pwd_context.hash(safe_password)
    except Exception as e:
        # Catch any bcrypt-related errors
        error_msg = str(e)
        print(f"Bcrypt error: {error_msg}")

        # If we still have an issue, try one more fallback approach
        try:
            # Use the character-level approach as a last resort
            fallback_password = password_str[:50] if len(password_str) > 50 else password_str
            return pwd_context.hash(fallback_password)
        except Exception as final_error:
            print(f"All attempts failed: {final_error}")
            # If all else fails, raise a clear error
            raise ValueError("Password could not be processed. Please try a different password.")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create an access token with expiration."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """Decode an access token and return its payload."""
    try:
        # Use the Better Auth secret for validation (since Better Auth generates the tokens)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None