import streamlit as st
from core.strings import *

st.set_page_config(
    page_title=HOME_PAGE_TITLE,
    page_icon=HOME_PAGE_ICON,
    layout=HOME_PAGE_LAYOUT
)

st.title(SIDEBAR_HEADER)
st.write(SIDEBAR_SUBHEADER)

st.markdown(HOME_PAGE_WELCOME)