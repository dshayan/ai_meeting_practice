import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime

from core.strings import *
from core.styles import *
from core.config import PROMPTS_DIR

def list_prompts():
    """Get list of available prompts with their details"""
    prompts = []
    
    if not PROMPTS_DIR.exists():
        st.error(PROMPTS_DIR_ERROR.format(PROMPTS_DIR))
        return prompts
        
    for file in PROMPTS_DIR.glob("*.txt"):
        if file.is_file():
            content = file.read_text()
            # Convert filename to display name (e.g., customer_creation_model -> Customer Creation Model)
            display_name = " ".join(
                word.capitalize()
                for word in file.stem.replace('_', ' ').split()
            )
            
            prompts.append({
                "Name": display_name,
                "File": file.name,
                "Content": content,
                "Last Modified": datetime.fromtimestamp(file.stat().st_mtime)
            })
    
    return prompts

# Custom CSS for vertical alignment
st.markdown(COMMON_TABLE_CSS, unsafe_allow_html=True)

st.title(SETTINGS_PAGE_TITLE)

# Initialize session state for selected prompt
if "selected_prompt" not in st.session_state:
    st.session_state.selected_prompt = None
    st.session_state.edit_mode = False

# Get prompts and create dataframe
prompts = list_prompts()
if prompts:
    # Create DataFrame
    df = pd.DataFrame(prompts)
    
    # Format the Last Modified column
    df['Last Modified'] = df['Last Modified'].dt.strftime('%Y-%m-%d')
    
    # Create columns with predefined layout
    cols = st.columns(TABLE_LAYOUTS['settings'])
    
    # Table headers with consistent styling
    for col, header in zip(cols, [
        PROMPTS_TABLE_HEADERS['name'],
        PROMPTS_TABLE_HEADERS['last_modified'],
        PROMPTS_TABLE_HEADERS['action']
    ]):
        col.markdown(f"<div class='table-header'>{header}</div>", unsafe_allow_html=True)
    
    # Display each prompt as a row with a button
    for idx, row in df.iterrows():
        cols = st.columns(TABLE_LAYOUTS['settings'])
        cols[0].markdown(f"<div class='table-cell'>{row['Name']}</div>", unsafe_allow_html=True)
        cols[1].markdown(f"<div class='table-cell'>{row['Last Modified']}</div>", unsafe_allow_html=True)
        if cols[2].button(VIEW_PROMPT_BUTTON, key=f"view_{idx}"):
            st.session_state.selected_prompt = row
            st.session_state.edit_mode = False
    
    # Display selected prompt content
    if st.session_state.selected_prompt is not None:
        st.markdown("---")
        with st.expander(PROMPT_EXPANDER_TITLE.format(st.session_state.selected_prompt['Name']), expanded=True):
            if st.session_state.edit_mode:
                edited_content = st.text_area(
                    EDIT_PROMPT_LABEL,
                    value=st.session_state.selected_prompt['Content'],
                    height=400
                )
                
                col1, col2, col3 = st.columns([1, 1, 4])
                
                if col1.button(CANCEL_BUTTON, key="cancel_edit"):
                    st.session_state.edit_mode = False
                    st.rerun()
                
                if col2.button(SAVE_BUTTON, key="save_prompt"):
                    # Get the file path
                    file_path = PROMPTS_DIR / st.session_state.selected_prompt['File']
                    try:
                        # Save the edited content
                        file_path.write_text(edited_content)
                        st.success(PROMPT_SAVE_SUCCESS)
                        # Update the content in session state
                        st.session_state.selected_prompt['Content'] = edited_content
                        st.session_state.edit_mode = False
                        st.rerun()
                    except Exception as e:
                        st.error(PROMPT_SAVE_ERROR.format(str(e)))
            else:
                st.text(st.session_state.selected_prompt['Content'])
                col1, col2, col3 = st.columns([1, 1, 4])
                
                if col1.button(CLOSE_BUTTON, key="close_prompt"):
                    st.session_state.selected_prompt = None
                    st.rerun()
                
                if col2.button(EDIT_BUTTON, key="edit_prompt"):
                    st.session_state.edit_mode = True
                    st.rerun()

else:
    st.write(NO_PROMPTS_FOUND)