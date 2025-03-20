import streamlit as st
from typing import List, Dict, Any
from ..utils.tokenizer import Tokenizer

class MemoryManager:
    def __init__(self, model_name: str):
        self.tokenizer = Tokenizer(model_name)
        self._initialize_session_state()

    def _initialize_session_state(self):
        """Initialize session state variables for chat memory."""
        if "messages" not in st.session_state:
            st.session_state.messages = []
        if "max_memory_tokens" not in st.session_state:
            st.session_state.max_memory_tokens = self.tokenizer.get_available_tokens()

    def render_memory_settings(self):
        """Render memory management settings in the sidebar."""
        st.sidebar.subheader("Memory Management")
        
        # Memory limit slider
        max_tokens = self.tokenizer.get_available_tokens()
        st.session_state.max_memory_tokens = st.sidebar.slider(
            "Max Memory Tokens",
            min_value=100,
            max_value=max_tokens,
            value=st.session_state.max_memory_tokens,
            step=100,
            help="Maximum number of tokens to keep in chat history. Older messages will be removed when exceeded."
        )

        # Display current token usage
        current_tokens = self.tokenizer.count_conversation_tokens(st.session_state.messages)
        st.sidebar.metric(
            "Current Token Usage",
            f"{current_tokens}/{st.session_state.max_memory_tokens}"
        )

        # Clear chat button
        if st.sidebar.button("Clear Chat History"):
            self.clear_messages()

    def add_message(self, role: str, content: str):
        """Add a message to the chat history and manage memory."""
        st.session_state.messages.append({"role": role, "content": content})
        self._manage_memory()

    def _manage_memory(self):
        """Manage chat memory by truncating if necessary."""
        current_tokens = self.tokenizer.count_conversation_tokens(st.session_state.messages)
        if current_tokens > st.session_state.max_memory_tokens:
            st.session_state.messages = self.tokenizer.truncate_conversation(
                st.session_state.messages,
                st.session_state.max_memory_tokens
            )

    def clear_messages(self):
        """Clear all messages from chat history."""
        st.session_state.messages = []

    def get_messages(self) -> List[Dict[str, str]]:
        """Get all messages in chat history."""
        return st.session_state.messages

    def get_token_usage(self) -> Dict[str, int]:
        """Get current token usage statistics."""
        current_tokens = self.tokenizer.count_conversation_tokens(st.session_state.messages)
        return {
            "current": current_tokens,
            "max": st.session_state.max_memory_tokens
        } 