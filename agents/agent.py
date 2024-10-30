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
    
    def get_system_message(self) -> str:
        return self.system_message

    def send_message(self, message : str) -> str:
        response = self.llm.query(self.system_message, message, self.chat_history)
        self.chat_history += LLM.package_history(message, response)
        return response
    
    def choose_action(self, response : str) -> tuple[Action, dict]:
        arguments = Parse.action(response)
        if arguments[Action.NAME] in self.actions:
            selected_action = self.actions[arguments[Action.NAME]]
            del arguments[Action.NAME]
            arguments[Action.CALLER_AGENT] = self
            return selected_action, arguments
        else:
            print("Failed do find action")
            return None, None

