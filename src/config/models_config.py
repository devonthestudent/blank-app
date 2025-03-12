from typing import Dict, Any

# Supported models configuration
SUPPORTED_MODELS = {
    "google": {
        "groq/gemma2-9b-it": {
            "name": "Gemma 2 9B IT",
            "provider": "groq",
            "context_length": 8192,
            "is_instruction": True,
            "default_temperature": 0.7,
            "default_max_tokens": 4096,
        }
    },
    "meta": {
        "groq/llama-3.3-70b-versatile": {
            "name": "LLaMA 3.3 70B Versatile",
            "provider": "groq",
            "context_length": 128000,
            "is_instruction": True,
            "default_temperature": 0.7,
            "default_max_tokens": 32768,
        },
        "groq/llama-3.1-8b-instant": {
            "name": "LLaMA 3.1 8B Instant",
            "provider": "groq",
            "context_length": 128000,
            "is_instruction": True,
            "default_temperature": 0.7,
            "default_max_tokens": 8192,
        },
        "groq/llama-guard-3-8b": {
            "name": "LLaMA Guard 3 8B",
            "provider": "groq",
            "context_length": 8192,
            "is_instruction": True,
            "default_temperature": 0.7,
            "default_max_tokens": 4096,
        },
        "groq/llama3-70b-8192": {
            "name": "LLaMA 3 70B",
            "provider": "groq",
            "context_length": 8192,
            "is_instruction": True,
            "default_temperature": 0.7,
            "default_max_tokens": 4096,
        },
        "groq/llama3-8b-8192": {
            "name": "LLaMA 3 8B",
            "provider": "groq",
            "context_length": 8192,
            "is_instruction": True,
            "default_temperature": 0.7,
            "default_max_tokens": 4096,
        }
    },
    "mistral": {
        "groq/mixtral-8x7b-32768": {
            "name": "Mixtral 8x7B",
            "provider": "groq",
            "context_length": 32768,
            "is_instruction": True,
            "default_temperature": 0.7,
            "default_max_tokens": 16384,
        }
    },
    "alibaba": {
        "groq/qwen-qwq-32b": {
            "name": "Qwen QWQ 32B",
            "provider": "groq",
            "context_length": 128000,
            "is_instruction": True,
            "default_temperature": 0.7,
            "default_max_tokens": 2048,
        },
        "groq/qwen-2.5-coder-32b": {
            "name": "Qwen 2.5 Coder 32B",
            "provider": "groq",
            "context_length": 128000,
            "is_instruction": True,
            "default_temperature": 0.7,
            "default_max_tokens": 2048,
        },
        "groq/qwen-2.5-32b": {
            "name": "Qwen 2.5 32B",
            "provider": "groq",
            "context_length": 128000,
            "is_instruction": True,
            "default_temperature": 0.7,
            "default_max_tokens": 2048,
        }
    },
    "deepseek": {
        "groq/deepseek-r1-distill-qwen-32b": {
            "name": "DeepSeek R1 Distill Qwen 32B",
            "provider": "groq",
            "context_length": 128000,
            "is_instruction": True,
            "default_temperature": 0.7,
            "default_max_tokens": 16384,
        },
        "groq/deepseek-r1-distill-llama-70b-specdec": {
            "name": "DeepSeek R1 Distill LLaMA 70B SpecDec",
            "provider": "groq",
            "context_length": 128000,
            "is_instruction": True,
            "default_temperature": 0.7,
            "default_max_tokens": 16384,
        },
        "groq/deepseek-r1-distill-llama-70b": {
            "name": "DeepSeek R1 Distill LLaMA 70B",
            "provider": "groq",
            "context_length": 128000,
            "is_instruction": True,
            "default_temperature": 0.7,
            "default_max_tokens": 2048,
        }
    },
    "replicate": {
        "deepseek-ai/deepseek-r1": {
            "name": "DeepSeek R1",
            "provider": "replicate",
            "context_length": 128000,
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