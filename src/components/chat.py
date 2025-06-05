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
        # Add clear chat button
        col1, col2 = st.columns([6, 1])
        with col2:
            if st.button("Clear Chat 🗑️", use_container_width=True):
                self.memory_manager.clear_messages()
                st.rerun()

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
                error_container = st.empty()
                
                start_time = time.time()
                full_response = ""
                thinking_buffer = ""
                displayed_response = ""
                thinking_phase = ""
                is_thinking = False  # Default to not thinking unless we see <think>
                end_tag_buffer = ""
                has_received_content = False
                
                # Get model configuration from session state
                model_config = st.session_state.get("model_config", {})
                if not model_config:
                    raise ValueError("Model configuration not found in session state")
                
                # Reset token counters
                st.session_state.thinking_tokens = 0
                st.session_state.response_tokens = 0
                
                try:
                    # Generate response
                    for chunk in self.api_handler.generate_response(
                        messages=self.memory_manager.get_messages(),
                        temperature=model_config.get("temperature"),
                        max_tokens=model_config.get("max_tokens"),
                        system_prompt=model_config.get("system_prompt")
                    ):
                        # Extract content from different response formats
                        content = None
                        reasoning = None
                        if isinstance(chunk, dict):
                            if 'choices' in chunk:
                                if 'delta' in chunk['choices'][0]:
                                    content = chunk['choices'][0]['delta'].get('content', '')
                                    reasoning = chunk['choices'][0]['delta'].get('reasoning', '')
                                    if 'text' in chunk['choices'][0]:
                                        content = chunk['choices'][0]['text']
                                    elif 'message' in chunk['choices'][0]:
                                        content = chunk['choices'][0]['message'].get('content', '')
                                    elif 'content' in chunk['choices'][0]:
                                        content = chunk['choices'][0]['content']
                                elif 'content' in chunk:
                                    content = chunk['content']
                            elif 'content' in chunk:
                                content = chunk['content']
                        elif isinstance(chunk, str):
                            content = chunk
                        elif hasattr(chunk, 'content'):
                            content = chunk.content

                        if content or reasoning:
                            has_received_content = True
                            if reasoning:
                                full_response += f"\n\nReasoning:\n{reasoning}\n\nResponse:\n"
                            full_response += content
                            displayed_response += content
                            
                            # Display reasoning if available
                            if reasoning:
                                with thinking_container:
                                    st.markdown(f"""
                                    <div style='background-color: #f0f2f6; padding: 1rem; border-radius: 0.5rem; margin: 0.5rem 0;'>
                                        <div style='color: #666; font-style: italic;'>
                                            {reasoning}
                                        </div>
                                    </div>
                                    """, unsafe_allow_html=True)
                            
                            # Display the response
                            response_container.markdown(
                                displayed_response,
                                unsafe_allow_html=True
                            )
                            st.session_state.response_tokens = len(displayed_response.split())
                            
                            # Update elapsed time and token counts
                            elapsed_time = time.time() - start_time
                            timer_container.markdown(f"⏱️ {elapsed_time:.1f}s")
                            token_container.markdown(
                                f"💭 Response: {st.session_state.response_tokens} tokens"
                            )
                    
                    # Final update - only if we've received any content
                    if has_received_content:
                        final_response = displayed_response.strip()
                        if final_response:
                            # Display final response without cursor
                            response_container.markdown(final_response)
                            # Add to memory
                            self.memory_manager.add_message("assistant", final_response)
                        else:
                            error_container.warning("Response was empty after processing.")
                    else:
                        error_container.warning("No response was generated by the model.")

                except Exception as e:
                    error_msg = f"Error during response generation: {str(e)}"
                    error_container.error(error_msg)
                    st.error(f"Model: {model_config.get('model_name', 'Unknown')}")
                    st.error(f"Provider: {model_config.get('provider', 'Unknown')}")

            except Exception as e:
                st.error(f"Error in chat interface: {str(e)}")
            finally:
                st.session_state.is_processing = False 