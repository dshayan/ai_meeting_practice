import streamlit as st
from anthropic import Anthropic
from datetime import datetime
from pathlib import Path
import json
import time

from core.config import MODEL_CONFIG, CUSTOMERS_DIR, PROMPTS_DIR, PROFILE_EXTENSION
from core.strings import *

client = Anthropic(api_key=MODEL_CONFIG["api_key"])

def read_creation_prompt():
    """Read the customer creation model prompt"""
    try:
        path = PROMPTS_DIR / "customer_creation_model.txt"
        return path.read_text().strip()
    except FileNotFoundError:
        st.error(PROFILE_CREATION_PROMPT_ERROR.format(path))
        return ""

def save_customer_profile(profile_name, content):
    """Save the customer profile to a file"""
    try:
        # Sanitize profile name and create filename
        safe_name = "".join(c for c in profile_name if c.isalnum() or c in (' ', '-', '_'))
        filename = f"{safe_name}{PROFILE_EXTENSION}"
        filepath = CUSTOMERS_DIR / filename
        
        # Write content to file
        filepath.write_text(content)
        return True
    except Exception as e:
        st.error(PROFILE_SAVE_ERROR.format(str(e)))
        return False

def get_ai_response(messages):
    """Get response from Claude API"""
    try:
        config = MODEL_CONFIG["chat"].copy()
        
        response = client.messages.create(
            model=config["model"],
            max_tokens=config["max_tokens"],
            temperature=config["temperature"],
            messages=[
                {
                    "role": "assistant" if msg["role"] == "assistant" else "user",
                    "content": msg["content"]
                }
                for msg in messages
            ]
        )
        
        return response.content[0].text if response.content else ""
    except Exception as e:
        st.error(API_CALL_ERROR.format(str(e)))
        return None

# Initialize session state
if "profile_messages" not in st.session_state:
    st.session_state.profile_messages = []
    st.session_state.profile_name = ""
    st.session_state.creation_completed = False

st.title(CREATE_PROFILE_TITLE)

# Initialize chat with system prompt if empty
if not st.session_state.profile_messages:
    creation_prompt = read_creation_prompt()
    st.session_state.profile_messages = [
        {"role": "system", "content": creation_prompt}
    ]

# Display chat messages
for message in st.session_state.profile_messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.write(message["content"])

# Chat input
if not st.session_state.creation_completed:
    user_input = st.chat_input(PROFILE_DESCRIPTION_PLACEHOLDER)
    
    if user_input:
        # Add user message
        st.session_state.profile_messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)
        
        # Get AI response
        response = get_ai_response(st.session_state.profile_messages)
        if response:
            st.session_state.profile_messages.append({"role": "assistant", "content": response})
            with st.chat_message("assistant"):
                st.write(response)

# Profile name and save button
if len(st.session_state.profile_messages) > 2:  # If there's been some conversation
    st.sidebar.header(SAVE_PROFILE_HEADER)
    profile_name = st.sidebar.text_input(PROFILE_NAME_LABEL, key="profile_name_input")
    
    if st.sidebar.button(SAVE_PROFILE_BUTTON, use_container_width=True):
        if not profile_name:
            st.sidebar.error(PROFILE_NAME_REQUIRED)
        else:
            # Extract the last complete profile from assistant
            profile_content = None
            for msg in reversed(st.session_state.profile_messages):
                if msg["role"] == "assistant" and "CUSTOMER PROFILE:" in msg["content"]:
                    profile_content = msg["content"]
                    break
            
            if not profile_content:
                st.sidebar.error(NO_COMPLETE_PROFILE)
            elif save_customer_profile(profile_name, profile_content):
                st.sidebar.success(PROFILE_SAVE_SUCCESS.format(profile_name))
                st.session_state.creation_completed = True
                st.session_state.profile_name = profile_name
                
                # Add a small delay before redirecting
                time.sleep(1)
                st.switch_page("💬_Meet.py")

# Reset button
if st.sidebar.button(CREATE_NEW_PROFILE_BUTTON, use_container_width=True):
    st.session_state.profile_messages = []
    st.session_state.profile_name = ""
    st.session_state.creation_completed = False
    st.rerun()