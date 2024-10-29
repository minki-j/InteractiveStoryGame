import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

load_dotenv(".env", override=True)
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL")
FALLBACK_MODEL = os.getenv("FALLBACK_MODEL")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", 0.7))
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def get_chat_model(temp: float = LLM_TEMPERATURE, size: str = "small"):

    if "claude" in DEFAULT_MODEL:
        main_model = ChatAnthropic(
            model=DEFAULT_MODEL if size == "large" else "claude-3-haiku-20240307",
            api_key=ANTHROPIC_API_KEY,
            temperature=temp,
        )
        fallback_model = ChatOpenAI(
            model=FALLBACK_MODEL,
            api_key=OPENAI_API_KEY,
            temperature=temp,
        )
    elif "gpt" in DEFAULT_MODEL:
        main_model = ChatOpenAI(
            model=DEFAULT_MODEL if size == "large" else "gpt-4o-mini",
            api_key=OPENAI_API_KEY,
            temperature=temp,
        )
        fallback_model = ChatAnthropic(
            model=FALLBACK_MODEL,
            api_key=ANTHROPIC_API_KEY,
            temperature=temp,
        )
    else:
        raise ValueError("Invalid model name")

    return main_model.with_fallbacks([fallback_model])
