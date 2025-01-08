import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime

from core.config import MEETINGS_DATA_DIR, REPORT_EXTENSION
from core.strings import *

def list_meeting_reports():
    """Get list of available meeting reports with their details"""
    reports = []
    
    if not MEETINGS_DATA_DIR.exists():
        st.error(MEETINGS_DIR_ERROR.format(MEETINGS_DATA_DIR))
        return reports
        
    # Look specifically for meeting evaluation reports using the filename pattern
    # Format: meeting_evaluation_CustomerName_YYYYMMDD_HHMMSS.txt
    for file in MEETINGS_DATA_DIR.glob("meeting_evaluation_*" + REPORT_EXTENSION):
        if file.is_file():
            content = file.read_text()
            
            # Extract customer name from filename
            parts = file.stem.split('_')
            if len(parts) >= 3:
                customer_name = ' '.join(parts[2:-2])  # Join all parts between 'evaluation' and timestamp
            else:
                customer_name = "Unknown"
            
            reports.append({
                "Customer": customer_name,
                "File": file.name,
                "Content": content,
                "Last Modified": datetime.fromtimestamp(file.stat().st_mtime)
            })
    
    return reports

# Custom CSS for vertical alignment (same as view_profiles.py)
st.markdown("""
    <style>
        .stMarkdown p {
            margin-bottom: 0;
            line-height: 38px;
            vertical-align: middle;
        }
        .report-cell {
            display: flex;
            align-items: center;
            min-height: 38px;
        }
    </style>
""", unsafe_allow_html=True)

st.title(VIEW_REPORTS_TITLE)

# Initialize session state for selected report
if "selected_report" not in st.session_state:
    st.session_state.selected_report = None

# Get reports and create dataframe
reports = list_meeting_reports()
if reports:
    # Create DataFrame
    df = pd.DataFrame(reports)
    
    # Format the Last Modified column
    df['Last Modified'] = df['Last Modified'].dt.strftime('%Y-%m-%d')
    
    # Create columns for layout
    cols = st.columns([4, 2, 1])
    
    # Table headers
    cols[0].write(f"**{REPORT_TABLE_HEADERS['customer']}**")
    cols[1].write(f"**{REPORT_TABLE_HEADERS['last_modified']}**")
    cols[2].write(f"**{REPORT_TABLE_HEADERS['action']}**")
    
    # Display each report as a row with a button
    for idx, row in df.iterrows():
        cols = st.columns([4, 2, 1])
        cols[0].markdown(f"<div class='report-cell'>{row['Customer']}</div>", unsafe_allow_html=True)
        cols[1].markdown(f"<div class='report-cell'>{row['Last Modified']}</div>", unsafe_allow_html=True)
        if cols[2].button(VIEW_REPORT_BUTTON_TEXT, key=f"view_{idx}"):
            st.session_state.selected_report = row
    
    # Display selected report content
    if st.session_state.selected_report is not None:
        st.markdown("---")
        with st.expander(REPORT_EXPANDER_TITLE.format(st.session_state.selected_report['Customer']), expanded=True):
            st.text(st.session_state.selected_report['Content'])
            
            col1, col2, col3 = st.columns([1, 1, 4])
            if col1.button(CLOSE_BUTTON, key="close_report"):
                st.session_state.selected_report = None
                st.rerun()

else:
    st.write(NO_REPORTS_FOUND)