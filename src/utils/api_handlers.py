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
        for provider, companies in SUPPORTED_MODELS.items():
            for company, models in companies.items():
                for model_id, config in models.items():
                    if model_id == self.model_name:
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
        elif self.provider == "gemini":
            if "GEMINI_API_KEY" not in os.environ:
                raise ValueError("GEMINI_API_KEY environment variable not set")

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

        # Use model-specific system prompt if available
        if system_prompt is None and "model_type" in self.model_config:
            system_prompt = self.get_default_system_prompt()

        formatted_messages = self._format_messages(messages, system_prompt)

        try:
            # Add specific configuration for OpenRouter
            if self.provider == "openrouter":
                # Create the completion request with OpenRouter-specific parameters
                completion_kwargs = {
                    "model": self.model_name,
                    "messages": formatted_messages,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                    "stream": stream,
                    "drop_params": True,  # Drop unsupported parameters
                    "merge_reasoning_content_in_choices": True,  # Keep original content structure
                    "extra_body": {
                        "reasoning": {
                            "effort": "high",
                            "exclude": False
                        }
                    }
                }
                
                response = completion(**completion_kwargs)
            # Add specific configuration for Replicate
            elif self.provider == "replicate":
                response = completion(
                    model=self.model_name,
                    messages=formatted_messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    stream=stream,
                    max_retries=3,  # Add retries for reliability
                    timeout=120  # Increase timeout for longer responses
                )
            else:
                response = completion(
                    model=self.model_name,
                    messages=formatted_messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    stream=stream
                )

            if stream:
                for chunk in response:
                    # Handle different response formats
                    content = None
                    reasoning = None
                    thinking_blocks = None
                    original_content = None
                    
                    # Extract content and reasoning from different response formats
                    if hasattr(chunk, 'choices') and chunk.choices:
                        if hasattr(chunk.choices[0], 'delta'):
                            if hasattr(chunk.choices[0].delta, 'content'):
                                content = chunk.choices[0].delta.content
                            if hasattr(chunk.choices[0].delta, 'reasoning_content'):
                                reasoning = chunk.choices[0].delta.reasoning_content
                            if hasattr(chunk.choices[0].delta, 'thinking_blocks'):
                                thinking_blocks = chunk.choices[0].delta.thinking_blocks
                            # Get original content if available
                            if hasattr(chunk.choices[0].delta, 'provider_specific_fields'):
                                original_content = chunk.choices[0].delta.provider_specific_fields.get('original_content')
                        elif hasattr(chunk.choices[0], 'text'):
                            content = chunk.choices[0].text
                        elif hasattr(chunk.choices[0], 'content'):
                            content = chunk.choices[0].content
                    elif isinstance(chunk, dict):
                        if 'choices' in chunk:
                            if 'delta' in chunk['choices'][0]:
                                content = chunk['choices'][0]['delta'].get('content', '')
                                reasoning = chunk['choices'][0]['delta'].get('reasoning_content', '')
                                thinking_blocks = chunk['choices'][0]['delta'].get('thinking_blocks', [])
                                # Get original content if available
                                if 'provider_specific_fields' in chunk['choices'][0]['delta']:
                                    original_content = chunk['choices'][0]['delta']['provider_specific_fields'].get('original_content')
                            elif 'text' in chunk['choices'][0]:
                                content = chunk['choices'][0]['text']
                            elif 'content' in chunk['choices'][0]:
                                content = chunk['choices'][0]['content']
                        elif 'content' in chunk:
                            content = chunk['content']
                    elif isinstance(chunk, str):
                        content = chunk.strip()
                    elif hasattr(chunk, 'content'):
                        content = chunk.content

                    # If we have any content, reasoning, or thinking blocks, yield it
                    if content or reasoning or thinking_blocks or original_content:
                        yield {
                            "choices": [{
                                "delta": {
                                    "content": original_content if original_content else content if content else "",
                                    "reasoning": reasoning if reasoning else "",
                                    "thinking_blocks": thinking_blocks if thinking_blocks else [],
                                    "provider_specific_fields": {
                                        "original_content": original_content if original_content else None
                                    }
                                }
                            }]
                        }
            else:
                if hasattr(response, 'choices') and response.choices:
                    yield response
                elif isinstance(response, str) and response.strip():
                    yield {
                        "choices": [{
                            "message": {"content": response}
                        }]
                    }

        except Exception as e:
            print(f"Debug - Error in generate_response: {str(e)}")  # Add debug print
            raise Exception(f"Error generating response: {str(e)}")

    def get_default_system_prompt(self) -> str:
        """Get the default system prompt for the model type."""
        if "model_type" in self.model_config:
            return SYSTEM_PROMPTS[self.model_config["model_type"]]
        model_type = "instruction" if self.model_config["is_instruction"] else "completion"
        return SYSTEM_PROMPTS[model_type]       