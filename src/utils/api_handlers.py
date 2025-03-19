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
            for model_id, config in models.items():
                if model_id in self.model_name:
                    return config
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
        template = PROMPT_TEMPLATES[self.provider]
        formatted_messages = []

        # Add system message if provided
        if system_prompt:
            formatted_messages.append({
                "role": "system",
                "content": f"{template['system']['pre_message']}{system_prompt}{template['system']['post_message']}"
            })

        # Format user and assistant messages
        for msg in messages:
            if msg["role"] in ["user", "assistant"]:
                formatted_messages.append({
                    "role": msg["role"],
                    "content": f"{template[msg['role']]['pre_message']}{msg['content']}{template[msg['role']]['post_message']}"
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
                buffer = ""
                for chunk in response:
                    # Handle different response formats
                    content = None
                    
                    # Extract content from different response formats
                    if hasattr(chunk, 'choices') and chunk.choices:
                        if hasattr(chunk.choices[0], 'delta') and hasattr(chunk.choices[0].delta, 'content'):
                            content = chunk.choices[0].delta.content
                        elif hasattr(chunk.choices[0], 'text'):
                            content = chunk.choices[0].text
                    elif isinstance(chunk, str):
                        content = chunk

                    # Process content if we have it
                    if content:
                        buffer += content
                        # If we have a complete thinking section, yield it
                        if "<think>" in buffer and "</think>" in buffer:
                            think_start = buffer.find("<think>")
                            think_end = buffer.find("</think>") + len("</think>")
                            think_content = buffer[think_start:think_end]
                            yield {
                                "choices": [{
                                    "delta": {"content": think_content}
                                }]
                            }
                            # Keep the rest for the next part
                            buffer = buffer[think_end:].lstrip()
                        # If we have content outside thinking tags, yield it
                        elif not ("<think>" in buffer or "</think>" in buffer):
                            yield {
                                "choices": [{
                                    "delta": {"content": content}
                                }]
                            }
                            buffer = ""
                
                # Yield any remaining content
                if buffer.strip():
                    yield {
                        "choices": [{
                            "delta": {"content": buffer}
                        }]
                    }
            else:
                if hasattr(response, 'choices') and response.choices:
                    yield response
                elif isinstance(response, str):
                    yield {
                        "choices": [{
                            "message": {"content": response}
                        }]
                    }

        except Exception as e:
            raise Exception(f"Error generating response: {str(e)}")

    def get_default_system_prompt(self) -> str:
        """Get the default system prompt for the model type."""
        model_type = "instruction" if self.model_config["is_instruction"] else "completion"
        return SYSTEM_PROMPTS[model_type] 