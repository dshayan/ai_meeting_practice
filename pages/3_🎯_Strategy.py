import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime
import json
from anthropic import Anthropic

from core.config import (
    CUSTOMERS_DIR,
    STRATEGIES_DIR, 
    MEETINGS_DIR,
    MEETING_EVALUATIONS_DIR,
    PROMPTS_DIR,
    PROFILE_EXTENSION,
    MEETING_EXTENSION,
    REPORT_EXTENSION,
    MODEL_CONFIG
)
from core.strings import *

# Initialize Anthropic client
client = Anthropic(api_key=MODEL_CONFIG["api_key"])

def get_strategy_filepath(customer_name):
    """Get strategy file path for a customer"""
    return STRATEGIES_DIR / f"{customer_name}_strategy.txt"

def strategy_exists(customer_name):
    """Check if strategy exists for customer"""
    return get_strategy_filepath(customer_name).exists()

def list_saved_meetings(customer_name=None):
    """List saved meetings, optionally filtered by customer"""
    try:
        meetings = []
        for file in MEETINGS_DIR.glob(f"*{MEETING_EXTENSION}"):
            if file.is_file():
                try:
                    data = json.loads(file.read_text())
                    if customer_name and data.get('customer_profile') != customer_name:
                        continue
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

def list_meeting_reports(customer_name=None):
    """Get list of meeting reports, optionally filtered by customer"""
    reports = []
    
    if not MEETING_EVALUATIONS_DIR.exists():
        st.error(MEETINGS_DIR_ERROR.format(MEETING_EVALUATIONS_DIR))
        return reports
        
    for file in MEETING_EVALUATIONS_DIR.glob("meeting_evaluation_*" + REPORT_EXTENSION):
        if file.is_file():
            parts = file.stem.split('_')
            if len(parts) >= 3:
                file_customer_name = ' '.join(parts[2:-2])
                if customer_name and file_customer_name != customer_name:
                    continue
                content = file.read_text()
                reports.append({
                    "Customer": file_customer_name,
                    "Content": content
                })
    
    return reports

def create_strategy(customer_profile, meetings, reports):
    """Generate meeting strategy using AI"""
    try:
        # Load strategy generation prompt
        prompt_path = PROMPTS_DIR / "strategy_generation_model.txt"
        if not prompt_path.exists():
            st.error(STRATEGY_PROMPT_ERROR.format(prompt_path))
            return None
            
        prompt_template = prompt_path.read_text()
        
        # Prepare context from customer profile, meetings and reports
        context = prompt_template.format(
            customer_profile,
            meetings if meetings else 'No previous meetings',
            reports if reports else 'No previous evaluations'
        )
        
        response = client.messages.create(
            model=MODEL_CONFIG["strategy"]["model"],
            max_tokens=MODEL_CONFIG["strategy"]["max_tokens"],
            temperature=MODEL_CONFIG["strategy"]["temperature"],
            messages=[{
                "role": "user",
                "content": context
            }]
        )
        
        return response.content[0].text if response.content else ""
        
    except Exception as e:
        st.error(STRATEGY_GENERATION_ERROR.format(str(e)))
        return None

def save_strategy(customer_name, strategy_content):
    """Save strategy to file"""
    try:
        filepath = get_strategy_filepath(customer_name)
        filepath.write_text(strategy_content)
        return True
    except Exception as e:
        st.error(STRATEGY_SAVE_ERROR.format(str(e)))
        return False

# Custom CSS for vertical alignment
st.markdown("""
    <style>
        .stMarkdown p {
            margin-bottom: 0;
            line-height: 38px;
            vertical-align: middle;
        }
        .strategy-cell {
            display: flex;
            align-items: center;
            min-height: 38px;
        }
    </style>
""", unsafe_allow_html=True)

st.title(STRATEGY_PAGE_TITLE)

# Initialize session state
if "selected_strategy" not in st.session_state:
    st.session_state.selected_strategy = None

# Get customer profiles
profiles = []
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
            "Has_Strategy": strategy_exists(name)
        })

if profiles:
    # Create DataFrame
    df = pd.DataFrame(profiles)
    
    # Create columns for layout
    cols = st.columns([3, 4, 2])
    
    # Table headers
    cols[0].write(f"**{STRATEGY_TABLE_HEADERS['name']}**")
    cols[1].write(f"**{STRATEGY_TABLE_HEADERS['role']}**")
    cols[2].write(f"**{STRATEGY_TABLE_HEADERS['action']}**")
    
    # Display each profile as a row
    for idx, row in df.iterrows():
        cols = st.columns([3, 4, 2])
        cols[0].markdown(f"<div class='strategy-cell'>{row['Name']}</div>", unsafe_allow_html=True)
        cols[1].markdown(f"<div class='strategy-cell'>{row['Role']}</div>", unsafe_allow_html=True)
        
        if row['Has_Strategy']:
            if cols[2].button(STRATEGY_VIEW_BUTTON, key=f"strategy_view_{idx}"):
                strategy_content = get_strategy_filepath(row['Name']).read_text()
                st.session_state.selected_strategy = {
                    'name': row['Name'],
                    'content': strategy_content
                }
        else:
            if cols[2].button(STRATEGY_CREATE_BUTTON, key=f"strategy_create_{idx}"):
                # Get meetings and reports for this customer
                customer_meetings = list_saved_meetings(row['Name'])
                customer_reports = list_meeting_reports(row['Name'])
                
                # Generate strategy
                strategy_content = create_strategy(
                    row['Content'],
                    customer_meetings,
                    customer_reports
                )
                
                if strategy_content and save_strategy(row['Name'], strategy_content):
                    st.success(STRATEGY_CREATION_SUCCESS.format(row['Name']))
                    st.session_state.selected_strategy = {
                        'name': row['Name'],
                        'content': strategy_content
                    }
                    st.rerun()

    # Display selected strategy
    if st.session_state.selected_strategy:
        st.markdown("---")
        with st.expander(STRATEGY_EXPANDER_TITLE.format(st.session_state.selected_strategy['name']), expanded=True):
            st.text(st.session_state.selected_strategy['content'])
            
            col1, col2, col3 = st.columns([1, 1, 4])
            if col1.button(CLOSE_BUTTON, key="strategy_close_view"):
                st.session_state.selected_strategy = None
                st.rerun()

            if col2.button(STRATEGY_MEET_BUTTON, key="strategy_start_meeting"):
                st.switch_page("pages/4_💬_Meet.py")

else:
    st.write(NO_STRATEGIES_FOUND)