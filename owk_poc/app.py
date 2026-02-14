"""
File contains implementation of app for the Agentic POC.
"""

import streamlit as st
import os
import sys

from owk_poc.agent import Agent

# Initialize the agent
if "agent" not in st.session_state:
    st.session_state.agent = Agent()

# UI Layout
st.set_page_config(page_title="GenAIAgent", page_icon="🧬")
st.title("🧬 Agentic POC")
st.markdown("Ask me about cancer genes and expression values.")

# Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("What would you like to know?"):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant"):
        response = st.session_state.agent.process_query(prompt)
        st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
