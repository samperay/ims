import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    ENVIRONMENT = os.getenv("ENVIRONMENT", "dev")

    # Database configuration
    DATABASE_URL = os.getenv("DATABASE_URL_DEV") if ENVIRONMENT == "dev" else os.getenv("DATABASE_URL_PROD")
    
config = Config()