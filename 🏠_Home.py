import streamlit as st
from core.strings import *

st.set_page_config(
    page_title="Pitch Perfect",
    page_icon="🎯",
    layout="centered"
)

st.title(SIDEBAR_HEADER)
st.markdown(HOME_PAGE_WELCOME)