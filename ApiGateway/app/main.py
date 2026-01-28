from fastapi import FastAPI
from app.routes.proxy import router as proxy_router
from app.middleware.auth import auth_middleware
from app.middleware.rate_limit import rate_limit_middleware
from starlette.middleware.base import BaseHTTPMiddleware

# Initialize the app
app = FastAPI(title="API Gateway")

# Add the auth middleware to the app
app.middleware("http")(auth_middleware)
app.include_router(proxy_router)

# Add the rate limiting middleware to the app
app.add_middleware(BaseHTTPMiddleware, dispatch=rate_limit_middleware)

# Expose a get endpoint to check if the server is running
@app.get("/health")
def health():
    return {"status": "ok"}
