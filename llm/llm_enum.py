from enum import Enum
from llm.llm import LLM
from llm.models.groq_llm import GroqLLM


class LLMEnum(Enum):

    LLaMa3_8b = GroqLLM("llama3-8b-8192")
    LLaMa3_2_90b = GroqLLM("llama-3.2-90b-text-preview")

    def default_llm() -> LLM:
        return LLMEnum.LLaMa3_2_90b.value