import streamlit as st
import time
from typing import Dict, Any, Generator, Tuple
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
        if "thinking_tokens" not in st.session_state:
            st.session_state.thinking_tokens = 0
        if "response_tokens" not in st.session_state:
            st.session_state.response_tokens = 0

    def _extract_thinking_phase(self, text: str) -> Tuple[str, str]:
        """Extract thinking phase and response from text."""
        thinking = ""
        response = text

        if "<think>" in text and "</think>" in text:
            start_idx = text.find("<think>") + len("<think>")
            end_idx = text.find("</think>")
            if start_idx < end_idx:
                thinking = text[start_idx:end_idx].strip()
                response = text[end_idx + len("</think>"):].strip()

        return thinking, response

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
                # Create containers in desired order
                timer_container = st.empty()
                token_container = st.empty()
                thinking_container = st.empty()
                response_container = st.empty()
                
                start_time = time.time()
                full_response = ""
                thinking_buffer = ""
                displayed_response = ""
                thinking_phase = ""
                is_thinking = True
                end_tag_buffer = ""
                
                # Get model configuration from session state
                model_config = st.session_state.get("model_config", {})
                
                # Reset token counters
                st.session_state.thinking_tokens = 0
                st.session_state.response_tokens = 0
                
                # Generate response
                for chunk in self.api_handler.generate_response(
                    messages=self.memory_manager.get_messages(),
                    temperature=model_config.get("temperature"),
                    max_tokens=model_config.get("max_tokens"),
                    system_prompt=model_config.get("system_prompt")
                ):
                    if chunk.choices[0].delta.content:
                        content = chunk.choices[0].delta.content
                        full_response += content
                        
                        # Check for end of thinking phase
                        if is_thinking:
                            end_tag_buffer += content
                            if len(end_tag_buffer) > 8:  # Keep only last 8 characters
                                end_tag_buffer = end_tag_buffer[-8:]
                            
                            if "</think>" in full_response and is_thinking:
                                thinking_phase, remaining = self._extract_thinking_phase(full_response)
                                full_response = remaining
                                displayed_response = ""
                                is_thinking = False
                                
                                # Display final thinking phase in styled container
                                thinking_container.markdown(f"""
                                <div style='background-color: #f0f2f6; padding: 1rem; border-radius: 0.5rem; margin: 0.5rem 0;'>
                                    <div style='color: #666; font-style: italic;'>
                                        "{thinking_phase}"
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                # Update token count for thinking phase
                                st.session_state.thinking_tokens = len(thinking_phase.split())
                            else:
                                # Only display content up to potential partial </think> tag
                                safe_content = content
                                if "</th" in end_tag_buffer or "think>" in end_tag_buffer:
                                    safe_content = ""
                                thinking_buffer += safe_content
                                
                                with thinking_container:
                                    with st.spinner("Thinking..."):
                                        st.markdown(f"""
                                        <div style='background-color: #f0f2f6; padding: 1rem; border-radius: 0.5rem; margin: 0.5rem 0;'>
                                            <div style='color: #666; font-style: italic;'>
                                                "{thinking_buffer}"
                                            </div>
                                        </div>
                                        """, unsafe_allow_html=True)
                        else:
                            displayed_response += content
                            response_container.markdown(displayed_response + "▌")
                            st.session_state.response_tokens = len(displayed_response.split())
                        
                        # Update elapsed time and token counts
                        elapsed_time = time.time() - start_time
                        timer_container.markdown(f"⏱️ {elapsed_time:.1f}s")
                        token_container.markdown(
                            f"🤔 Thinking: {st.session_state.thinking_tokens} tokens | "
                            f"💭 Response: {st.session_state.response_tokens} tokens"
                        )
                
                # Final update
                if thinking_phase:
                    response_container.markdown(displayed_response)
                else:
                    # If no thinking phase was detected, treat everything as response
                    response_container.markdown(displayed_response)
                    st.session_state.response_tokens = len(displayed_response.split())
                    st.session_state.thinking_tokens = 0
                
                self.memory_manager.add_message("assistant", f"""
                <think>{thinking_phase}</think>
                {displayed_response}
                """.strip())

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
            st.markdown("""
                <style>
                .stApp {
                    background-color: #1E1E1E !important;
                    color: #FFFFFF;
                }
                .stChatMessage {
                    background-color: #2D2D2D !important;
                    border-radius: 10px;
                    padding: 10px;
                    margin: 5px 0;
                }
                .stMarkdown {
                    color: #FFFFFF;
                }
                .stTextInput input {
                    background-color: #2D2D2D !important;
                    color: #FFFFFF;
                }
                .stSelectbox select {
                    background-color: #2D2D2D !important;
                    color: #FFFFFF;
                }
                </style>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <style>
                .stApp {
                    background: linear-gradient(to bottom right, #fff5f5, #fff) !important;
                }
                .stChatMessage {
                    background-color: #FFFFFF;
                    border-radius: 10px;
                    padding: 10px;
                    margin: 5px 0;
                }
                </style>
                """, unsafe_allow_html=True) 