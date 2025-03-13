from typing import Dict, Any

# Supported models configuration
SUPPORTED_MODELS = {
    # =====================
    # PRODUCTION MODELS
    # =====================
    # Models intended for use in production environments
    # Meeting high standards for speed and quality
    
    "google": {
        "groq/gemma2-9b-it": {
            "name": "Gemma 2 9B IT",
            "provider": "groq",
            "context_length": 8192,
            "is_instruction": True,
            "default_temperature": 0.7,
            "default_max_tokens": 4000,
            "is_production": True
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
            "is_production": True
        },
        "groq/llama-3.1-8b-instant": {
            "name": "LLaMA 3.1 8B Instant",
            "provider": "groq",
            "context_length": 128000,
            "is_instruction": True,
            "default_temperature": 0.7,
            "default_max_tokens": 8192,
            "is_production": True
        },
        "groq/llama-guard-3-8b": {
            "name": "LLaMA Guard 3 8B",
            "provider": "groq",
            "context_length": 8192,
            "is_instruction": True,
            "default_temperature": 0.7,
            "default_max_tokens": 4000,
            "is_production": True
        },
        "groq/llama3-70b-8192": {
            "name": "LLaMA 3 70B",
            "provider": "groq",
            "context_length": 8192,
            "is_instruction": True,
            "default_temperature": 0.7,
            "default_max_tokens": 4000,
            "is_production": True
        },
        "groq/llama3-8b-8192": {
            "name": "LLaMA 3 8B",
            "provider": "groq",
            "context_length": 8192,
            "is_instruction": True,
            "default_temperature": 0.7,
            "default_max_tokens": 4000,
            "is_production": True
        }
    },
    "mistral": {
        "groq/mixtral-8x7b-32768": {
            "name": "Mixtral 8x7B",
            "provider": "groq",
            "context_length": 32768,
            "is_instruction": True,
            "default_temperature": 0.7,
            "default_max_tokens": 16000,
            "is_production": True
        }
    },
    "huggingface": {
        "groq/distil-whisper-large-v3-en": {
            "name": "Distil Whisper Large V3 (English)",
            "provider": "groq",
            "is_audio": True,
            "max_file_size_mb": 25,
            "is_production": True
        }
    },
    "openai": {
        "groq/whisper-large-v3": {
            "name": "Whisper Large V3",
            "provider": "groq",
            "is_audio": True,
            "max_file_size_mb": 25,
            "is_production": True
        },
        "groq/whisper-large-v3-turbo": {
            "name": "Whisper Large V3 Turbo",
            "provider": "groq",
            "is_audio": True,
            "max_file_size_mb": 25,
            "is_production": True
        }
    },

    # =====================
    # PREVIEW MODELS
    # =====================
    # Models intended for evaluation purposes only
    # May be discontinued at short notice
    # Not recommended for production use
    
    "alibaba_preview": {
        "groq/qwen-qwq-32b": {
            "name": "Qwen QWQ 32B (Preview)",
            "provider": "groq",
            "context_length": 128000,
            "is_instruction": True,
            "default_temperature": 0.7,
            "default_max_tokens": 32000,
            "is_preview": True
        },
        "groq/qwen-2.5-coder-32b": {
            "name": "Qwen 2.5 Coder 32B (Preview)",
            "provider": "groq",
            "context_length": 128000,
            "is_instruction": True,
            "default_temperature": 0.7,
            "default_max_tokens": 32000,
            "is_preview": True
        },
        "groq/qwen-2.5-32b": {
            "name": "Qwen 2.5 32B (Preview)",
            "provider": "groq",
            "context_length": 128000,
            "is_instruction": True,
            "default_temperature": 0.7,
            "default_max_tokens": 32000,
            "is_preview": True
        }
    },
    "mistral_preview": {
        "groq/mistral-saba-24b": {
            "name": "Mistral Saba 24B (Preview)",
            "provider": "groq",
            "context_length": 32000,
            "is_instruction": True,
            "default_temperature": 0.7,
            "default_max_tokens": 16000,
            "is_preview": True
        }
    },
    "meta_preview": {
        "groq/llama-3.3-70b-specdec": {
            "name": "LLaMA 3.3 70B SpecDec (Preview)",
            "provider": "groq",
            "context_length": 8192,
            "is_instruction": True,
            "default_temperature": 0.7,
            "default_max_tokens": 4000,
            "is_preview": True
        },
        "groq/llama-3.2-1b-preview": {
            "name": "LLaMA 3.2 1B (Preview)",
            "provider": "groq",
            "context_length": 128000,
            "is_instruction": True,
            "default_temperature": 0.7,
            "default_max_tokens": 8192,
            "is_preview": True
        },
        "groq/llama-3.2-3b-preview": {
            "name": "LLaMA 3.2 3B (Preview)",
            "provider": "groq",
            "context_length": 128000,
            "is_instruction": True,
            "default_temperature": 0.7,
            "default_max_tokens": 8192,
            "is_preview": True
        },
        "groq/llama-3.2-11b-vision-preview": {
            "name": "LLaMA 3.2 11B Vision (Preview)",
            "provider": "groq",
            "context_length": 128000,
            "is_instruction": True,
            "default_temperature": 0.7,
            "default_max_tokens": 8192,
            "is_preview": True
        },
        "groq/llama-3.2-90b-vision-preview": {
            "name": "LLaMA 3.2 90B Vision (Preview)",
            "provider": "groq",
            "context_length": 128000,
            "is_instruction": True,
            "default_temperature": 0.7,
            "default_max_tokens": 8192,
            "is_preview": True
        }
    },
    "deepseek_preview": {
        "groq/deepseek-r1-distill-qwen-32b": {
            "name": "DeepSeek R1 Distill Qwen 32B (Preview)",
            "provider": "groq",
            "context_length": 128000,
            "is_instruction": True,
            "default_temperature": 0.7,
            "default_max_tokens": 16384,
            "is_preview": True
        },
        "groq/deepseek-r1-distill-llama-70b-specdec": {
            "name": "DeepSeek R1 Distill LLaMA 70B SpecDec (Preview)",
            "provider": "groq",
            "context_length": 128000,
            "is_instruction": True,
            "default_temperature": 0.7,
            "default_max_tokens": 16384,
            "is_preview": True
        },
        "groq/deepseek-r1-distill-llama-70b": {
            "name": "DeepSeek R1 Distill LLaMA 70B (Preview)",
            "provider": "groq",
            "context_length": 128000,
            "is_instruction": True,
            "default_temperature": 0.7,
            "default_max_tokens": 32000,
            "is_preview": True
        }
    },
    "replicate": {
        "deepseek-ai/deepseek-r1": {
            "name": "DeepSeek R1",
            "provider": "replicate",
            "context_length": 128000,
            "is_instruction": True,
            "default_temperature": 0.7,
            "default_max_tokens": 2000,
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