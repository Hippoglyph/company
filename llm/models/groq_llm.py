from llm.llm import LLM
from groq import Groq
from openai.resources.chat import Chat
import tiktoken

class GroqLLM(LLM):

    TOKENIZER = tiktoken.get_encoding("cl100k_base")
    
    def __init__(self, model_id : str, token_limit : int):
        self.client = Groq()
        self.model_id = model_id
        self.token_limit = token_limit

    def _get_model_id(self) -> str:
        return self.model_id

    def _get_chat(self) -> Chat:
        return self.client.chat
    
    def is_retry_exception(self, exception : Exception) -> bool:
        # TODO
        #if isinstance(exception, groq.RateLimitError):
            # return (exception.status_code == 413 and 
            #         exception.body.get('error', {}).get('code') == 'rate_limit_exceeded')

        return False
    
    def get_token_limit(self) -> int:
        return self.token_limit
    
    def get_token_count(self, role : str, content : str) -> int:
        return len(GroqLLM.TOKENIZER.encode(f"{role}: {content}"))