import streamlit as st
import pandas as pd
from datetime import datetime

from core.config import MEETINGS_DATA_DIR, MEETING_EXTENSION
from core.strings import *
import importlib
meet = importlib.import_module("pages.3_💬_Meet")
list_saved_meetings = meet.list_saved_meetings
load_meeting = meet.load_meeting

# Custom CSS for vertical alignment
st.markdown("""
    <style>
        .stMarkdown p {
            margin-bottom: 0;
            line-height: 38px;
            vertical-align: middle;
        }
        .meeting-cell {
            display: flex;
            align-items: center;
            min-height: 38px;
        }
    </style>
""", unsafe_allow_html=True)

st.title(VIEW_HISTORY_TITLE)

# Initialize session state for selected meeting
if "selected_meeting" not in st.session_state:
    st.session_state.selected_meeting = None

# Get meetings and create dataframe
meetings = list_saved_meetings()
if meetings:
    # Create DataFrame with formatted dates
    df = pd.DataFrame(meetings)
    df['Date'] = pd.to_datetime(df['timestamp'], format='%Y%m%d_%H%M%S').dt.strftime('%Y-%m-%d')
    
    # Create columns for layout
    cols = st.columns([4, 2, 1])
    
    # Table headers
    cols[0].write(f"**{MEETING_TABLE_HEADERS['customer']}**")
    cols[1].write(f"**{MEETING_TABLE_HEADERS['date']}**")
    cols[2].write(f"**{MEETING_TABLE_HEADERS['action']}**")
    
    # Display each meeting as a row with a button
    for idx, row in df.iterrows():
        cols = st.columns([4, 2, 1])
        cols[0].markdown(f"<div class='meeting-cell'>{row['customer_profile']}</div>", unsafe_allow_html=True)
        cols[1].markdown(f"<div class='meeting-cell'>{row['Date']}</div>", unsafe_allow_html=True)
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