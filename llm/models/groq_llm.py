import groq
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
    
    @staticmethod
    def is_retry_exception(exception : Exception) -> bool:
        if isinstance(exception, groq.APIStatusError):
            return (exception.status_code == 413 and 
                    exception.body.get('error', {}).get('code') == 'rate_limit_exceeded')
        return False