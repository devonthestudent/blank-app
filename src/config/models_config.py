from typing import Dict, Any

# Supported models configuration
SUPPORTED_MODELS = {
    "alibaba": {
        "groq/qwen-qwq-32b": {
            "name": "Qwen QWQ 32B",
            "provider": "groq",
            "context_length": 128000,
            "is_instruction": True,
            "default_temperature": 0.7,
            "default_max_tokens": 2048,
        },
      #   "groq/qwen-2.5-coder-32b": {
      #       "name": "Qwen 2.5 Coder 32B",
      #       "provider": "groq",
      #       "context_length": 128000,
      #       "is_instruction": True,
      #       "default_temperature": 0.7,
      #       "default_max_tokens": 2048,
      #   },
      #   "groq/qwen-2.5-32b": {
      #       "name": "Qwen 2.5 32B",
      #       "provider": "groq",
      #       "context_length": 128000,
      #       "is_instruction": True,
      #       "default_temperature": 0.7,
      #       "default_max_tokens": 2048,
      #   }
    },
    "mistral": {
        "groq/mistral-saba-24b": {
            "name": "Mistral Saba 24B",
            "provider": "groq",
            "context_length": 32000,
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
      #   "groq/deepseek-r1-distill-llama-70b-specdec": {
      #       "name": "DeepSeek R1 Distill LLaMA 70B SpecDec",
      #       "provider": "groq",
      #       "context_length": 128000,
      #       "is_instruction": True,
      #       "default_temperature": 0.7,
      #       "default_max_tokens": 16384,
      #   },
        "groq/deepseek-r1-distill-llama-70b": {
            "name": "DeepSeek R1 Distill LLaMA 70B",
            "provider": "groq",
            "context_length": 128000,
            "is_instruction": True,
            "default_temperature": 0.7,
            "default_max_tokens": 2048,
        }
    },
    "meta": {
        "groq/llama-3.3-70b-specdec": {
            "name": "LLaMA 3.3 70B SpecDec",
            "provider": "groq",
            "context_length": 8192,
            "is_instruction": True,
            "default_temperature": 0.7,
            "default_max_tokens": 2048,
        },
#         "groq/llama-3.2-1b-preview": {
#             "name": "LLaMA 3.2 1B Preview",
#             "provider": "groq",
#             "context_length": 128000,
#             "is_instruction": True,
#             "default_temperature": 0.7,
#             "default_max_tokens": 8192,
#         },
#         "groq/llama-3.2-3b-preview": {
#             "name": "LLaMA 3.2 3B Preview",
#             "provider": "groq",
#             "context_length": 128000,
#             "is_instruction": True,
#             "default_temperature": 0.7,
#             "default_max_tokens": 8192,
#         },
#         "groq/llama-3.2-11b-vision-preview": {
#             "name": "LLaMA 3.2 11B Vision Preview",
#             "provider": "groq",
#             "context_length": 128000,
#             "is_instruction": True,
#             "default_temperature": 0.7,
#             "default_max_tokens": 8192,
#         },
#         "groq/llama-3.2-90b-vision-preview": {
#             "name": "LLaMA 3.2 90B Vision Preview",
#             "provider": "groq",
#             "context_length": 128000,
#             "is_instruction": True,
#             "default_temperature": 0.7,
#             "default_max_tokens": 8192,
#         }
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