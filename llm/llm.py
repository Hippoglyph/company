import random
import time
from openai.resources.chat import Chat

class LLM:

    ROLE = "role"
    CONTENT = "content"
    ROLE_USER = "user"
    ROLE_ASSISTANT = "assistant"
    ROLE_SYSTEM = "system"

    def query(self, system_message : str, message : str, chat_history : list [dict] = []) -> str:
        messages = LLM._package_messages(system_message, message, chat_history)
        max_retries = 5
        for attempt in range(max_retries):
            try:
                chat_completion = self._get_chat().completions.create(
                    messages=messages,
                    model=self._get_model_id(),
                    temperature=0,
                    top_p=0.95
                )
                break
            except Exception as e:
                if LLM.is_retry_exception(e):
                    print(f"Rate limit exceeded. Retrying in a moment (attempt {attempt + 1}/{max_retries})")
                    LLM.exponential_backoff(attempt)
                else:
                    raise e
        return chat_completion.choices[0].message.content
    
    def exponential_backoff(attempt, max_delay=60):
        delay = min(2 ** attempt + random.random(), max_delay)
        time.sleep(delay)

    
    @staticmethod
    def _package_messages(system_message : str, message : str, chat_history : list [dict]) -> list[dict]:
        messages = [
            {
                LLM.ROLE : LLM.ROLE_SYSTEM,
                LLM.CONTENT : system_message
            }
        ]
        messages += chat_history
        messages += [
            {
                LLM.ROLE : LLM.ROLE_USER,
                LLM.CONTENT : message
            }
        ]
        return messages
    
    def package_history(message : str, response : str) -> list[dict]:
        return [
            {
                LLM.ROLE : LLM.ROLE_USER,
                LLM.CONTENT : message
            },
            {
                LLM.ROLE : LLM.ROLE_ASSISTANT,
                LLM.CONTENT : response
            }
        ]
    
    def _get_model_id(self) -> str:
        pass

    def _get_chat(self) -> Chat:
        pass
    
    @staticmethod
    def is_retry_exception(exception : Exception) -> bool:
        return False