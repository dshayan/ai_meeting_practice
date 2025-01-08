import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime

from core.config import CUSTOMERS_DIR, PROFILE_EXTENSION
from core.strings import *

def list_customer_profiles():
    """Get list of available customer profiles with their details"""
    profiles = []
    
    if not CUSTOMERS_DIR.exists():
        st.error(CUSTOMERS_DIR_ERROR.format(CUSTOMERS_DIR))
        return profiles
        
    for file in CUSTOMERS_DIR.glob(f"*{PROFILE_EXTENSION}"):
        if file.is_file():
            content = file.read_text()
            
            # Extract basic info from content
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

# Custom CSS for vertical alignment
st.markdown("""
    <style>
        .stMarkdown p {
            margin-bottom: 0;
            line-height: 38px;  /* Matches the height of Streamlit buttons */
            vertical-align: middle;
        }
        .profile-cell {
            display: flex;
            align-items: center;
            min-height: 38px;
        }
    </style>
""", unsafe_allow_html=True)

st.title(VIEW_PROFILES_TITLE)

# Initialize session state for selected profile
if "selected_profile" not in st.session_state:
    st.session_state.selected_profile = None

# Get profiles and create dataframe
profiles = list_customer_profiles()
if profiles:
    # Create DataFrame
    df = pd.DataFrame(profiles)
    
    # Format the Last Modified column
    df['Last Modified'] = df['Last Modified'].dt.strftime('%Y-%m-%d')
    
    # Create columns for layout
    cols = st.columns([3, 4, 2, 1])
    
    # Table headers
    cols[0].write(f"**{PROFILE_TABLE_HEADERS['name']}**")
    cols[1].write(f"**{PROFILE_TABLE_HEADERS['role']}**")
    cols[2].write(f"**{PROFILE_TABLE_HEADERS['last_modified']}**")
    cols[3].write(f"**{VIEW_PROFILE_COLUMN_HEADER}**")
    
    # Display each profile as a row with a button
    for idx, row in df.iterrows():
        cols = st.columns([3, 4, 2, 1])
        cols[0].markdown(f"<div class='profile-cell'>{row['Name']}</div>", unsafe_allow_html=True)
        cols[1].markdown(f"<div class='profile-cell'>{row['Role']}</div>", unsafe_allow_html=True)
        cols[2].markdown(f"<div class='profile-cell'>{row['Last Modified']}</div>", unsafe_allow_html=True)
        if cols[3].button(VIEW_PROFILE_BUTTON_TEXT, key=f"view_{idx}"):
            st.session_state.selected_profile = row
    
    # Inside the if block where we display the selected profile content
    if st.session_state.selected_profile is not None:
        st.markdown("---")
        with st.expander(PROFILE_EXPANDER_TITLE.format(st.session_state.selected_profile['Name']), expanded=True):
            # Add edit mode to session state if not exists
            if 'edit_mode' not in st.session_state:
                st.session_state.edit_mode = False
                
            # Show either editable text area or regular text display
            if st.session_state.edit_mode:
                edited_content = st.text_area(EDIT_PROFILE_LABEL, 
                                           value=st.session_state.selected_profile['Content'],
                                           height=400)
                
                col1, col2, col3 = st.columns([1, 1, 4])
                
                if col1.button(CANCEL_BUTTON, key="cancel_edit"):
                    st.session_state.edit_mode = False
                    st.rerun()
                
                if col2.button(SAVE_BUTTON, key="save_profile"):
                    # Get the file path
                    file_path = CUSTOMERS_DIR / st.session_state.selected_profile['File']
                    try:
                        # Save the edited content
                        file_path.write_text(edited_content)
                        st.success(PROFILE_SAVE_SUCCESS_MESSAGE)
                        # Update the content in session state
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

# Add button to create new profile
if st.button(CREATE_NEW_PROFILE_BUTTON, use_container_width=True):
    st.switch_page("pages/1_➕_Create.py")