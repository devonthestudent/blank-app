import streamlit as st
from typing import Dict, Any
from ..config.models_config import SUPPORTED_MODELS

class ModelSelector:
    def __init__(self):
        self.providers = list(SUPPORTED_MODELS.keys())
        self.models_by_provider = {
            provider: {
                model_id: config["name"]
                for model_id, config in models.items()
            }
            for provider, models in SUPPORTED_MODELS.items()
        }

    def render(self) -> Dict[str, Any]:
        """Render the model selection interface and return the selected model configuration."""
        st.sidebar.subheader("Model Selection")
        
        # Provider selection
        selected_provider = st.sidebar.selectbox(
            "Select Provider",
            self.providers,
            format_func=lambda x: x.capitalize()
        )

        # Model selection based on provider
        selected_model_id = st.sidebar.selectbox(
            "Select Model",
            list(self.models_by_provider[selected_provider].keys()),
            format_func=lambda x: self.models_by_provider[selected_provider][x]
        )

        # Get model configuration
        model_config = SUPPORTED_MODELS[selected_provider][selected_model_id]

        # Model parameters
        st.sidebar.subheader("Model Parameters")
        
        temperature = st.sidebar.slider(
            "Temperature",
            min_value=0.0,
            max_value=2.0,
            value=model_config["default_temperature"],
            step=0.1,
            help="Higher values make the output more random, lower values make it more deterministic."
        )

        max_tokens = st.sidebar.slider(
            "Max Tokens",
            min_value=1,
            max_value=model_config["context_length"],
            value=model_config["default_max_tokens"],
            step=1,
            help="Maximum number of tokens to generate in the response."
        )

        # System prompt
        st.sidebar.subheader("System Prompt")
        system_prompt = st.sidebar.text_area(
            "Custom System Prompt",
            value="",
            height=100,
            help="Optional system prompt to guide the model's behavior. Leave empty to use default."
        )

        return {
            "model_name": selected_model_id,
            "provider": selected_provider,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "system_prompt": system_prompt if system_prompt else None,
            "context_length": model_config["context_length"]
        } 