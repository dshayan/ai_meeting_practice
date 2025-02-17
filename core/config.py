# Imports
import os
from pathlib import Path
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

# Base paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
PROJECTS_DIR = DATA_DIR / "projects"
MEETINGS_DIR = DATA_DIR / "meetings"
MEETING_EVALUATIONS_DIR = DATA_DIR / "meeting_evaluations"
RESPONSE_EVALUATIONS_DIR = DATA_DIR / "response_evaluations"
STRATEGIES_DIR = DATA_DIR / "strategies"
PROMPTS_DIR = BASE_DIR / "prompts"
CUSTOMERS_DIR = BASE_DIR / "customers"

# Create directories if they don't exist (with parents=True)
PROJECTS_DIR.mkdir(parents=True, exist_ok=True)
MEETINGS_DIR.mkdir(parents=True, exist_ok=True)
MEETING_EVALUATIONS_DIR.mkdir(parents=True, exist_ok=True)
RESPONSE_EVALUATIONS_DIR.mkdir(parents=True, exist_ok=True)
STRATEGIES_DIR.mkdir(parents=True, exist_ok=True)
PROMPTS_DIR.mkdir(parents=True, exist_ok=True)
CUSTOMERS_DIR.mkdir(parents=True, exist_ok=True)
# File extensions
PROJECT_EXTENSION = ".txt"
PROFILE_EXTENSION = ".txt"
MEETING_EXTENSION = ".json"
REPORT_EXTENSION = ".txt"

# API Key - Check environment variables first, then Streamlit secrets
ANTHROPIC_API_KEY = (
    os.getenv("ANTHROPIC_API_KEY") or       # Local .env file
    st.secrets.get("ANTHROPIC_API_KEY", None)  # Streamlit Cloud secrets
)

if not ANTHROPIC_API_KEY:
    st.error("ANTHROPIC_API_KEY not found. Please add it to your .env file locally or Streamlit secrets in cloud.")
    st.stop()

# Model configurations
MODEL_CONFIG = {
    "provider": "anthropic",
    "api_key": ANTHROPIC_API_KEY,
    "chat": {
        "model": "claude-3-5-sonnet-latest",
        "temperature": 0.8,
        "max_tokens": 500
    },
    "response_evaluation": {
        "model": "claude-3-5-sonnet-latest",
        "temperature": 1.0,
        "max_tokens": 1000
    },
    "meeting_evaluation": {
        "model": "claude-3-5-sonnet-latest",
        "temperature": 1.0,
        "max_tokens": 2000
    },
    "strategy": {
        "model": "claude-3-5-sonnet-latest",
        "temperature": 0.7,
        "max_tokens": 1500
    }
}