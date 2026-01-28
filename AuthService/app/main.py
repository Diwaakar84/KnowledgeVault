from fastapi import FastAPI
from app.db.session import Base, engine
from app.routes.auth import router as auth_router

# Initialize the microservice
app = FastAPI(title="Auth Service")

Base.metadata.create_all(bind=engine)

# Include the router to the app
app.include_router(auth_router)

# Expose a get endpoint to check if the server is running
@app.get("/health")
def health():
    return {"status": "ok"}
