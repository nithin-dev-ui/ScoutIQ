import os

from dotenv import load_dotenv
from google import genai


load_dotenv()


class LLMService:
    """
    Gemini-powered LLM service for ScoutIQ.

    Uses Google's current Interactions API.
    The API key is read from the GEMINI_API_KEY
    environment variable and is never printed.
    """

    PLACEHOLDER_KEYS = {
        "",
        "YOUR_KEY_HERE",
        "PASTE_YOUR_GEMINI_API_KEY_HERE",
        "YOUR_GEMINI_API_KEY"
    }

    MODEL = "gemini-3.7-flash"

    def __init__(self):
        self.provider = os.getenv(
            "LLM_PROVIDER",
            "gemini"
        ).lower()

        self.api_key = os.getenv(
            "GEMINI_API_KEY",
            ""
        ).strip()

        self.client = None

        if (
            self.provider == "gemini"
            and self.api_key
            and self.api_key not in self.PLACEHOLDER_KEYS
        ):
            self.client = genai.Client(
                api_key=self.api_key
            )

    def is_available(self):
        return (
            self.provider == "gemini"
            and self.client is not None
        )

    def generate(self, prompt):
        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty")

        if not self.is_available():
            raise RuntimeError(
                "Gemini is not configured. "
                "Add GEMINI_API_KEY to .env."
            )

        interaction = self.client.interactions.create(
            model=self.MODEL,
            input=prompt
        )

        return interaction.output_text