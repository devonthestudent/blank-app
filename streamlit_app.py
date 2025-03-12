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

# Initialize session state for API keys if not exists
if 'GROQ_API_KEY' not in st.session_state:
    st.session_state.GROQ_API_KEY = None
if 'REPLICATE_API_KEY' not in st.session_state:
    st.session_state.REPLICATE_API_KEY = None

# Sidebar
with st.sidebar:
    st.title("🤖 AI Chat Interface")
    
    # API Provider Selection
    st.subheader("Select API Provider")
    api_provider = st.radio(
        "Choose your API provider:",
        ["Free (Groq)", "Premium (Replicate)"],
        help="Select which API provider you want to use. Groq offers free access to preview models, while Replicate provides premium model access."
    )

    # API Key Input based on selection
    st.subheader("API Key Configuration")
    
    if api_provider == "Free (Groq)":
        if st.session_state.GROQ_API_KEY:
            st.success('Groq API key already provided!', icon='✅')
        else:
                  groq_key = st.text_input("Enter Groq API Key", type="password")
            if groq_key:
                st.session_state.GROQ_API_KEY = groq_key
                os.environ["GROQ_API_KEY"] = groq_key
                st.success('Groq API key successfully loaded!', icon='✅')
    else:  # Premium (Replicate)
        if st.session_state.REPLICATE_API_KEY:
            st.success('Replicate API key already provided!', icon='✅')
        else:
            replicate_key = st.text_input("Enter Replicate API Key", type="password")
            if replicate_key:
                if replicate_key.startswith('r8_') and len(replicate_key) == 40:
                    st.session_state.REPLICATE_API_KEY = replicate_key
                    os.environ["REPLICATE_API_KEY"] = replicate_key
                    st.success('Replicate API key successfully loaded!', icon='✅')
                else:
                    st.error('Invalid Replicate API key format. It should start with "r8_" and be 40 characters long.')

    # Only show model selection if API key is provided
    if ((api_provider == "Free (Groq)" and st.session_state.GROQ_API_KEY) or 
        (api_provider == "Premium (Replicate)" and st.session_state.REPLICATE_API_KEY)):
        
        # Initialize model selector
        model_selector = ModelSelector(api_provider)
        
        # Model selection and configuration
        model_config = model_selector.render()
        
        # Store model configuration in session state
        st.session_state["model_config"] = model_config

        # Render memory settings if model is selected
        if "model_config" in st.session_state:
            chat_interface = ChatInterface(model_config["model_name"])
            chat_interface.memory_manager.render_memory_settings()
            chat_interface.render_theme_selector()
    else:
        st.info("Please enter your API key to access the models.", icon="ℹ️")

# Main chat interface
if "model_config" in st.session_state:
    st.title("Chat with AI")
    
    # Initialize and render chat interface
    chat_interface = ChatInterface(st.session_state["model_config"]["model_name"])
    chat_interface.render()
else:
    st.title("Welcome to AI Chat Interface")
    st.info("Please configure your API key and select a model in the sidebar to start chatting.", icon="👈")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center'>
        <p>Built with ❤️ using Streamlit and LiteLLM</p>
        <p>Supporting Groq and Replicate models</p>
    </div>
""", unsafe_allow_html=True)
