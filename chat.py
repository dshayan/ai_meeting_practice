# Imports
import json
from datetime import datetime
import streamlit as st
from anthropic import Anthropic
from core.strings import *

# Import config
from core.config import (
    MODEL_CONFIG,
    MEETINGS_DATA_DIR,
    PROMPTS_DIR,
    CUSTOMERS_DIR,
    PROFILE_EXTENSION,
    MEETING_EXTENSION,
    REPORT_EXTENSION
)
from core.strings import *

# Initialize Anthropic client
client = Anthropic(api_key=MODEL_CONFIG["api_key"])

# Helper Functions
def list_customer_profiles():
    """Get list of available customer profiles"""
    profiles = []
    # Check if directory exists
    if not CUSTOMERS_DIR.exists():
        st.error(CUSTOMERS_DIR_ERROR.format(CUSTOMERS_DIR))
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
        st.error(PROMPT_FILE_ERROR.format(path))
        return ""

def list_saved_meetings():
    """List all saved meetings"""
    try:
        meetings = []
        for file in MEETINGS_DATA_DIR.glob(f"*{MEETING_EXTENSION}"):
            if file.is_file():
                try:
                    data = json.loads(file.read_text())
                    meetings.append({
                        'filename': file.name,
                        'customer_profile': data.get('customer_profile', 'Unknown Customer'),
                        'timestamp': data.get('meeting_start', '')
                    })
                except json.JSONDecodeError:
                    st.error(MEETING_FILE_ERROR.format(file))
                    continue
        return sorted(meetings, key=lambda x: x['timestamp'], reverse=True)
    except Exception as e:
        st.error(MEETINGS_LIST_ERROR.format(str(e)))
        return []

def load_meeting(filename):
    """Load meeting data from file"""
    try:
        filepath = MEETINGS_DATA_DIR / filename
        if not filepath.exists():
            st.error(MEETING_LOAD_ERROR.format(filepath))
            return None
        
        data = json.loads(filepath.read_text())
        
        # Convert old format to new format if necessary
        if 'vendor_messages' in data:
            # Create chronological conversation from old format
            conversation = []
            vendor_msgs = data['vendor_messages']
            customer_msgs = data['customer_responses']
            
            # Zip the messages together to maintain order
            for i in range(max(len(vendor_msgs), len(customer_msgs))):
                if i < len(vendor_msgs):
                    conversation.append({
                        **vendor_msgs[i],
                        'timestamp': data.get('timestamp', '')
                    })
                if i < len(customer_msgs):
                    conversation.append({
                        **customer_msgs[i],
                        'timestamp': data.get('timestamp', '')
                    })
            
            # Update to new format
            data['conversation'] = conversation
            del data['vendor_messages']
            del data['customer_responses']
            data['meeting_start'] = data.pop('timestamp', '')
            
        return data
    except Exception as e:
        st.error(MEETING_LOAD_ERROR.format(str(e)))
        return None

def save_meeting(profile_name):
    """Save current meeting to file"""
    try:
        # Use existing timestamp if within same interaction cycle, or generate new one
        timestamp = getattr(st.session_state, 'current_meeting_timestamp', 
                          datetime.now().strftime("%Y%m%d_%H%M%S"))
        
        # Convert messages to a chronological format with timestamps
        conversation_flow = []
        for msg in st.session_state.messages:
            if msg['role'] != 'system':  # Skip the system prompt
                conversation_flow.append({
                    'role': msg['role'],
                    'content': msg['content'],
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
        
        meeting_data = {
            'customer_profile': profile_name if profile_name else "Unknown Customer",
            'conversation': conversation_flow,
            'vendor_evaluations': st.session_state.evaluations,
            'meeting_start': timestamp,
            'customer_model': st.session_state.customer_model,
            'response_evaluation_model': st.session_state.response_evaluation_model,
            'meeting_evaluation_model': st.session_state.meeting_evaluation_model
        }
        
        # Use the same timestamp for filename
        filename = MEETING_FILENAME.format(profile_name, timestamp, MEETING_EXTENSION)
        filepath = MEETINGS_DATA_DIR / filename
        filepath.write_text(json.dumps(meeting_data, indent=2))
        
        # Update session state with current filename and timestamp
        st.session_state.current_meeting_filename = filename
        st.session_state.current_meeting_timestamp = timestamp
        
        return filename
    except Exception as e:
        st.error(MEETING_SAVE_ERROR.format(str(e)))
        return None

def save_evaluation(evaluation, profile_name):
    """Save evaluation to file"""
    try:
        timestamp = getattr(st.session_state, 'current_meeting_timestamp', 
                          datetime.now().strftime("%Y%m%d_%H%M%S"))
        
        # Create a new evaluation filename for each meeting
        evaluation_filename = EVALUATION_FILENAME.format(profile_name, timestamp)
        filepath = MEETINGS_DATA_DIR / evaluation_filename
        
        # Write evaluation to a new file (not append mode)
        with open(filepath, 'w') as f:
            f.write(EVALUATION_HEADER.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            # Write all evaluations for this meeting
            for i, eval_text in enumerate(st.session_state.evaluations, 1):
                f.write(EVALUATION_SECTION.format(i))
                f.write(eval_text)
                f.write("\n")
            
        # Store the current evaluation filename
        st.session_state.current_evaluation_filename = evaluation_filename
        return evaluation_filename
    except Exception as e:
        st.error(EVALUATION_SAVE_ERROR.format(str(e)))
        return None

def update_response_evaluation(messages):
    """Update the ongoing evaluation of the vendor's response"""
    recent_vendor_message = next((msg for msg in reversed(messages) 
                              if msg['role'] == 'user'), None)
    
    if not recent_vendor_message:
        return
    
    previous_customer_message = next((msg for msg in reversed(messages[:-1]) 
                           if msg['role'] == 'assistant'), None)
    
    context_message = (
        f"Customer's previous message: {previous_customer_message['content']}\n\n" if previous_customer_message 
        else "Initial vendor pitch:\n\n"
    )
    
    eval_messages = [
        {"role": "system", "content": st.session_state.response_evaluation_model},
        {"role": "user", "content": (
            f"{context_message}"
            f"Vendor's response: {recent_vendor_message['content']}"
        )}
    ]
    
    evaluation = get_chat_response(eval_messages, mode="response_evaluation")
    if evaluation:
        st.session_state.evaluations.append(evaluation)

def generate_meeting_evaluation():
    """Generate meeting evaluation using all conversation data"""
    conversation_messages = [msg for msg in st.session_state.messages if msg["role"] != "system"]
    
    report_messages = [
        {
            "role": "system", 
            "content": f"{st.session_state.customer_model}\n{st.session_state.meeting_evaluation_model}"
        }
    ]
    report_messages.extend(conversation_messages)
    
    return get_chat_response(report_messages, mode="meeting_evaluation")

def save_report(report):
    """Save report to file"""
    try:
        if not report:
            return None
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = REPORT_FILENAME.format(st.session_state.customer_profile, timestamp, REPORT_EXTENSION)
        filepath = MEETINGS_DATA_DIR / filename
        filepath.write_text(report)
        return filename
    except Exception as e:
        st.error(MEETING_SAVE_ERROR.format(str(e)))
        return None

def get_chat_response(messages, mode="chat"):
    """Get response from API
    Args:
        messages: List of message dictionaries
        mode: One of "chat", "response_evaluation", or "meeting_evaluation"
    """
    try:
        # Initialize config based on the calling function
        config = MODEL_CONFIG[mode].copy()
        
        # Create message with Anthropic's required parameters
        response = client.messages.create(
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
        )
        
        return response.content[0].text if response.content else ""
        
    except Exception as e:
        st.error(API_CALL_ERROR.format(str(e)))
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
    st.session_state.response_evaluation_model = None
    st.session_state.meeting_evaluation_model = None

# Main UI - Title Section
if st.session_state.initialized and st.session_state.customer_profile:
    st.title(TITLE_WITH_CUSTOMER.format(st.session_state.customer_profile))
    st.write(f"Last edit at {datetime.now().strftime('%Y-%m-%d')}")
else:
    st.title(TITLE_DEFAULT)

# Sidebar
with st.sidebar:
    st.header(SIDEBAR_HEADER)
    st.write(SIDEBAR_SUBHEADER)
    st.markdown("---")
    
    if st.button(NEW_MEETING_BUTTON, use_container_width=True, key="new_meeting_button"):
        if st.session_state.initialized and len(st.session_state.messages) > 1:
            save_meeting(st.session_state.customer_profile)
        
        st.session_state.initialized = False
        st.session_state.messages = []
        st.session_state.evaluations = []
        st.session_state.conversation_ended = False
        st.session_state.customer_profile = None
        st.session_state.current_meeting_timestamp = None
        st.rerun()
    
    st.header(PREVIOUS_MEETINGS_HEADER)
    meetings = list_saved_meetings()
    
    if meetings:
        for i, meeting in enumerate(meetings):
            timestamp_str = meeting['timestamp']
            if timestamp_str:  # Only try to parse if timestamp exists
                timestamp = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")
                formatted_time = timestamp.strftime("%Y-%m-%d")
            else:
                formatted_time = "No date"
            
            is_active = (st.session_state.initialized and 
                        st.session_state.customer_profile == meeting['customer_profile'] and
                        st.session_state.current_meeting_timestamp == meeting['timestamp'])
            
            display_text = f"{meeting['customer_profile']}, {formatted_time}"
            if is_active:
                display_text = f"**{display_text}**"
            
            if st.button(
                display_text, 
                key=f"meeting_{i}", 
                use_container_width=True,
                disabled=is_active
            ):
                data = load_meeting(meeting['filename'])
                if data:
                    # Initialize system message
                    st.session_state.messages = [{"role": "system", "content": data['customer_model']}]
                    # Add conversation messages
                    st.session_state.messages.extend([
                        {"role": msg['role'], "content": msg['content']} 
                        for msg in data['conversation']
                    ])
                    st.session_state.evaluations = data['vendor_evaluations']
                    st.session_state.customer_model = data['customer_model']
                    st.session_state.response_evaluation_model = data['response_evaluation_model']
                    st.session_state.meeting_evaluation_model = data.get('meeting_evaluation_model', data.get('report_model', ''))
                    st.session_state.initialized = True
                    st.session_state.conversation_ended = False
                    st.session_state.customer_profile = meeting['customer_profile']
                    st.session_state.current_meeting_timestamp = meeting['timestamp']
                    st.rerun()
    else:
        st.write(NO_SAVED_MEETINGS)

# Customer Profile Selection
if not st.session_state.initialized:
    profiles = list_customer_profiles()
    selected_profile = st.selectbox(
        SELECT_CUSTOMER_PROMPT,
        profiles,
        format_func=lambda x: x,
        label_visibility="collapsed"
    )
    
    if st.button(START_MEETING_BUTTON):
        st.session_state.customer_profile = selected_profile
        st.session_state.current_meeting_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        st.session_state.customer_model = read_prompt(selected_profile, is_customer=True)
        st.session_state.response_evaluation_model = read_prompt('response_evaluation_model')
        st.session_state.meeting_evaluation_model = read_prompt('meeting_evaluation_model')
        
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
    user_input = st.chat_input(CHAT_INPUT_PLACEHOLDER)
    
    if user_input:
        # Vendor's message
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)
            
        # Evaluate vendor's response from customer's perspective
        update_response_evaluation(st.session_state.messages)

        if user_input.lower().strip() == FREEZE_COMMAND:
            meeting_evaluation = generate_meeting_evaluation()
            if meeting_evaluation:
                filename = save_report(meeting_evaluation)
                # Save the final state of the meeting and evaluation
                save_meeting(st.session_state.customer_profile)
                save_evaluation(st.session_state.evaluations[-1], st.session_state.customer_profile)
                with st.chat_message("assistant"):
                    st.write(meeting_evaluation)
                    st.write(f"\nReport saved to: {filename}")
                    st.write(f"Meeting saved to: {st.session_state.current_meeting_filename}")
                    st.write(f"Evaluations saved to: {st.session_state.current_evaluation_filename}")
            st.session_state.conversation_ended = True
        else:
            # Customer's response
            response = get_chat_response(st.session_state.messages)
            if response:
                st.session_state.messages.append({"role": "assistant", "content": response})
                with st.chat_message("assistant"):
                    st.write(response)
                
                # Save meeting and evaluation together
                save_meeting(st.session_state.customer_profile)
                save_evaluation(st.session_state.evaluations[-1], st.session_state.customer_profile)