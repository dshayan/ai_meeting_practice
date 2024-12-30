# Imports
import json
from datetime import datetime
import streamlit as st
from openai import OpenAI
from anthropic import Anthropic

# Import config
from config import (
    MODEL_CONFIG,
    MEETINGS_DIR,
    PROMPTS_DIR,
    CUSTOMERS_DIR,
    PROFILE_EXTENSION,
    MEETING_EXTENSION,
    REPORT_EXTENSION
)

# Initialize client based on provider
if MODEL_CONFIG["provider"] == "anthropic":
    client = Anthropic(api_key=MODEL_CONFIG["api_key"])
else:
    client = OpenAI(api_key=MODEL_CONFIG["api_key"])

# Helper Functions
def list_customer_profiles():
    """Get list of available customer profiles"""
    profiles = []
    # Check if directory exists
    if not CUSTOMERS_DIR.exists():
        st.error(f"Customers directory not found: {CUSTOMERS_DIR}")
        return profiles
        
    # List all files in directory
    for file in CUSTOMERS_DIR.glob(f"*{PROFILE_EXTENSION}"):
        if file.is_file():
            profiles.append(file.stem)
    
    return sorted(profiles)

def read_prompt(filename, is_customer=False):
    """Read prompt from file"""
    try:
        path = CUSTOMERS_DIR / f"{filename}{PROFILE_EXTENSION}" if is_customer else PROMPTS_DIR / f"{filename}{PROFILE_EXTENSION}"
        return path.read_text().strip()
    except FileNotFoundError:
        st.error(f"Prompt file not found: {path}")
        return ""

def list_saved_meetings():
    """List all saved meetings"""
    try:
        meetings = []
        for file in MEETINGS_DIR.glob(f"*{MEETING_EXTENSION}"):
            if file.is_file():
                try:
                    data = json.loads(file.read_text())
                    meetings.append({
                        'filename': file.name,
                        'profile': data.get('profile', 'Unknown'),
                        'timestamp': data.get('timestamp', '')
                    })
                except json.JSONDecodeError:
                    st.error(f"Error reading meeting file: {file}")
                    continue
        return sorted(meetings, key=lambda x: x['timestamp'], reverse=True)
    except Exception as e:
        st.error(f"Error listing meetings: {str(e)}")
        return []

def load_meeting(filename):
    """Load meeting data from file"""
    try:
        filepath = MEETINGS_DIR / filename
        if not filepath.exists():
            st.error(f"Meeting file not found: {filepath}")
            return None
        return json.loads(filepath.read_text())
    except Exception as e:
        st.error(f"Error loading meeting: {str(e)}")
        return None

def save_meeting(profile_name):
    """Save current meeting to file"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        meeting_data = {
            'profile': profile_name if profile_name else "Unknown Customer",
            'messages': st.session_state.messages,
            'evaluations': st.session_state.evaluations,
            'timestamp': timestamp,
            'customer_model': st.session_state.customer_model,
            'evaluation_model': st.session_state.evaluation_model,
            'report_model': st.session_state.report_model
        }
        
        filename = f"meeting_{profile_name}_{timestamp}{MEETING_EXTENSION}"
        filepath = MEETINGS_DIR / filename
        filepath.write_text(json.dumps(meeting_data, indent=2))
        return filename
    except Exception as e:
        st.error(f"Error saving meeting: {str(e)}")
        return None

def get_chat_response(messages, evaluation_update=False):
    """Get response from API"""
    try:
        # Initialize config first
        config = MODEL_CONFIG["evaluation"].copy() if evaluation_update else MODEL_CONFIG["chat"].copy()
        
        if not evaluation_update:
            if st.session_state.customer_model and st.session_state.evaluation_model:
                eval_context = f"{st.session_state.customer_model}\n\n{st.session_state.evaluation_model}"
                if MODEL_CONFIG["provider"] == "anthropic":
                    # For Anthropic, use system parameter
                    messages = messages[1:]  # Remove old system message
                    config["system"] = eval_context
                else:
                    # For OpenAI, keep system message in messages
                    messages = [{"role": "system", "content": eval_context}] + messages[1:]
            else:
                st.error("Customer model or evaluation model is missing")
                return None

        # Filter out any messages with null content
        valid_messages = [
            msg for msg in messages 
            if msg.get("content") is not None and isinstance(msg["content"], str) and msg["content"].strip() != ""
        ]
        
        if not valid_messages:
            st.error("No valid messages to send")
            return None
        
        if MODEL_CONFIG["provider"] == "anthropic":
            # Convert OpenAI message format to Anthropic format
            anthropic_messages = []
            for msg in valid_messages:
                if msg["role"] == "system":
                    config["system"] = msg["content"]
                else:
                    anthropic_messages.append({
                        "role": msg["role"],
                        "content": msg["content"]
                    })
            
            response = client.messages.create(
                messages=anthropic_messages,
                **config
            )
            # Extract the text content from the response
            return response.content[0].text if response.content else ""
        else:
            response = client.chat.completions.create(
                messages=valid_messages,
                **config
            )
            return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error in API call: {str(e)}")
        return None
    
def update_user_evaluation(messages):
    """Update the ongoing evaluation of the user"""
    eval_messages = messages.copy()
    eval_messages.append({"role": "system", "content": st.session_state.evaluation_model})
    evaluation = get_chat_response(eval_messages, evaluation_update=True)
    if evaluation:
        st.session_state.evaluations.append(evaluation)

def generate_final_report():
    """Generate final report using all conversation data"""
    report_messages = st.session_state.messages.copy()
    report_context = f"{st.session_state.evaluation_model}\n\n{st.session_state.report_model}"
    report_messages.append({"role": "system", "content": report_context})
    report_messages.append({"role": "user", "content": "Generate final evaluation report"})
    return get_chat_response(report_messages)

def save_report(report):
    """Save report to file"""
    try:
        if not report:
            return None
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"report_{st.session_state.customer_profile}_{timestamp}{REPORT_EXTENSION}"
        filepath = MEETINGS_DIR / filename
        filepath.write_text(report)
        return filename
    except Exception as e:
        st.error(f"Error saving report: {str(e)}")
        return None

# Initialize Streamlit Session State
if "initialized" not in st.session_state:
    st.session_state.initialized = False
    st.session_state.conversation_ended = False
    st.session_state.messages = []
    st.session_state.evaluations = []
    st.session_state.customer_profile = None
    st.session_state.current_meeting_timestamp = None
    st.session_state.customer_model = None
    st.session_state.evaluation_model = None
    st.session_state.report_model = None

# Main UI - Title Section
if st.session_state.initialized and st.session_state.customer_profile:
    st.title(f"Meeting with {st.session_state.customer_profile}")
    st.write(f"Last edit at {datetime.now().strftime('%Y-%m-%d')}")
else:
    st.title("Who do you want to meet?")

# Sidebar
with st.sidebar:
    st.header("Momentum")
    st.write("Customer Meeting Simulator")
    st.markdown("---")
    
    if st.button("New meeting", use_container_width=True, key="new_meeting_button"):
        if st.session_state.initialized and len(st.session_state.messages) > 1:
            save_meeting(st.session_state.customer_profile)
        
        st.session_state.initialized = False
        st.session_state.messages = []
        st.session_state.evaluations = []
        st.session_state.conversation_ended = False
        st.session_state.customer_profile = None
        st.session_state.current_meeting_timestamp = None
        st.rerun()

    st.header("Previous meetings")
    meetings = list_saved_meetings()
    
    if meetings:
        for i, meeting in enumerate(meetings):
            timestamp = datetime.strptime(meeting['timestamp'], "%Y%m%d_%H%M%S")
            formatted_time = timestamp.strftime("%Y-%m-%d")
            
            is_active = (st.session_state.initialized and 
                        st.session_state.customer_profile == meeting['profile'] and
                        st.session_state.current_meeting_timestamp == meeting['timestamp'])
            
            display_text = f"{meeting['profile']}, {formatted_time}"
            if is_active:
                display_text = f"**{display_text}**"
            
            if st.button(
                display_text, 
                key=f"meeting_{i}", 
                use_container_width=True,
                disabled=is_active
            ):
                data = load_meeting(meeting['filename'])
                st.session_state.messages = data['messages']
                st.session_state.evaluations = data['evaluations']
                st.session_state.customer_model = data['customer_model']
                st.session_state.evaluation_model = data['evaluation_model']
                st.session_state.report_model = data['report_model']
                st.session_state.initialized = True
                st.session_state.conversation_ended = False
                st.session_state.customer_profile = meeting['profile']
                st.session_state.current_meeting_timestamp = meeting['timestamp']
                st.rerun()
    else:
        st.write("No saved meetings yet.")

# Customer Profile Selection
if not st.session_state.initialized:
    profiles = list_customer_profiles()
    selected_profile = st.selectbox(
        "Select a customer",
        profiles,
        format_func=lambda x: x,
        label_visibility="collapsed"
    )
    
    if st.button("Start meeting"):
        st.session_state.customer_profile = selected_profile
        st.session_state.current_meeting_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        st.session_state.customer_model = read_prompt(selected_profile, is_customer=True)
        st.session_state.evaluation_model = read_prompt('evaluation_model')
        st.session_state.report_model = read_prompt('report_model')
        
        st.session_state.messages = [
            {"role": "system", "content": st.session_state.customer_model}
        ]
        st.session_state.initialized = True
        st.rerun()

# Chat Interface
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.write(message["content"])

if not st.session_state.conversation_ended:
    user_input = st.chat_input("Make your pitch...")
    
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        if user_input.lower().strip() == "freeze and report":
            final_report = generate_final_report()
            if final_report:
                filename = save_report(final_report)
                meeting_filename = save_meeting(st.session_state.customer_profile)
                with st.chat_message("assistant"):
                    st.write("Final Evaluation Report:")
                    st.write(final_report)
                    st.write(f"\nReport saved to: {filename}")
                    st.write(f"Meeting saved to: {meeting_filename}")
            st.session_state.conversation_ended = True
        else:
            response = get_chat_response(st.session_state.messages)
            if response:
                st.session_state.messages.append({"role": "assistant", "content": response})
                update_user_evaluation(st.session_state.messages)
                with st.chat_message("assistant"):
                    st.write(response)