from llm.llm import LLM


class Agent:

    def __init__(self, *, llm : LLM, system_message : str):
        self.llm = llm
        self.system_message = system_message
        self.chat_history = []

    def send_message(self, message : str) -> None:
        response = self._proccess_input(message)
        print("Agent: " + response)

    def _proccess_input(self, message : str) -> str:
        response = self.llm.query(self.system_message, message, self.chat_history)
        self.chat_history += LLM.package_history(message, response)
        return response

