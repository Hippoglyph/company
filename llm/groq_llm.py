from llm.llm import LLM
from groq import Groq

class GroqLLM(LLM):
    
    def __init__(self, model_id : str):
        self.client = Groq()
        self.model_id = model_id

    def query(self, system_message : str, message : str, chat_history : list [dict] = []) -> str:
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": "Explain the importance of low latency LLMs",
                }
            ],
            model="llama3-8b-8192",
        )
        return chat_completion.choices[0].message.content