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
from core.config import MODEL_CONFIG, PROJECTS_DIR, PROMPTS_DIR
from core.strings import *
from core.styles import *

# Initialize Anthropic client
client = Anthropic(api_key=MODEL_CONFIG["api_key"])

def read_project_prompt():
    """Read the project creation model prompt"""
    try:
        path = PROMPTS_DIR / "project_creation_model.txt"
        return path.read_text().strip()
    except FileNotFoundError:
        st.error(PROJECT_CREATION_PROMPT_ERROR.format(path))
        return ""

def save_project(project_name, content):
    """Save the project to a file"""
    try:
        safe_name = "".join(c for c in project_name if c.isalnum() or c in (' ', '-', '_'))
        filename = f"{safe_name}.txt"
        filepath = PROJECTS_DIR / filename
        filepath.write_text(content)
        return True
    except Exception as e:
        st.error(PROJECT_SAVE_ERROR.format(str(e)))
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

def list_projects():
    """Get list of available projects with their details"""
    projects = []
    if not PROJECTS_DIR.exists():
        st.error(PROJECTS_DIR_ERROR.format(PROJECTS_DIR))
        return projects
        
    for file in PROJECTS_DIR.glob("*.txt"):
        if file.is_file():
            content = file.read_text()
            name = next((line.replace("PROJECT SPECIFICATION:", "").strip() 
                        for line in content.split('\n') 
                        if line.startswith("PROJECT SPECIFICATION:")), "Unknown")
            objective = next((line.replace("- Primary goal: ", "").strip() 
                            for line in content.split('\n') 
                            if "Primary goal" in line), "")
            projects.append({
                "Name": name,
                "Objective": objective,
                "File": file.name,
                "Content": content,
                "Last Modified": datetime.fromtimestamp(file.stat().st_mtime)
            })
    return projects

# Initialize session states
if "creation_mode" not in st.session_state:
    st.session_state.creation_mode = False
if "project_messages" not in st.session_state:
    st.session_state.project_messages = []
if "selected_project" not in st.session_state:
    st.session_state.selected_project = None
if "creation_completed" not in st.session_state:
    st.session_state.creation_completed = False

# Custom CSS
st.markdown(COMMON_TABLE_CSS, unsafe_allow_html=True)

# Main UI
if not st.session_state.creation_mode:
    st.title(VIEW_PROJECTS_TITLE)
    
    # Display projects table
    projects = list_projects()
    if projects:
        df = pd.DataFrame(projects)
        df['Last Modified'] = df['Last Modified'].dt.strftime('%Y-%m-%d')
        
        cols = st.columns(TABLE_LAYOUTS['projects'])
        for col, header in zip(cols, [
            PROJECT_TABLE_HEADERS["name"],
            PROJECT_TABLE_HEADERS["objective"],
            PROJECT_TABLE_HEADERS["last_modified"],
            PROJECT_TABLE_HEADERS["action"]
        ]):
            col.markdown(f"<div class='table-header col-{header.lower()}'>{header}</div>", unsafe_allow_html=True)
        
        for idx, row in df.iterrows():
            cols = st.columns(TABLE_LAYOUTS['projects'])
            cols[0].markdown(f"<div class='table-cell'>{row['Name']}</div>", unsafe_allow_html=True)
            cols[1].markdown(f"<div class='table-cell'>{row['Objective']}</div>", unsafe_allow_html=True)
            cols[2].markdown(f"<div class='table-cell'>{row['Last Modified']}</div>", unsafe_allow_html=True)
            if cols[3].button(VIEW_PROJECT_BUTTON_TEXT, key=f"view_{idx}"):
                st.session_state.selected_project = row
        
        # Project viewer/editor
        if st.session_state.selected_project is not None:
            st.markdown("---")
            with st.expander(PROJECT_EXPANDER_TITLE.format(st.session_state.selected_project['Name']), expanded=True):
                if 'edit_mode' not in st.session_state:
                    st.session_state.edit_mode = False
                    
                if st.session_state.edit_mode:
                    edited_content = st.text_area(EDIT_PROJECT_LABEL, 
                                               value=st.session_state.selected_project['Content'],
                                               height=400)
                    
                    col1, col2, col3 = st.columns([1, 1, 4])
                    if col1.button(CANCEL_BUTTON, key="cancel_edit"):
                        st.session_state.edit_mode = False
                        st.rerun()
                    
                    if col2.button(SAVE_BUTTON, key="save_project"):
                        file_path = PROJECTS_DIR / st.session_state.selected_project['File']
                        try:
                            file_path.write_text(edited_content)
                            st.success(PROJECT_SAVE_SUCCESS_MESSAGE)
                            st.session_state.selected_project['Content'] = edited_content
                            st.session_state.edit_mode = False
                            st.rerun()
                        except Exception as e:
                            st.error(PROJECT_EDIT_ERROR.format(str(e)))
                else:
                    st.text(st.session_state.selected_project['Content'])
                    col1, col2, col3 = st.columns([1, 1, 4])
                    
                    if col1.button(CLOSE_BUTTON, key="close_project"):
                        st.session_state.selected_project = None
                        st.rerun()
                    
                    if col2.button(EDIT_BUTTON, key="edit_project"):
                        st.session_state.edit_mode = True
                        st.rerun()
    else:
        st.write(NO_PROJECTS_FOUND)

    # Create new project button
    if st.button(CREATE_NEW_PROJECT_BUTTON, use_container_width=True):
        st.session_state.creation_mode = True
        st.session_state.project_messages = []
        st.rerun()

else:
    # Project Creation Mode
    st.title(CREATE_PROJECT_TITLE)

    # Initialize chat with system prompt if empty
    if not st.session_state.project_messages:
        creation_prompt = read_project_prompt()
        st.session_state.project_messages = [
            {"role": "system", "content": creation_prompt}
        ]

    # Display chat messages
    for message in st.session_state.project_messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.write(message["content"])

    # Chat input
    if not st.session_state.creation_completed:
        user_input = st.chat_input(PROJECT_DESCRIPTION_PLACEHOLDER)
        
        if user_input:
            st.session_state.project_messages.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.write(user_input)
            
            response = get_ai_response(st.session_state.project_messages)
            if response:
                st.session_state.project_messages.append({"role": "assistant", "content": response})
                with st.chat_message("assistant"):
                    st.write(response)

    # Project name and save button
    if len(st.session_state.project_messages) > 2:
        st.sidebar.header(SAVE_PROJECT_HEADER)
        project_name = st.sidebar.text_input(PROJECT_NAME_LABEL, key="project_name_input")
        
        if st.sidebar.button(SAVE_PROJECT_BUTTON, use_container_width=True):
            if not project_name:
                st.sidebar.error(PROJECT_NAME_REQUIRED)
            else:
                project_content = None
                for msg in reversed(st.session_state.project_messages):
                    if msg["role"] == "assistant" and "PROJECT SPECIFICATION:" in msg["content"]:
                        project_content = msg["content"]
                        break
                
                if not project_content:
                    st.sidebar.error(NO_COMPLETE_PROJECT)
                elif save_project(project_name, project_content):
                    st.sidebar.success(PROJECT_SAVE_SUCCESS.format(project_name))
                    st.session_state.creation_completed = True
                    st.session_state.creation_mode = False
                    time.sleep(1)
                    st.rerun()

    # Cancel button to return to projects view
    if st.sidebar.button(CANCEL_CREATION_BUTTON, use_container_width=True):
        st.session_state.creation_mode = False
        st.session_state.project_messages = []
        st.session_state.creation_completed = False
        st.rerun()