import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base paths
BASE_DIR = Path(__file__).parent.resolve()
MEETINGS_DIR = BASE_DIR / "meetings"
PROMPTS_DIR = BASE_DIR / "prompts"
CUSTOMERS_DIR = PROMPTS_DIR / "customers"

# OpenAI settings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CHAT_MODEL_CONFIG = {
    "model": "gpt-4",
    "temperature": 0.7,
    "max_tokens": 1000
}

# Evaluation settings
EVALUATION_CONFIG = {
    "model": "gpt-4",
    "temperature": 0.7,
    "max_tokens": 1500
}

# Report settings
REPORT_CONFIG = {
    "model": "gpt-4",
    "temperature": 0.7,
    "max_tokens": 2000
}

# File patterns
PROFILE_EXTENSION = ".txt"
MEETING_EXTENSION = ".json"
REPORT_EXTENSION = ".txt"

# Ensure required directories exist
for directory in [MEETINGS_DIR, PROMPTS_DIR, CUSTOMERS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)