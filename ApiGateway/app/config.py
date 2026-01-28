import os
from dotenv import load_dotenv

load_dotenv()

# Fetch all the keys stored in the env
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL")
CONTENT_SERVICE_URL = os.getenv("CONTENT_SERVICE_URL")
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = "HS256"
