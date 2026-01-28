from fastapi import Request, HTTPException
from jose import jwt, JWTError
from app.config import JWT_SECRET, JWT_ALGORITHM

# Endpoints that can be accessed without user authentication
PUBLIC_PATHS = [
    "/auth/login",
    "/auth/register",
    "/health"
]

# Function to verify the authentication header provided if valid or not
# and store the user information for the further requests from the user
async def auth_middleware(request: Request, call_next):
    path = request.url.path

    # Skip authentication for public endpoints
    if any(path.startswith(p) for p in PUBLIC_PATHS):
        return await call_next(request)

    # Check the authorization header provided in the request
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing auth token")

    token = auth_header.split(" ")[1]

    # Decode and verify the header JWT token
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        request.state.user_id = payload["sub"]
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    return await call_next(request)
