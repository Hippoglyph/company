from actions.action import Action
from agents.utils.parse import Parse
from llm.llm import LLM


class Agent:

    def __init__(self, *, name : str, llm : LLM, system_message : str, actions : list[Action]):
        self.name = name
        self.llm = llm
        self.system_message = system_message
        self.actions = {action.get_name() : action for action in actions}
        self.chat_history = []

    def get_name(self) -> str:
        return self.name

    def send_message(self, message : str) -> None:
        response = self._proccess_input(message)
        print(f"{self.name}: {response}")
        self.take_action(response)

    def _proccess_input(self, message : str) -> str:
        response = self.llm.query(self.system_message, message, self.chat_history)
        self.chat_history += LLM.package_history(message, response)
        return response
    
    def take_action(self, response : str) -> None:
        action_data = Parse.action(response)
        if action_data[Action.NAME] in self.actions:
            print(">Intends to " + action_data[Action.NAME])

