import os
from dotenv import load_dotenv

load_dotenv()

# Fetch all the keys stored in the env
DATABASE_URL = os.getenv("DATABASE_URL")
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = "HS256"
