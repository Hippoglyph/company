from llm.llm import LLM
from groq import Groq
from openai.resources.chat import Chat

class GroqLLM(LLM):
    
    def __init__(self, model_id : str):
        self.client = Groq()
        self.model_id = model_id

    def _get_model_id(self) -> str:
        return self.model_id

    def _get_chat(self) -> Chat:
        return self.client.chat