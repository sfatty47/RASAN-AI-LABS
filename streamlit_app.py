import streamlit as st
import os
import sys

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the main app
from app import *

# Set page config
st.set_page_config(
    page_title="RASAN AI Labs",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add a welcome message
st.title("Welcome to RASAN AI Labs")
st.markdown("""
    This is your AI-Powered AutoML Platform. The application will automatically:
    - Analyze your data
    - Select the best approach
    - Generate relevant visualizations
    - Train and optimize models
    - Provide actionable insights
""")

# Add a button to start
if st.button("Start Using RASAN AI Labs"):
    st.switch_page("app.py") 