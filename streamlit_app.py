# Import required libraries
import streamlit as st
import os
from src.components.model_selector import ModelSelector
from src.components.chat import ChatInterface
from src.components.memory import MemoryManager

# Page configuration must be the first Streamlit command
st.set_page_config(
    page_title="Chat with Jane",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initial theme styling
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to bottom right, #fff5f5, #fff);
    }
    .stButton button {
        background-color: #ffb6c1;
        color: white;
        border-radius: 20px;
    }
    .stButton button:hover {
        background-color: #ff69b4;
    }
    .stRadio label {
        color: #db7093;
    }
    .stCheckbox label {
        color: #db7093;
    }
    .stTitle {
        color: #db7093;
    }
    .stSubheader {
        color: #c71585;
    }
    .stChatMessage {
        border-radius: 15px;
        padding: 10px;
        margin: 5px 0;
    }
    .stChatInput {
        border-radius: 20px;
    }
    .stTextInput input {
        border-radius: 20px;
    }
    .stSelectbox select {
        border-radius: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for API keys if not exists
if 'GROQ_API_KEY' not in st.session_state:
    # Try to get the key from secrets first
    try:
        st.session_state.GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
        os.environ["GROQ_API_KEY"] = st.session_state.GROQ_API_KEY
    except:
        st.session_state.GROQ_API_KEY = None

if 'REPLICATE_API_KEY' not in st.session_state:
    st.session_state.REPLICATE_API_KEY = None

if 'use_custom_groq_key' not in st.session_state:
    st.session_state.use_custom_groq_key = False

# Sidebar
with st.sidebar:
    st.title("🌸 Chat Assistant")
    
    # API Provider Selection
    st.subheader("Select API Provider")
    api_provider = st.radio(
        "Choose your API provider:",
        [
            "Free (Groq)",
            "Premium (Replicate)",
            "Google Gemini (Free Tier)",
            "OpenRouter"
        ],
        help="Select which API provider you want to use. Groq offers free access to preview models, Replicate provides premium model access, Gemini is Google's advanced AI, and OpenRouter is a new provider."
    )

    # API Key Input based on selection
    st.subheader("API Key Configuration")
    
    if api_provider == "Free (Groq)":
        st.session_state.use_custom_groq_key = st.checkbox(
            "Use custom Groq API key",
            value=st.session_state.use_custom_groq_key,
            help="Check this box if you want to use your own Groq API key instead of the default one"
        )

        if st.session_state.use_custom_groq_key:
            if st.session_state.GROQ_API_KEY and st.session_state.GROQ_API_KEY != st.secrets.get("GROQ_API_KEY", ""):
                st.success('Custom Groq API key already provided!', icon='✨')
            else:
                groq_key = st.text_input("Enter your Groq API Key", type="password")
                if groq_key:
                    st.session_state.GROQ_API_KEY = groq_key
                    os.environ["GROQ_API_KEY"] = groq_key
                    st.success('Custom Groq API key successfully loaded!', icon='✨')
        else:
            if st.secrets.get("GROQ_API_KEY"):
                st.success('Using default Groq API key', icon='✨')
                st.session_state.GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
                os.environ["GROQ_API_KEY"] = st.session_state.GROQ_API_KEY
            else:
                st.error('Default Groq API key not found in secrets!', icon='💫')
                st.session_state.GROQ_API_KEY = None

    elif api_provider == "Premium (Replicate)":
        if st.session_state.REPLICATE_API_KEY:
            st.success('Replicate API key already provided!', icon='✨')
        else:
            replicate_key = st.text_input("Enter Replicate API Key", type="password")
            if replicate_key:
                if replicate_key.startswith('r8_') and len(replicate_key) == 40:
                    st.session_state.REPLICATE_API_KEY = replicate_key
                    os.environ["REPLICATE_API_KEY"] = replicate_key
                    st.success('Replicate API key successfully loaded!', icon='✨')
                else:
                    st.error('Invalid Replicate API key format. It should start with "r8_" and be 40 characters long.')

    elif api_provider == "Google Gemini (Free Tier)":
        if 'use_custom_gemini_key' not in st.session_state:
            st.session_state.use_custom_gemini_key = False
        st.session_state.use_custom_gemini_key = st.checkbox(
            "Use custom Gemini API key",
            value=st.session_state.use_custom_gemini_key,
            help="Check this box if you want to use your own Gemini API key instead of the default one"
        )
        if st.session_state.use_custom_gemini_key:
            if st.session_state.get("GEMINI_API_KEY") and st.session_state.GEMINI_API_KEY != st.secrets.get("GEMINI_API_KEY", ""):
                st.success('Custom Gemini API key already provided!', icon='✨')
            else:
                gemini_key = st.text_input("Enter your Gemini API Key", type="password")
                if gemini_key:
                    st.session_state.GEMINI_API_KEY = gemini_key
                    os.environ["GEMINI_API_KEY"] = gemini_key
                    st.success('Custom Gemini API key successfully loaded!', icon='✨')
        else:
            if st.secrets.get("GEMINI_API_KEY"):
                st.success('Using default Gemini API key', icon='✨')
                st.session_state.GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
                os.environ["GEMINI_API_KEY"] = st.session_state.GEMINI_API_KEY
            else:
                st.error('Default Gemini API key not found in secrets!', icon='💫')
                st.session_state.GEMINI_API_KEY = None

    elif api_provider == "OpenRouter":
        if 'use_custom_openrouter_key' not in st.session_state:
            st.session_state.use_custom_openrouter_key = False
        st.session_state.use_custom_openrouter_key = st.checkbox(
            "Use custom OpenRouter API key",
            value=st.session_state.use_custom_openrouter_key,
            help="Check this box if you want to use your own OpenRouter API key instead of the default one"
        )
        if st.session_state.use_custom_openrouter_key:
            if st.session_state.get("OPENROUTER_API_KEY") and st.session_state.OPENROUTER_API_KEY != st.secrets.get("OPENROUTER_API_KEY", ""):
                st.success('Custom OpenRouter API key already provided!', icon='✨')
            else:
                openrouter_key = st.text_input("Enter OpenRouter API Key", type="password")
                if openrouter_key:
                    st.session_state.OPENROUTER_API_KEY = openrouter_key
                    os.environ["OPENROUTER_API_KEY"] = openrouter_key
                    st.success('OpenRouter API key successfully loaded!', icon='✨')
        else:
            if st.secrets.get("OPENROUTER_API_KEY"):
                st.success('Using default OpenRouter API key', icon='✨')
                st.session_state.OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
                os.environ["OPENROUTER_API_KEY"] = st.session_state.OPENROUTER_API_KEY
            else:
                st.error('Default OpenRouter API key not found in secrets!', icon='💫')
                st.session_state.OPENROUTER_API_KEY = None

    # Only show model selection if API key is provided
    if ((api_provider == "Free (Groq)" and st.session_state.GROQ_API_KEY) or 
        (api_provider == "Premium (Replicate)" and st.session_state.REPLICATE_API_KEY) or
        (api_provider == "Google Gemini (Free Tier)" and st.session_state.GEMINI_API_KEY) or
        (api_provider == "OpenRouter" and st.session_state.OPENROUTER_API_KEY)):
        # Map provider option to correct provider for ModelSelector
        selector_provider = (
            "replicate" if api_provider == "Premium (Replicate)" else
            "gemini" if api_provider == "Google Gemini (Free Tier)" else
            "openrouter" if api_provider == "OpenRouter" else
            "groq"
        )
        st.write("api_provider:", api_provider, "selector_provider:", selector_provider)
        model_selector = ModelSelector(selector_provider)
        model_config = model_selector.render()
        st.session_state["model_config"] = model_config
        if "model_config" in st.session_state:
            chat_interface = ChatInterface(model_config["model_name"])
            chat_interface.memory_manager.render_memory_settings()
    else:
        st.info("Please enter your API key to access the models.", icon="🎀")

# Main chat interface
if "model_config" in st.session_state:
    st.title("Chat with Jane 💝")
    
    # Initialize and render chat interface
    chat_interface = ChatInterface(st.session_state["model_config"]["model_name"])
    chat_interface.render()
else:
    st.title("Welcome to Jane's Chat Space 💖")
    st.info("Please configure your API key and select a model in the sidebar to start chatting.", icon="🎀")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center'>
        <p style='color: #db7093;'>Created with 💝 by D the student using LiteLLM</p>
        <p style='color: #c71585;'>Powered by Groq and Replicate models</p>
        <p style='color: #ffb6c1; font-size: 0.8em;'>Made with Cursor</p>
    </div>
""", unsafe_allow_html=True)
