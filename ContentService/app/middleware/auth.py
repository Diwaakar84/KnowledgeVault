from fastapi import Request, HTTPException, Depends
from jose import jwt, JWTError
from app.config import JWT_SECRET, JWT_ALGORITHM

# Verify the current user token to check if he is an authenticated user or not 
def get_current_user(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing auth token")

    token = auth_header.split(" ")[1]

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload["sub"]
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
