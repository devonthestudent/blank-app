import streamlit as st
import os
from src.components.model_selector import ModelSelector
from src.components.chat import ChatInterface
from src.components.memory import MemoryManager

# Page configuration
st.set_page_config(
    page_title="AI Chat Interface",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize components
model_selector = ModelSelector()

# Sidebar
with st.sidebar:
    st.title("🤖 AI Chat Interface")
    
    # API Key inputs
    st.subheader("API Keys")
    groq_key = st.text_input("Groq API Key", type="password")
    replicate_key = st.text_input("Replicate API Key", type="password")
    
    # Set API keys in environment
    if groq_key:
        os.environ["GROQ_API_KEY"] = groq_key
    if replicate_key:
        os.environ["REPLICATE_API_KEY"] = replicate_key
    
    # Model selection and configuration
    model_config = model_selector.render()
    
    # Store model configuration in session state
    st.session_state["model_config"] = model_config

# Main chat interface
st.title("Chat with AI")

# Initialize chat interface with selected model
chat_interface = ChatInterface(model_config["model_name"])

# Render memory settings
chat_interface.memory_manager.render_memory_settings()

# Render theme selector
chat_interface.render_theme_selector()

# Render chat interface
chat_interface.render()

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center'>
        <p>Built with ❤️ using Streamlit and LiteLLM</p>
        <p>Supporting Groq and Replicate models</p>
    </div>
""", unsafe_allow_html=True)
