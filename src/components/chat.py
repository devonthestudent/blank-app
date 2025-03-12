import streamlit as st
from typing import Dict, Any, Generator
from ..utils.api_handlers import APIHandler
from .memory import MemoryManager

class ChatInterface:
    def __init__(self, model_name: str):
        self.api_handler = APIHandler(model_name)
        self.memory_manager = MemoryManager(model_name)
        self._initialize_session_state()

    def _initialize_session_state(self):
        """Initialize session state variables for the chat interface."""
        if "is_processing" not in st.session_state:
            st.session_state.is_processing = False

    def render(self):
        """Render the chat interface."""
        # Display chat messages
        for message in self.memory_manager.get_messages():
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Chat input
        if prompt := st.chat_input(disabled=st.session_state.is_processing):
            self._handle_user_input(prompt)

    def _handle_user_input(self, prompt: str):
        """Handle user input and generate response."""
        # Add user message to chat
        self.memory_manager.add_message("user", prompt)
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate and display assistant response
        with st.chat_message("assistant"):
            st.session_state.is_processing = True
            try:
                response_placeholder = st.empty()
                full_response = ""
                
                # Get model configuration from session state
                model_config = st.session_state.get("model_config", {})
                
                # Generate response
                for chunk in self.api_handler.generate_response(
                    messages=self.memory_manager.get_messages(),
                    temperature=model_config.get("temperature"),
                    max_tokens=model_config.get("max_tokens"),
                    system_prompt=model_config.get("system_prompt")
                ):
                    if chunk.choices[0].delta.content:
                        full_response += chunk.choices[0].delta.content
                        response_placeholder.markdown(full_response + "▌")
                
                response_placeholder.markdown(full_response)
                self.memory_manager.add_message("assistant", full_response)

            except Exception as e:
                st.error(f"Error generating response: {str(e)}")
            finally:
                st.session_state.is_processing = False

    def render_theme_selector(self):
        """Render theme selection in the sidebar."""
        st.sidebar.subheader("Theme")
        theme = st.sidebar.selectbox(
            "Select Theme",
            ["Light", "Dark"],
            key="theme"
        )
        if theme == "Dark":
            st.set_page_config(page_title="AI Chat", layout="wide", initial_sidebar_state="expanded")
            st.markdown("""
                <style>
                .stApp {
                    background-color: #1E1E1E;
                    color: #FFFFFF;
                }
                .stChatMessage {
                    background-color: #2D2D2D;
                    border-radius: 10px;
                    padding: 10px;
                    margin: 5px 0;
                }
                </style>
                """, unsafe_allow_html=True) 