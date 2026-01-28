from fastapi import Request
from fastapi.responses import JSONResponse
from app.cache.redis_client import redis_client

RATE_LIMIT = 100          # requests
WINDOW_SECONDS = 60      # per minute

async def rate_limit_middleware(request: Request, call_next):
    # Identify caller (prefer user_id from auth middleware, fallback to IP)
    user_id = request.state.user_id if hasattr(request.state, "user_id") else None
    identifier = user_id or request.client.host

    key = f"rate:{identifier}"

    try:
        # Increement the count for key, create a new one if not present
        current = redis_client.incr(key)

        # 1 denotes the key was just created thus set the window to expire after the specified time
        if current == 1:
            redis_client.expire(key, WINDOW_SECONDS)

        # Greater than the rate limit means we should fail the user request
        # and notify the user to try after the timer is reset 
        if current > RATE_LIMIT:
            ttl = redis_client.ttl(key)
            return JSONResponse(
                status_code=429,
                content={
                    "detail": "Rate limit exceeded",
                    "retry_after_seconds": ttl
                }
            )

    except Exception as e:
        # Fail open: do NOT block traffic if Redis is down
        print("⚠️ Rate limit Redis error:", e)

    response = await call_next(request)
    return response
