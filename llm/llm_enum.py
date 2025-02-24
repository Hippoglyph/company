from enum import Enum
from llm.llm import LLM
from llm.models.gemini_llm import GeminiLLM
from llm.models.groq_llm import GroqLLM


class LLMEnum(Enum):

    LLaMa3_8b = GroqLLM("llama3-8b-8192", 7000)
    LLaMa3_2_90b = GroqLLM("llama-3.2-90b-text-preview", 7000)
    Gemini_2_Flash = GeminiLLM("gemini-2.0-flash", 1000000)


    def default_llm() -> LLM:
        return LLMEnum.Gemini_2_Flash.value