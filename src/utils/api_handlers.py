from typing import List, Dict, Any, Generator
import os
from litellm import completion
from ..config.models_config import SUPPORTED_MODELS, PROMPT_TEMPLATES, SYSTEM_PROMPTS

class APIHandler:
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.model_config = self._get_model_config()
        self.provider = self.model_config["provider"]
        self._setup_api_keys()

    def _get_model_config(self) -> Dict[str, Any]:
        """Get the configuration for the current model."""
        for provider, models in SUPPORTED_MODELS.items():
            if self.model_name in models:
                return models[self.model_name]
        raise ValueError(f"Model {self.model_name} not found in configuration")

    def _setup_api_keys(self):
        """Setup API keys for the provider."""
        if self.provider == "groq":
            if "GROQ_API_KEY" not in os.environ:
                raise ValueError("GROQ_API_KEY environment variable not set")
        elif self.provider == "replicate":
            if "REPLICATE_API_KEY" not in os.environ:
                raise ValueError("REPLICATE_API_KEY environment variable not set")

    def _format_messages(self, messages: List[Dict[str, str]], system_prompt: str = None) -> List[Dict[str, str]]:
        """Format messages according to the model's template."""
        formatted_messages = []

        # Add system message if provided
        if system_prompt:
            formatted_messages.append({
                "role": "system",
                "content": system_prompt
            })
        elif self.model_config.get("is_instruction"):
            formatted_messages.append({
                "role": "system",
                "content": SYSTEM_PROMPTS["instruction"]
            })

        # Add user and assistant messages without templates
        for msg in messages:
            if msg["role"] in ["user", "assistant"]:
                formatted_messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })

        return formatted_messages

    def generate_response(
        self,
        messages: List[Dict[str, str]],
        temperature: float = None,
        max_tokens: int = None,
        stream: bool = True,
        system_prompt: str = None
    ) -> Generator[Dict[str, Any], None, None]:
        """Generate a response from the model."""
        if temperature is None:
            temperature = self.model_config["default_temperature"]
        if max_tokens is None:
            max_tokens = self.model_config["default_max_tokens"]

        formatted_messages = self._format_messages(messages, system_prompt)

        try:
            response = completion(
                model=self.model_name,
                messages=formatted_messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=stream
            )

            if stream:
                for chunk in response:
                    if chunk.choices[0].delta.content:
                        yield chunk
            else:
                yield response

        except Exception as e:
            raise Exception(f"Error generating response: {str(e)}")

    def get_default_system_prompt(self) -> str:
        """Get the default system prompt for the model type."""
        model_type = "instruction" if self.model_config["is_instruction"] else "completion"
        return SYSTEM_PROMPTS[model_type] 