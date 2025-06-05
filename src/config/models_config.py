from typing import Dict, Any

# Supported models configuration
SUPPORTED_MODELS = {
    "groq": {
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
            "groq/llama3-70b-8192": {
                "name": "LLaMA3 70B 8192",
                "provider": "groq",
                "context_length": 8192,
                "is_instruction": True,
                "default_temperature": 0.7,
                "default_max_tokens": 4000,
                "is_production": True
            },
            "groq/llama3-8b-8192": {
                "name": "LLaMA3 8B 8192",
                "provider": "groq",
                "context_length": 8192,
                "is_instruction": True,
                "default_temperature": 0.7,
                "default_max_tokens": 4000,
                "is_production": True
            }
        },
        "huggingface": {
            "groq/distil-whisper-large-v3-en": {
                "name": "Distil Whisper Large V3 EN",
                "provider": "groq",
                "is_production": True
            }
        },
        "mistral_preview": {
            "groq/mistral-saba-24b": {
                "name": "Mistral Saba 24B (Preview)",
                "provider": "groq",
                "context_length": 32000,
                "is_instruction": True,
                "is_preview": True
            }
        },
        "meta_preview": {
            "groq/meta-llama/llama-4-maverick-17b-128e-instruct": {
                "name": "LLaMA 4 Maverick 17B 128E Instruct (Preview)",
                "provider": "groq",
                "context_length": 131072,
                "default_max_tokens": 8192,
                "is_instruction": True,
                "is_preview": True
            },
            "groq/meta-llama/llama-4-scout-17b-16e-instruct": {
                "name": "LLaMA 4 Scout 17B 16E Instruct (Preview)",
                "provider": "groq",
                "context_length": 131072,
                "default_max_tokens": 8192,
                "is_instruction": True,
                "is_preview": True
            },
            "groq/meta-llama/Llama-Guard-4-12B": {
                "name": "LLaMA Guard 4 12B (Preview)",
                "provider": "groq",
                "context_length": 131072,
                "default_max_tokens": 128,
                "is_instruction": True,
                "is_preview": True
            }
        },
        "deepseek_preview": {
            "groq/deepseek-r1-distill-llama-70b": {
                "name": "DeepSeek R1 Distill LLaMA 70B (Preview)",
                "provider": "groq",
                "context_length": 128000,
                "is_instruction": True,
                "is_preview": True
            }
        },
        "playht_preview": {
            "groq/playai-tts": {
                "name": "PlayAI TTS (Preview)",
                "provider": "groq",
                "context_length": 10000,
                "is_preview": True
            },
            "groq/playai-tts-arabic": {
                "name": "PlayAI TTS Arabic (Preview)",
                "provider": "groq",
                "context_length": 10000,
                "is_preview": True
            }
        },
        "alibaba_preview": {
            "groq/qwen-qwq-32b": {
                "name": "Qwen QWQ 32B (Preview)",
                "provider": "groq",
                "context_length": 128000,
                "is_instruction": True,
                "is_preview": True
            }
        }
    },
    "replicate": {
        "replicate": {
            "replicate/deepseek-ai/deepseek-r1": {
                "name": "deepseek-r1",
                "provider": "replicate",
                "context_length": 18192,
                "is_instruction": True,
                "default_temperature": 0.1,
                "default_max_tokens": 8000,
            },
            "replicate/meta/meta-llama-3-8b-instruct": {
                "name": "LLaMA 3 8B Instruct",
                "provider": "replicate",
                "context_length": 8192,
                "is_instruction": True,
                "default_temperature": 0.7,
                "default_max_tokens": 4000,
            },
            "replicate/meta/meta-llama-3-70b-instruct": {
                "name": "LLaMA 3 70B Instruct",
                "provider": "replicate",
                "context_length": 8192,
                "is_instruction": True,
                "default_temperature": 0.7,
                "default_max_tokens": 4000,
            },
            "replicate/meta/meta-llama-3-13b-instruct": {
                "name": "LLaMA 3 13B Instruct",
                "provider": "replicate",
                "context_length": 8192,
                "is_instruction": True,
                "default_temperature": 0.7,
                "default_max_tokens": 4000,
            }
        }
    },
    "gemini": {
        "gemini": {
            "gemini/gemini-2.5-flash-preview-05-20": {
                "name": "Gemini Flash 2.5",
                "provider": "gemini",
                "context_length":128000,
                "is_instruction": True,
                "default_temperature": 0.5,
                "default_max_tokens": 48000,
                "is_production": True
            },
            "gemini/gemini-pro": {
                "name": "Gemini Pro （Need premium API_key）",
                "provider": "gemini",
                "context_length": 128000,
                "is_instruction": True,
                "default_temperature": 0.7,
                "default_max_tokens": 4000,
                "is_production": True
            }
        },
        "system": {
            "pre_message": "",
            "post_message": "\n\n"
        },
        "user": {
            "pre_message": "User: ",
            "post_message": "\n\n"
        },
        "assistant": {
            "pre_message": "Assistant: ",
            "post_message": "\n\n"
        }
    },
    "openrouter": {
        "deepseek": {
            "openrouter/deepseek/deepseek-r1-0528:free": {
                "name": "deepseek-r1-0528",
                "provider": "openrouter",
                "context_length": 164000,
                "is_instruction": True,
                "default_temperature": 0.5,
                "default_max_tokens": 48000,
                "is_production": True
            },
            "openrouter/anthropic/claude-instant-v1": {
                "name": "claude-instant-v1",
                "provider": "openrouter",
                "context_length": 131000,
                "is_instruction": True,
                "default_temperature": 0.5,
                "default_max_tokens": 48000,
                "is_production": True
            }
        },
        "system": {
            "pre_message": "",
            "post_message": "\n\n"
        },
        "user": {
            "pre_message": "User: ",
            "post_message": "\n\n"
        },
        "assistant": {
            "pre_message": "Assistant: ",
            "post_message": "\n\n"
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
    },
    "gemini": {
        "system": {
            "pre_message": "",
            "post_message": "\n\n"
        },
        "user": {
            "pre_message": "User: ",
            "post_message": "\n\n"
        },
        "assistant": {
            "pre_message": "Assistant: ",
            "post_message": "\n\n"
        }
    }
} 
