from actions.action import Action
from actions.send_message_action import SendMessageAction
from agents.utils.parse import Parse
from llm.llm import LLM
from prompts_utils.prompt_handler import PromptHandler

class Agent:

    def __init__(self, *, name : str, llm : LLM, system_message : str, actions : list[Action],
                 human : bool = False):
        self.name = name
        self.llm = llm
        self.system_message = system_message
        self.actions = {action.get_name() : action for action in actions}
        self.chat_history = []
        self.human = human

    def get_name(self) -> str:
        return self.name
    
    def get_system_message(self) -> str:
        return self.system_message

    def send_message(self, message : str) -> str:
        if self.is_human():
            response = self._get_human_response(message)
        else:
            response = self.llm.query(self.system_message, message, self.chat_history)
        self._handle_history(message, response)
        return response
    
    def _handle_history(self, message : str, response : str) -> None:
        self.chat_history += LLM.package_history(message, response)
        while self.llm.get_tokens_count(self.chat_history) > self.llm.get_token_limit() - self.llm.get_token_count(LLM.ROLE_SYSTEM, self.system_message):
            self.chat_history = self.chat_history[:-2] # Remove one interaction at the time
    
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
        
    def is_human(self) -> bool:
        return self.human
    
    def _get_human_response(self, message : str) -> str:
        print(message)
        light_response = input(">")
        for action_name, action  in self.actions.items():
            if isinstance(action, SendMessageAction):
                arguments = {
                    SendMessageAction.RECEIVER : action.get_relations_names()[0], # assume
                    SendMessageAction.CONTENT : light_response
                }
                return PromptHandler.get_action(action_name = action_name, **arguments)
        raise RuntimeError("Human has no SendMessageAction")
    
    def get_actions(self) -> list[Action]:
        return self.actions.values()
    
        

