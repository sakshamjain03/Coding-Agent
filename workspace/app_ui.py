#!/usr/bin/env python3
# Streamlit UI for the unique binary search trees application

import streamlit as st
from main import uniqueBSTs

# Page configuration
st.set_page_config(
    page_title="Unique Binary Search Trees",
    page_icon="🌳",
    layout="wide"
)

# Title and description
st.title("🌳 Unique Binary Search Trees")
st.markdown("This application calculates the number of unique binary search trees that can be formed with n nodes.")

# Sidebar (if needed)
with st.sidebar:
    st.header("Settings")
    # Add settings/options here

# Main content
st.header("Calculate Unique Binary Search Trees")

# Input widgets
n = st.number_input("Enter the number of nodes (n):", min_value=0, max_value=100, value=10)

# Calculate and display results
if st.button("Calculate"):
    result = uniqueBSTs(n)
    st.write("The number of unique binary search trees that can be formed with {} nodes is: {}".format(n, result))

# Footer
st.divider()
st.caption("Created by Saksham")