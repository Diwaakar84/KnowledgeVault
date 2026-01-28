from fastapi import FastAPI
from app.db.session import Base, engine
from app.routes.notes import router as notes_router

# Initialize the microservice
app = FastAPI(title="Content Service")

Base.metadata.create_all(bind=engine)

# Include the router to the app
app.include_router(notes_router)

# Expose a get endpoint to check if the server is running
@app.get("/health")
def health():
    return {"status": "ok"}
