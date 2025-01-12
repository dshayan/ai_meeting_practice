import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime

from core.strings import *
from core.styles import *
from core.config import MEETING_EVALUATIONS_DIR, REPORT_EXTENSION

def list_meeting_reports():
    """Get list of available meeting reports with their details"""
    reports = []
    
    if not MEETING_EVALUATIONS_DIR.exists():
        st.error(MEETINGS_DIR_ERROR.format(MEETING_EVALUATIONS_DIR))
        return reports
        
    # Look specifically for meeting evaluation reports using the filename pattern
    # Format: meeting_evaluation_CustomerName_YYYYMMDD_HHMMSS.txt
    for file in MEETING_EVALUATIONS_DIR.glob("meeting_evaluation_*" + REPORT_EXTENSION):
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
st.markdown(COMMON_TABLE_CSS, unsafe_allow_html=True)

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
    
    # Create columns with predefined layout
    cols = st.columns(TABLE_LAYOUTS['reports'])

    # Table headers with consistent styling
    for col, header in zip(cols, [
        REPORT_TABLE_HEADERS['customer'],
        REPORT_TABLE_HEADERS['last_modified'],
        REPORT_TABLE_HEADERS['action']
    ]):
        col.markdown(f"<div class='table-header col-{header.lower()}'>{header}</div>", unsafe_allow_html=True)
    
    # Display each report as a row with a button
    for idx, row in df.iterrows():
        cols = st.columns(TABLE_LAYOUTS['reports'])
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