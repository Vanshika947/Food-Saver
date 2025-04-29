import streamlit as st
import os
import pandas as pd
from datetime import datetime, timedelta
from utils.data_manager import load_data, save_data, load_points
from utils.notifications import check_expiring_items

# Initialize session state variables if they don't exist
if 'items_df' not in st.session_state:
    st.session_state.items_df = load_data()
    
if 'points' not in st.session_state:
    # Initialize points from data
    st.session_state.points = load_points()

# Page configuration
st.set_page_config(
    page_title="FoodSaver - Expiry Date Tracker",
    page_icon="🍲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main page
st.title("🍲 FoodSaver")
st.subheader("Track food expiry dates and reduce waste")

# Remove OpenAI API key hint as we're not using it anymore

# Check for expiring items and show notifications
expiring_items = check_expiring_items(st.session_state.items_df)
if expiring_items is not None and not expiring_items.empty:
    st.warning(f"⚠️ You have {len(expiring_items)} items expiring soon! Check your dashboard.")

# Display points
st.sidebar.title("Rewards")
st.sidebar.metric("Total Points", st.session_state.points)
st.sidebar.write("Earn points by scanning and tracking items!")

# Main page content
col1, col2 = st.columns(2)

with col1:
    st.header("How it works")
    st.write("""
    1. Scan food items using your camera
    2. We'll extract the expiry date automatically
    3. Get notified before items expire
    4. Earn points for every scan
    """)
    st.image("https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/svg/1f4f8.svg", width=100)

with col2:
    st.header("Quick Stats")
    
    # Calculate stats
    total_items = len(st.session_state.items_df)
    
    if not st.session_state.items_df.empty:
        expiring_soon = len(st.session_state.items_df[
            (st.session_state.items_df['expiry_date'] <= (datetime.now() + timedelta(days=15)).strftime('%Y-%m-%d')) & 
            (st.session_state.items_df['expiry_date'] >= datetime.now().strftime('%Y-%m-%d'))
        ])
        expired = len(st.session_state.items_df[
            st.session_state.items_df['expiry_date'] < datetime.now().strftime('%Y-%m-%d')
        ])
    else:
        expiring_soon = 0
        expired = 0
    
    col2_1, col2_2, col2_3 = st.columns(3)
    col2_1.metric("Total Items", total_items)
    col2_2.metric("Expiring Soon", expiring_soon)
    col2_3.metric("Expired", expired)

# Navigation
st.header("Navigation")
nav_col1, nav_col2, nav_col3 = st.columns(3)

with nav_col1:
    if st.button("📊 Dashboard", use_container_width=True):
        st.switch_page("pages/dashboard.py")

with nav_col2:
    if st.button("📷 Scan New Item", use_container_width=True):
        st.switch_page("pages/scan_item.py")

with nav_col3:
    if st.button("🏆 Rewards", use_container_width=True):
        st.switch_page("pages/rewards.py")

# Footer
st.markdown("---")
st.markdown("FoodSaver - Save Food, Save Money, Earn Rewards")
