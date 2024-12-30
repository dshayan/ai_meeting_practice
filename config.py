# Imports
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base paths
BASE_DIR = Path(__file__).parent
MEETINGS_DIR = BASE_DIR / "meetings"
PROMPTS_DIR = BASE_DIR / "prompts"
CUSTOMERS_DIR = BASE_DIR / "customers"

# File extensions
PROFILE_EXTENSION = ".txt"
MEETING_EXTENSION = ".json"
REPORT_EXTENSION = ".txt"

# API Keys
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Model configurations
ANTHROPIC_MODELS = {
    "chat": {
        "model": "claude-3-5-sonnet-latest",
        "temperature": 0.7,
        "max_tokens": 1000
    },
    "evaluation": {
        "model": "claude-3-5-sonnet-latest",
        "temperature": 0.7,
        "max_tokens": 1500
    },
    "report": {
        "model": "claude-3-5-sonnet-latest",
        "temperature": 0.7,
        "max_tokens": 2000
    }
}

OPENAI_MODELS = {
    "chat": {
        "model": "gpt-4o",
        "temperature": 0.7,
        "max_tokens": 1000
    },
    "evaluation": {
        "model": "gpt-4o",
        "temperature": 0.7,
        "max_tokens": 1500
    },
    "report": {
        "model": "gpt-4o",
        "temperature": 0.7,
        "max_tokens": 2000
    }
}

def get_active_config():
    """Get active model configurations based on available API keys"""
    if ANTHROPIC_API_KEY:
        return {
            "provider": "anthropic",
            "api_key": ANTHROPIC_API_KEY,
            "chat": ANTHROPIC_MODELS["chat"],
            "evaluation": ANTHROPIC_MODELS["evaluation"],
            "report": ANTHROPIC_MODELS["report"]
        }
    elif OPENAI_API_KEY:
        return {
            "provider": "openai",
            "api_key": OPENAI_API_KEY,
            "chat": OPENAI_MODELS["chat"],
            "evaluation": OPENAI_MODELS["evaluation"],
            "report": OPENAI_MODELS["report"]
        }
    else:
        raise ValueError("No API keys found. Please set either ANTHROPIC_API_KEY or OPENAI_API_KEY in your .env file")

# Active configuration
MODEL_CONFIG = get_active_config()

# Create directories if they don't exist
MEETINGS_DIR.mkdir(exist_ok=True)
PROMPTS_DIR.mkdir(exist_ok=True)
CUSTOMERS_DIR.mkdir(exist_ok=True)