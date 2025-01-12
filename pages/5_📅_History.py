import streamlit as st
import pandas as pd
from datetime import datetime
import json

from core.strings import *
from core.styles import *
from core.config import MEETINGS_DIR, MEETING_EXTENSION

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

def load_meeting(filename):
    """Load meeting data from file"""
    filepath = MEETINGS_DIR / filename
    try:
        with open(filepath) as f:
            return json.load(f)
    except Exception as e:
        st.error(MEETING_FILE_ERROR.format(str(e)))
        return None

def list_saved_meetings():
    """List all saved meetings with their metadata"""
    if not MEETINGS_DIR.exists():
        st.error(MEETINGS_DIR_ERROR.format(MEETINGS_DIR))
        return []
    
    meetings = []
    for file in MEETINGS_DIR.glob(f"*{MEETING_EXTENSION}"):
        try:
            meeting_data = json.loads(file.read_text())
            # Get timestamp from meeting_start field instead of filename
            timestamp = meeting_data.get('meeting_start', '')
            
            meetings.append({
                'filename': file.name,
                'customer_profile': meeting_data.get('customer_profile', 'Unknown'),
                'timestamp': timestamp,
                'formatted_date': parse_timestamp(timestamp) if timestamp else "Unknown Date"
            })
        except Exception as e:
            st.error(MEETING_FILE_ERROR.format(str(e)))
            continue
    
    return sorted(meetings, key=lambda x: x['timestamp'], reverse=True)

# Custom CSS for vertical alignment
st.markdown(COMMON_TABLE_CSS, unsafe_allow_html=True)

st.title(VIEW_HISTORY_TITLE)

# Initialize session state for selected meeting
if "selected_meeting" not in st.session_state:
    st.session_state.selected_meeting = None

# Get meetings and create dataframe
meetings = list_saved_meetings()
if meetings:
    # Create DataFrame with formatted dates
    df = pd.DataFrame(meetings)
    
    # Create columns with predefined layout
    cols = st.columns(TABLE_LAYOUTS['history'])

    # Table headers with consistent styling
    for col, header in zip(cols, [
        MEETING_TABLE_HEADERS['customer'],
        MEETING_TABLE_HEADERS['date'],
        MEETING_TABLE_HEADERS['action']
    ]):
        col.markdown(f"<div class='table-header col-{header.lower()}'>{header}</div>", unsafe_allow_html=True)
    
    # Display each meeting as a row with a button
    for idx, row in df.iterrows():
        cols = st.columns(TABLE_LAYOUTS['history'])
        cols[0].markdown(f"<div class='meeting-cell'>{row['customer_profile']}</div>", unsafe_allow_html=True)
        cols[1].markdown(f"<div class='meeting-cell'>{row['formatted_date']}</div>", unsafe_allow_html=True)
        if cols[2].button(VIEW_REPORT_BUTTON_TEXT, key=f"view_{idx}"):
            meeting_data = load_meeting(row['filename'])
            if meeting_data:
                st.session_state.selected_meeting = {
                    'customer': row['customer_profile'],
                    'data': meeting_data
                }
    
    # Display selected meeting content
    if st.session_state.selected_meeting is not None:
        st.markdown("---")
        with st.expander(MEETING_EXPANDER_TITLE.format(st.session_state.selected_meeting['customer']), expanded=True):
            # Display conversation
            for msg in st.session_state.selected_meeting['data']['conversation']:
                with st.chat_message(msg['role']):
                    st.write(msg['content'])
            
            col1, col2, col3 = st.columns([1, 1, 4])
            if col1.button(CLOSE_BUTTON, key="close_meeting"):
                st.session_state.selected_meeting = None
                st.rerun()

else:
    st.write(NO_MEETINGS_FOUND)