import os

from dotenv import load_dotenv


load_dotenv()


class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

    LLM_MODEL = "gpt-4o-mini"

    if not OPENAI_API_KEY:
        raise ValueError(
            "OPENAI_API_KEY mancante. Controlla il file .env"
        )

    if not TAVILY_API_KEY:
        raise ValueError(
            "TAVILY_API_KEY mancante. Controlla il file .env"
        )