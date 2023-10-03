import os
from dotenv import load_dotenv

load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL", "")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS", "")
PROVIDER = os.getenv("PROVIDER", "")
