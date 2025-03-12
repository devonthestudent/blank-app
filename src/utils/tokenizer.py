from typing import List, Dict, Any
import tiktoken
from ..config.models_config import SUPPORTED_MODELS

class Tokenizer:
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.encoding = tiktoken.get_encoding("cl100k_base")  # Using a common encoding
        self.model_config = self._get_model_config()
        
    def _get_model_config(self) -> Dict[str, Any]:
        """Get the configuration for the current model."""
        for provider, models in SUPPORTED_MODELS.items():
            for model_id, config in models.items():
                if model_id in self.model_name:
                    return config
        raise ValueError(f"Model {self.model_name} not found in configuration")

    def count_tokens(self, text: str) -> int:
        """Count the number of tokens in a text string."""
        return len(self.encoding.encode(text))

    def count_message_tokens(self, message: Dict[str, str]) -> int:
        """Count tokens in a message dictionary."""
        content = message.get("content", "")
        role = message.get("role", "")
        return self.count_tokens(f"{role}: {content}")

    def count_conversation_tokens(self, messages: List[Dict[str, str]]) -> int:
        """Count total tokens in a conversation."""
        return sum(self.count_message_tokens(msg) for msg in messages)

    def truncate_conversation(self, messages: List[Dict[str, str]], max_tokens: int) -> List[Dict[str, str]]:
        """Truncate conversation to fit within token limit while preserving the most recent messages."""
        total_tokens = self.count_conversation_tokens(messages)
        if total_tokens <= max_tokens:
            return messages

        # Keep system message if present
        system_message = next((msg for msg in messages if msg["role"] == "system"), None)
        
        # Start with system message if it exists
        truncated_messages = [system_message] if system_message else []
        
        # Add messages from the end until we hit the token limit
        current_tokens = self.count_conversation_tokens(truncated_messages)
        for msg in reversed(messages):
            if msg["role"] == "system":
                continue
                
            msg_tokens = self.count_message_tokens(msg)
            if current_tokens + msg_tokens > max_tokens:
                break
                
            truncated_messages.insert(1 if system_message else 0, msg)
            current_tokens += msg_tokens

        return truncated_messages

    def get_available_tokens(self, max_tokens: int = None) -> int:
        """Get the available tokens based on model context length and optional max_tokens parameter."""
        context_length = self.model_config["context_length"]
        if max_tokens is None:
            return context_length
        return min(max_tokens, context_length) 