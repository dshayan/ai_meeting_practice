import sys
from pathlib import Path
import json
from datetime import datetime
import streamlit as st
from anthropic import Anthropic

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from core.strings import *
from core.styles import *
from core.config import (
    MODEL_CONFIG, MEETINGS_DIR, MEETING_EVALUATIONS_DIR, RESPONSE_EVALUATIONS_DIR,
    PROMPTS_DIR, CUSTOMERS_DIR, PROFILE_EXTENSION, MEETING_EXTENSION, REPORT_EXTENSION
)

# Initialize Anthropic client
client = Anthropic(api_key=MODEL_CONFIG["api_key"])

def format_timestamp(format="%Y%m%d_%H%M%S"):
    """Centralized timestamp formatting"""
    return datetime.now().strftime(format)

def parse_timestamp(timestamp_str, input_format="%Y%m%d_%H%M%S", output_format="%Y-%m-%d"):
    """Parse timestamp string to desired format"""
    try:
        dt = datetime.strptime(timestamp_str, input_format)
        return dt.strftime(output_format)
    except ValueError:
        # Fallback for legacy timestamps
        try:
            dt = datetime.strptime(timestamp_str, "%y%m%d_%H%M%S")
            return dt.strftime(output_format)
        except ValueError:
            return "Unknown Date"

def safe_file_operation(operation, *args, error_message=None, **kwargs):
    """Centralized file operation handling"""
    try:
        return operation(*args, **kwargs)
    except Exception as e:
        st.error(error_message.format(str(e)) if error_message else str(e))
        return None

def read_prompt(filename, is_customer=False):
    """Read prompt from file"""
    path = CUSTOMERS_DIR if is_customer else PROMPTS_DIR
    filepath = path / f"{filename}{PROFILE_EXTENSION}"
    return safe_file_operation(
        lambda: filepath.read_text().strip(),
        error_message=PROMPT_FILE_ERROR.format(filepath)
    ) or ""

def display_customer_profiles_table():
    """Display customer profiles in a table format"""
    if not CUSTOMERS_DIR.exists():
        st.error(CUSTOMERS_DIR_ERROR.format(CUSTOMERS_DIR))
        return None

    profiles = sorted(
        [f.stem for f in CUSTOMERS_DIR.glob(f"*{PROFILE_EXTENSION}") if f.is_file()]
    )
    
    if not profiles:
        st.write(NO_PROFILES_FOUND)
        return None

    # Create columns with predefined layout
    cols = st.columns(TABLE_LAYOUTS['meet'])

    # Table headers with consistent styling
    for col, header in zip(cols, [
        PROFILE_TABLE_HEADERS['name'],
        PROFILE_TABLE_HEADERS['role'],
        PROFILE_TABLE_HEADERS['last_modified'],
        PROFILE_TABLE_HEADERS['action']
    ]):
        col.markdown(f"<div class='table-header col-{header.lower()}'>{header}</div>", unsafe_allow_html=True)

    # Display profiles
    for idx, profile in enumerate(profiles):
        content = read_prompt(profile, is_customer=True)
        name = next((line.replace("Name:", "").strip() 
                    for line in content.split('\n') 
                    if line.startswith("Name:")), "Unknown")
        role = next((line.replace("Role:", "").strip() 
                    for line in content.split('\n') 
                    if line.startswith("Role:")), "")
        
        last_modified = format_timestamp("%Y-%m-%d")
        
        cols = st.columns(TABLE_LAYOUTS['meet'])
        cols[0].markdown(f"<div class='profile-cell'>{name}</div>", unsafe_allow_html=True)
        cols[1].markdown(f"<div class='profile-cell'>{role}</div>", unsafe_allow_html=True)
        cols[2].markdown(f"<div class='profile-cell'>{last_modified}</div>", unsafe_allow_html=True)
        
        if cols[3].button("Meet", key=f"meet_{idx}"):
            return profile
    
    return None

def save_meeting(profile_name):
    """Save current meeting to file"""
    timestamp = getattr(st.session_state, 'current_meeting_timestamp', format_timestamp())
    
    meeting_data = {
        'customer_profile': profile_name or "Unknown Customer",
        'conversation': [
            {
                'role': msg['role'],
                'content': msg['content'],
                'timestamp': format_timestamp("%Y-%m-%d %H:%M:%S")
            }
            for msg in st.session_state.messages if msg['role'] != 'system'
        ],
        'vendor_evaluations': st.session_state.evaluations,
        'meeting_start': timestamp,
        'customer_model': st.session_state.customer_model,
        'response_evaluation_model': st.session_state.response_evaluation_model,
        'meeting_evaluation_model': st.session_state.meeting_evaluation_model
    }
    
    filename = MEETING_FILENAME.format(profile_name, timestamp, MEETING_EXTENSION)
    filepath = MEETINGS_DIR / filename
    
    if safe_file_operation(
        filepath.write_text,
        json.dumps(meeting_data, indent=2),
        error_message=MEETING_SAVE_ERROR
    ):
        st.session_state.current_meeting_filename = filename
        st.session_state.current_meeting_timestamp = timestamp
        return filename
    return None

def save_evaluation(evaluation, profile_name):
    """Save evaluation to file"""
    timestamp = getattr(st.session_state, 'current_meeting_timestamp', format_timestamp())
    filename = EVALUATION_FILENAME.format(profile_name, timestamp)
    filepath = RESPONSE_EVALUATIONS_DIR / filename
    
    content = (
        EVALUATION_HEADER.format(format_timestamp("%Y-%m-%d %H:%M:%S")) +
        "".join(
            EVALUATION_SECTION.format(i) + eval_text + "\n"
            for i, eval_text in enumerate(st.session_state.evaluations, 1)
        )
    )
    
    if safe_file_operation(
        filepath.write_text,
        content,
        error_message=EVALUATION_SAVE_ERROR
    ):
        st.session_state.current_evaluation_filename = filename
        return filename
    return None

def get_chat_response(messages, mode="chat"):
    """Get response from API"""
    config = MODEL_CONFIG[mode].copy()
    
    return safe_file_operation(
        lambda: client.messages.create(
            model=config["model"],
            max_tokens=config["max_tokens"],
            temperature=config["temperature"],
            system=next((msg["content"] for msg in messages if msg["role"] == "system"), ""),
            messages=[
                {
                    "role": "assistant" if msg["role"] == "assistant" else "user",
                    "content": msg["content"]
                }
                for msg in messages 
                if msg["role"] != "system" and msg.get("content") and isinstance(msg["content"], str)
            ]
        ).content[0].text,
        error_message=API_CALL_ERROR
    )

def update_response_evaluation(messages):
    """Update the ongoing evaluation of the vendor's response"""
    recent_vendor_message = next((msg for msg in reversed(messages) 
                              if msg['role'] == 'user'), None)
    if not recent_vendor_message:
        return
    
    previous_customer_message = next((msg for msg in reversed(messages[:-1]) 
                           if msg['role'] == 'assistant'), None)
    
    context_message = (
        CHAT_CUSTOMER_PREVIOUS_MESSAGE.format(previous_customer_message['content'])
        if previous_customer_message else CHAT_INITIAL_VENDOR_PITCH
    )
    
    eval_messages = [
        {"role": "system", "content": st.session_state.response_evaluation_model},
        {"role": "user", "content": context_message + CHAT_VENDOR_RESPONSE.format(recent_vendor_message['content'])}
    ]
    
    evaluation = get_chat_response(eval_messages, mode="response_evaluation")
    if evaluation:
        st.session_state.evaluations.append(evaluation)

def generate_meeting_evaluation():
    """Generate meeting evaluation using all conversation data"""
    vendor_messages = [msg for msg in st.session_state.messages if msg["role"] == "user"]
    
    messages = [
        {"role": "system", "content": st.session_state.meeting_evaluation_model},
        {"role": "user", "content": CHAT_CUSTOMER_CONTEXT.format(st.session_state.customer_model)}
    ]
    messages.extend({"role": "user", "content": msg["content"]} for msg in vendor_messages)
    
    return get_chat_response(messages, mode="meeting_evaluation")

def save_report(report):
    """Save report to file"""
    if not report:
        return None
        
    filename = REPORT_FILENAME.format(
        st.session_state.customer_profile,
        format_timestamp(),
        REPORT_EXTENSION
    )
    filepath = MEETING_EVALUATIONS_DIR / filename
    
    return safe_file_operation(
        filepath.write_text,
        report,
        error_message=MEETING_SAVE_ERROR
    ) and filename

def initialize_session():
    """Initialize session state variables"""
    if "initialized" not in st.session_state:
        st.session_state.initialized = False
        st.session_state.conversation_ended = False
        st.session_state.messages = []
        st.session_state.evaluations = []
        st.session_state.customer_profile = None
        st.session_state.current_meeting_timestamp = None
        st.session_state.customer_model = None
        st.session_state.response_evaluation_model = None
        st.session_state.meeting_evaluation_model = None

def handle_new_meeting():
    """Handle new meeting button click"""
    if st.session_state.initialized and len(st.session_state.messages) > 1:
        save_meeting(st.session_state.customer_profile)
    
    st.session_state.initialized = False
    st.session_state.messages = []
    st.session_state.evaluations = []
    st.session_state.conversation_ended = False
    st.session_state.customer_profile = None
    st.session_state.current_meeting_timestamp = None
    st.rerun()

def initialize_meeting(selected_profile):
    """Initialize meeting with selected profile"""
    st.session_state.customer_profile = selected_profile
    st.session_state.current_meeting_timestamp = format_timestamp()
    
    st.session_state.customer_model = read_prompt(selected_profile, is_customer=True)
    st.session_state.response_evaluation_model = read_prompt('response_evaluation_model')
    st.session_state.meeting_evaluation_model = read_prompt('meeting_evaluation_model')
    
    st.session_state.messages = [{
        "role": "system",
        "content": "\n\n".join([
            read_prompt('core_instruction'),
            st.session_state.customer_model,
            read_prompt('vendor_model'),
            read_prompt('meeting_context')
        ])
    }]
    st.session_state.initialized = True
    st.rerun()

def main():
    initialize_session()

    # Main UI - Title Section
    st.title(
        TITLE_WITH_CUSTOMER.format(st.session_state.customer_profile)
        if st.session_state.initialized and st.session_state.customer_profile
        else TITLE_DEFAULT
    )

    # Sidebar
    with st.sidebar:
        if st.button(NEW_MEETING_BUTTON, use_container_width=True):
            handle_new_meeting()

    # Customer Profile Selection
    if not st.session_state.initialized:
        st.markdown(COMMON_TABLE_CSS, unsafe_allow_html=True)
        selected_profile = display_customer_profiles_table()
        if selected_profile:
            initialize_meeting(selected_profile)

    # Chat Interface
    if st.session_state.initialized:
        # Display chat history
        for message in st.session_state.messages:
            if message["role"] != "system":
                with st.chat_message(message["role"]):
                    st.write(message["content"])

        # Chat input
        if not st.session_state.conversation_ended:
            user_input = st.chat_input(CHAT_INPUT_PLACEHOLDER)
            
            if user_input:
                # Display user message
                st.session_state.messages.append({"role": "user", "content": user_input})
                with st.chat_message("user"):
                    st.write(user_input)
                
                update_response_evaluation(st.session_state.messages)

                if user_input.lower().strip() == FREEZE_COMMAND:
                    meeting_evaluation = generate_meeting_evaluation()
                    if meeting_evaluation:
                        filename = save_report(meeting_evaluation)
                        save_meeting(st.session_state.customer_profile)
                        if st.session_state.evaluations:
                            save_evaluation(st.session_state.evaluations[-1], st.session_state.customer_profile)
                        
                        with st.chat_message("assistant"):
                            st.write(meeting_evaluation)
                            st.write(CHAT_REPORT_SAVED.format(filename))
                            st.write(CHAT_MEETING_SAVED.format(st.session_state.current_meeting_filename))
                            st.write(CHAT_EVALUATIONS_SAVED.format(st.session_state.current_evaluation_filename))
                    st.session_state.conversation_ended = True
                else:
                    response = get_chat_response(st.session_state.messages)
                    if response:
                        st.session_state.messages.append({"role": "assistant", "content": response})
                        with st.chat_message("assistant"):
                            st.write(response)
                        
                        save_meeting(st.session_state.customer_profile)
                        if st.session_state.evaluations:
                            save_evaluation(st.session_state.evaluations[-1], st.session_state.customer_profile)

if __name__ == "__main__":
    main()