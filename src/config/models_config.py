from typing import Dict, Any

# Supported models configuration
SUPPORTED_MODELS = {
    "groq": {
        "llama3-8b-8192": {
            "name": "Llama 3 8B",
            "provider": "groq",
            "context_length": 8192,
            "is_instruction": True,
            "default_temperature": 0.7,
            "default_max_tokens": 2048,
        },
        "mixtral-8x7b-32768": {
            "name": "Mixtral 8x7B",
            "provider": "groq",
            "context_length": 32768,
            "is_instruction": True,
            "default_temperature": 0.7,
            "default_max_tokens": 2048,
        },
        "llama2-70b-4096": {
            "name": "Llama 2 70B",
            "provider": "groq",
            "context_length": 4096,
            "is_instruction": True,
            "default_temperature": 0.7,
            "default_max_tokens": 2048,
        }
    },
    "replicate": {
        "meta/meta-llama-3-8b-instruct": {
            "name": "Llama 3 8B Instruct",
            "provider": "replicate",
            "context_length": 4096,
            "is_instruction": True,
            "default_temperature": 0.7,
            "default_max_tokens": 2048,
        },
        "meta/meta-llama-3-70b-instruct": {
            "name": "Llama 3 70B Instruct",
            "provider": "replicate",
            "context_length": 4096,
            "is_instruction": True,
            "default_temperature": 0.7,
            "default_max_tokens": 2048,
        },
        "mistralai/mistral-7b-instruct": {
            "name": "Mistral 7B Instruct",
            "provider": "replicate",
            "context_length": 4096,
            "is_instruction": True,
            "default_temperature": 0.7,
            "default_max_tokens": 2048,
        }
    }
}

# Default system prompts for different model types
SYSTEM_PROMPTS = {
    "instruction": """You are a helpful AI assistant. You aim to provide accurate, helpful, and safe responses.
    Always be direct and concise in your answers. If you're not sure about something, say so.""",
    "completion": """You are a helpful AI assistant that completes text in a natural and coherent way.
    Your completions should be contextually appropriate and maintain the style of the input text."""
}

# Model-specific prompt templates
PROMPT_TEMPLATES = {
    "groq": {
        "system": {
            "pre_message": "",
            "post_message": "\n\n"
        },
        "user": {
            "pre_message": "Human: ",
            "post_message": "\n\n"
        },
        "assistant": {
            "pre_message": "Assistant: ",
            "post_message": "\n\n"
        }
    },
    "replicate": {
        "system": {
            "pre_message": "<s>[INST] <<SYS>>\n",
            "post_message": "\n<</SYS>>\n[/INST]</s>\n"
        },
        "user": {
            "pre_message": "<s>[INST] ",
            "post_message": " [/INST]</s>\n"
        },
        "assistant": {
            "pre_message": "",
            "post_message": "\n"
        }
    }
} 