# Project Overview

Use this guide to build a streamlit application (deploys using streamlit_app.py in the BLANK_APP folder) that allows user to interact with chat models in python.

# Feature requirements

## Model Access and Selection
The chatbot will integrate multiple AI models from Replicate (for premium access to advanced models) and Groq (for free model access).
LiteLLM will be used as an abstraction layer to streamline API calls and enhance model management.
Users can easily switch between models via the UI.
Initially, the chatbot will support three models from Groq and Replicate as a starting point, with the potential for future expansion.

### User Interface (UI)
The chatbot will have a modern, intuitive UI designed for seamless interaction.
A clean, responsive layout that works across devices (desktop, tablet, mobile).
Theming support, including light and dark modes.
Accessibility features, such as keyboard navigation and screen reader compatibility.
A clear distinction between chat messages from the user and the assistant for readability.
A loading indicator when responses are being generated.
Configurable settings panel where users can adjust preferences (e.g., model selection, token limits).

### Chat History and Memory Management
The chatbot will store user-assistant interactions to provide continuity in conversations.
A tokenizer will track token usage in the chat to monitor API limits and prevent excessive memory consumption.
Users will have access to a slider to set the maximum chat memory retained, allowing them to balance memory usage and performance.
Automatic memory pruning will remove older messages when the token limit is exceeded.


###  Conversation Handling
The chat interface will differentiate between:
Instruction-based models (e.g., chat-based AI assistants)
Non-instruction models (e.g., completion-based models for text generation)
The chatbot will automatically apply different templates when interacting with each model type to optimize the prompts for better responses.
A system message area where predefined or user-customized system prompts can be used.

### Model Management
The system will start with three models from Groq and Replicate, but the architecture will allow scalability to integrate more models in the future.
A backend structure that allows easy swapping and adding of AI models without major modifications.

### Additional Features (Future Enhancements)

Export chat history to save past interactions as text or JSON files.
Customizable system prompts to tailor model behavior.
Multilingual support to interact in different languages.



# Relevant docs

## Sample usage of Groq on litellm

### Sample Usage - Streaming
from litellm import completion
import os

os.environ['GROQ_API_KEY'] = ""
response = completion(
    model="groq/llama3-8b-8192", 
    messages=[
       {"role": "user", "content": "hello from litellm"}
   ],
    stream=True
)

for chunk in response:
    print(chunk)

## Sample usage of Groq on litellm

### Sample Usage - Streaming
from litellm import completion
import os

os.environ['GROQ_API_KEY'] = ""
response = completion(
    model="groq/llama3-8b-8192", 
    messages=[
       {"role": "user", "content": "hello from litellm"}
   ],
    stream=True
)

for chunk in response:
    print(chunk)

## Replicate on LiteLLM
LiteLLM supports all models on Replicate

API KEYS
import os 
os.environ["REPLICATE_API_KEY"] = ""

Example Call
from litellm import completion
import os
### set ENV variables
os.environ["REPLICATE_API_KEY"] = "replicate key"

### replicate llama-3 call
response = completion(
    model="replicate/meta/meta-llama-3-8b-instruct", 
    messages = [{ "content": "Hello, how are you?","role": "user"}]
)

Advanced Usage - Prompt Formatting
LiteLLM has prompt template mappings for all meta-llama llama3 instruct models. See Code

To apply a custom prompt template:

SDK
PROXY
import litellm

import os 
os.environ["REPLICATE_API_KEY"] = ""

### Create your own custom prompt template 
litellm.register_prompt_template(
        model="togethercomputer/LLaMA-2-7B-32K",
        initial_prompt_value="You are a good assistant" # [OPTIONAL]
        roles={
            "system": {
                "pre_message": "[INST] <<SYS>>\n", # [OPTIONAL]
                "post_message": "\n<</SYS>>\n [/INST]\n" # [OPTIONAL]
            },
            "user": { 
                "pre_message": "[INST] ", # [OPTIONAL]
                "post_message": " [/INST]" # [OPTIONAL]
            }, 
            "assistant": {
                "pre_message": "\n" # [OPTIONAL]
                "post_message": "\n" # [OPTIONAL]
            }
        }
        final_prompt_value="Now answer as best you can:" # [OPTIONAL]
)

def test_replicate_custom_model():
    model = "replicate/togethercomputer/LLaMA-2-7B-32K"
    response = completion(model=model, messages=messages)
    print(response['choices'][0]['message']['content'])
    return response

test_replicate_custom_model()

Advanced Usage - Calling Replicate Deployments
Calling a deployed replicate LLM Add the replicate/deployments/ prefix to your model, so litellm will call the deployments endpoint. This will call ishaan-jaff/ishaan-mistral deployment on replicate

response = completion(
    model="replicate/deployments/ishaan-jaff/ishaan-mistral", 
    messages= [{ "content": "Hello, how are you?","role": "user"}]
)


# Current File Structure

📦 BLANK-APP
 ┣ 📂 .devcontainer
 ┣ 📂 .github
 ┣ 📂 requirements
 ┃ ┣ 📄 frontend_instructions.md
 ┃ ┗ 📄 other_requirements.md
 ┣ 📂 src
 ┃ ┣ 📂 components
 ┃ ┃ ┣ 📄 chat.py
 ┃ ┃ ┣ 📄 memory.py
 ┃ ┃ ┗ 📄 model_selector.py
 ┃ ┣ 📂 utils
 ┃ ┃ ┣ 📄 tokenizer.py
 ┃ ┃ ┣ 📄 templates.py
 ┃ ┃ ┗ 📄 api_handlers.py
 ┃ ┗ 📂 config
 ┃   ┗ 📄 models_config.py
 ┣ 📄 .gitignore
 ┣ 📄 LICENSE
 ┣ 📄 README.md
 ┣ 📄 requirements.txt
 ┗ 📄 streamlit_app.py