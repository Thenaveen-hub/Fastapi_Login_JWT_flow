import time
from typing import Dict
import jwt
from passlib.context import CryptContext

# Configuration
JWT_SECRET = "your_secret_key"
JWT_ALGORITHM = "HS256"

# We use bcrypt for hashing. 
# Note: Bcrypt has a hard 72-byte limit for inputs.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """
    Hashes the password. 
    We truncate to 72 chars to prevent the internal ValueError.
    """
    # Truncate to 72 characters before hashing
    safe_password = password[:72]
    return pwd_context.hash(safe_password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain text password against a stored hash.
    Includes a try-except to prevent the 500 error if the hash is malformed.
    """
    try:
        # We must truncate here too so it matches the signup logic
        return pwd_context.verify(plain_password[:72], hashed_password)
    except Exception as e:
        print(f"Hashing Verification Error: {e}")
        return False

def signJWT(user_id: str) -> Dict[str, str]:
    """Generates a JWT token and sets token_type for the schema."""
    payload = {
        "user_id": user_id,
        "expires": time.time() + 3600 
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    # Match the 'Token' schema in schemas.py
    return {"access_token": token, "token_type": "bearer"}