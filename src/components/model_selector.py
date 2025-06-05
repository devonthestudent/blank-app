import streamlit as st
from typing import Dict, Any
from ..config.models_config import SUPPORTED_MODELS

class ModelSelector:
    def __init__(self, api_provider: str):
        self.api_provider = api_provider
        if api_provider == "Premium (Replicate)":
            self.provider = "replicate"
        elif api_provider == "Google Gemini (Free Tier)":
            self.provider = "gemini"
        else:
            self.provider = "groq"

        # Special handling for Gemini: no company grouping
        if self.provider == "gemini":
            # Flatten all gemini models into a single dict, show name and model_id for uniqueness
            self.gemini_models = {
                model_id: f"{config['name']} ({model_id})"
                for model_id, config in SUPPORTED_MODELS["gemini"]["gemini"].items()
                if config.get("provider") == "gemini"
            }
        else:
            # Filter companies based on provider
            self.companies = [
                company for company, models in SUPPORTED_MODELS[self.provider].items()
                if any(config.get("provider") == self.provider for config in models.values())
            ]
            # Filter models by provider
            self.models_by_company = {
                company: {
                    model_id: config["name"]
                    for model_id, config in models.items()
                    if config.get("provider") == self.provider
                }
                for company, models in SUPPORTED_MODELS[self.provider].items()
                if any(config.get("provider") == self.provider for config in models.values())
            }

    def render(self) -> Dict[str, Any]:
        """Render the model selection interface and return the selected model configuration."""
        st.sidebar.subheader("Model Selection")
        if self.provider == "gemini":
            selected_model_id = st.sidebar.selectbox(
                "Select Gemini Model",
                list(self.gemini_models.keys()),
                format_func=lambda x: self.gemini_models[x],
                help="Select a Gemini model"
            )
            # Find the config for the selected model
            model_config = None
            for company, models in SUPPORTED_MODELS.items():
                if selected_model_id in models:
                    model_config = models[selected_model_id]
                    break
        else:
            # Company selection
            selected_company = st.sidebar.selectbox(
                "Select Company",
                self.companies,
                format_func=lambda x: x.capitalize(),
                help="Select the AI company whose models you want to use"
            )
            # Model selection based on company
            selected_model_id = st.sidebar.selectbox(
                "Select Model",
                list(self.models_by_company[selected_company].keys()),
                format_func=lambda x: self.models_by_company[selected_company][x],
                help=f"Select a specific model from {selected_company.capitalize()}"
            )
            # Get model configuration
            model_config = SUPPORTED_MODELS[selected_company][selected_model_id]

        # Display model information
        st.sidebar.markdown(f"""
        **Model Info:**
        - Context Length: {model_config['context_length']:,} tokens
        - Provider: {model_config['provider'].capitalize()}
        """)

        # Model parameters
        st.sidebar.subheader("Model Parameters")
        temperature = st.sidebar.slider(
            "Temperature",
            min_value=0.0,
            max_value=2.0,
            value=model_config.get("default_temperature",0.3),
            step=0.1,
            help="Higher values make the output more random, lower values make it more deterministic."
        )
        max_tokens = st.sidebar.slider(
            "Max Tokens",
            min_value=1,
            max_value=model_config["context_length"],
            value=min(model_config.get("default_max_tokens",4000), model_config["context_length"]),
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
        # Add a note about preview models
        if model_config["provider"] == "groq":
            st.sidebar.warning(
                "Note: These are preview models intended for evaluation purposes only. "
                "They may be discontinued at short notice."
            )
        return {
            "model_name": selected_model_id,
            "provider": model_config["provider"],
            "temperature": temperature,
            "max_tokens": max_tokens,
            "system_prompt": system_prompt if system_prompt else None,
            "context_length": model_config["context_length"]
        } 