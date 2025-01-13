# Imports
import sys
from pathlib import Path
import streamlit as st
from anthropic import Anthropic
from datetime import datetime
import pandas as pd
import json
import time

# Add the project root directory to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# Import from core
from core.config import MODEL_CONFIG, CUSTOMERS_DIR, PROMPTS_DIR, PROFILE_EXTENSION
from core.strings import *
from core.styles import *

# Initialize Anthropic client
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
        safe_name = "".join(c for c in profile_name if c.isalnum() or c in (' ', '-', '_'))
        filename = f"{safe_name}{PROFILE_EXTENSION}"
        filepath = CUSTOMERS_DIR / filename
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

def list_customer_profiles():
    """Get list of available customer profiles with their details"""
    profiles = []
    if not CUSTOMERS_DIR.exists():
        st.error(CUSTOMERS_DIR_ERROR.format(CUSTOMERS_DIR))
        return profiles
        
    for file in CUSTOMERS_DIR.glob(f"*{PROFILE_EXTENSION}"):
        if file.is_file():
            content = file.read_text()
            name = next((line.replace("Name:", "").strip() 
                        for line in content.split('\n') 
                        if line.startswith("Name:")), "Unknown")
            role = next((line.replace("Role:", "").strip() 
                        for line in content.split('\n') 
                        if line.startswith("Role:")), "")
            profiles.append({
                "Name": name,
                "Role": role,
                "File": file.name,
                "Content": content,
                "Last Modified": datetime.fromtimestamp(file.stat().st_mtime)
            })
    return profiles

# Initialize session states
if "creation_mode" not in st.session_state:
    st.session_state.creation_mode = False
if "profile_messages" not in st.session_state:
    st.session_state.profile_messages = []
if "selected_profile" not in st.session_state:
    st.session_state.selected_profile = None
if "creation_completed" not in st.session_state:
    st.session_state.creation_completed = False

# Custom CSS
st.markdown(COMMON_TABLE_CSS, unsafe_allow_html=True)

# Main UI
if not st.session_state.creation_mode:
    st.title(VIEW_PROFILES_TITLE)
    
    # Display profiles table
    profiles = list_customer_profiles()
    if profiles:
        df = pd.DataFrame(profiles)
        df['Last Modified'] = df['Last Modified'].dt.strftime('%Y-%m-%d')
        
        cols = st.columns(TABLE_LAYOUTS['profiles'])
        for col, header in zip(cols, [
            PROFILE_TABLE_HEADERS["name"],
            PROFILE_TABLE_HEADERS["role"],
            PROFILE_TABLE_HEADERS["last_modified"],
            PROFILE_TABLE_HEADERS["action"]
        ]):
            col.markdown(f"<div class='table-header col-{header.lower()}'>{header}</div>", unsafe_allow_html=True)
        
        for idx, row in df.iterrows():
            cols = st.columns(TABLE_LAYOUTS['profiles'])
            cols[0].markdown(f"<div class='table-cell'>{row['Name']}</div>", unsafe_allow_html=True)
            cols[1].markdown(f"<div class='table-cell'>{row['Role']}</div>", unsafe_allow_html=True)
            cols[2].markdown(f"<div class='table-cell'>{row['Last Modified']}</div>", unsafe_allow_html=True)
            if cols[3].button(VIEW_PROFILE_BUTTON_TEXT, key=f"view_{idx}"):
                st.session_state.selected_profile = row
        
        # Profile viewer/editor
        if st.session_state.selected_profile is not None:
            st.markdown("---")
            with st.expander(PROFILE_EXPANDER_TITLE.format(st.session_state.selected_profile['Name']), expanded=True):
                if 'edit_mode' not in st.session_state:
                    st.session_state.edit_mode = False
                    
                if st.session_state.edit_mode:
                    edited_content = st.text_area(EDIT_PROFILE_LABEL, 
                                               value=st.session_state.selected_profile['Content'],
                                               height=400)
                    
                    col1, col2, col3 = st.columns([1, 1, 4])
                    if col1.button(CANCEL_BUTTON, key="cancel_edit"):
                        st.session_state.edit_mode = False
                        st.rerun()
                    
                    if col2.button(SAVE_BUTTON, key="save_profile"):
                        file_path = CUSTOMERS_DIR / st.session_state.selected_profile['File']
                        try:
                            file_path.write_text(edited_content)
                            st.success(PROFILE_SAVE_SUCCESS_MESSAGE)
                            st.session_state.selected_profile['Content'] = edited_content
                            st.session_state.edit_mode = False
                            st.rerun()
                        except Exception as e:
                            st.error(PROFILE_EDIT_ERROR.format(str(e)))
                else:
                    st.text(st.session_state.selected_profile['Content'])
                    col1, col2, col3 = st.columns([1, 1, 4])
                    
                    if col1.button(CLOSE_BUTTON, key="close_profile"):
                        st.session_state.selected_profile = None
                        st.rerun()
                    
                    if col2.button(EDIT_BUTTON, key="edit_profile"):
                        st.session_state.edit_mode = True
                        st.rerun()
    else:
        st.write(NO_PROFILES_FOUND)

    # Create new profile button
    if st.button(CREATE_NEW_PROFILE_BUTTON, use_container_width=True):
        st.session_state.creation_mode = True
        st.session_state.profile_messages = []
        st.rerun()

else:
    # Profile Creation Mode
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
            st.session_state.profile_messages.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.write(user_input)
            
            response = get_ai_response(st.session_state.profile_messages)
            if response:
                st.session_state.profile_messages.append({"role": "assistant", "content": response})
                with st.chat_message("assistant"):
                    st.write(response)

    # Profile name and save button
    if len(st.session_state.profile_messages) > 2:
        st.sidebar.header(SAVE_PROFILE_HEADER)
        profile_name = st.sidebar.text_input(PROFILE_NAME_LABEL, key="profile_name_input")
        
        if st.sidebar.button(SAVE_PROFILE_BUTTON, use_container_width=True):
            if not profile_name:
                st.sidebar.error(PROFILE_NAME_REQUIRED)
            else:
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
                    st.session_state.creation_mode = False
                    time.sleep(1)
                    st.rerun()

    # Cancel button to return to profiles view
    if st.sidebar.button(CANCEL_CREATION_BUTTON, use_container_width=True):
        st.session_state.creation_mode = False
        st.session_state.profile_messages = []
        st.session_state.creation_completed = False
        st.rerun()