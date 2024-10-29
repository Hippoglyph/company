from openai.resources.chat import Chat

class LLM:

    ROLE = "role"
    CONTENT = "content"
    ROLE_USER = "user"
    ROLE_ASSISTANT = "assistant"
    ROLE_SYSTEM = "system"

    def query(self, system_message : str, message : str, chat_history : list [dict] = []) -> str:
        chat_completion = self._get_chat().completions.create(
            messages=[
                {
                    "role": "user",
                    "content": message,
                }
            ],
            model=self._get_model_id(),
        )
        return chat_completion.choices[0].message.content
    
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
                LLM.ROLE : LLM.ROLE_SYSTEM,
                LLM.CONTENT : message
            }
        ]
    
    def _get_model_id(self) -> str:
        pass

    def _get_chat(self) -> Chat:
        pass