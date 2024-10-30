from actions.action import Action
from agents.agent import Agent


class SendMessageAction(Action):

    message_map = {}

    RECEIVER = "receiver"
    CONTENT = "content"

    def __init__(self, relations_names : list[str]):
        self.relations_names = relations_names

    def get_name(self) -> str:
        return "SendMessage"

    def get_description(self) -> str:
        return "Sends a message to an agent"

    def get_arguments(self) -> dict:
        return {SendMessageAction.RECEIVER : f"The name of the agent that you wish to send a message to. Agent names: {", ".join(self.relations_names)}",
            SendMessageAction.CONTENT : "The message content"
        }
    
    def _sanity_check(arguments : dict) -> str:
        if SendMessageAction.RECEIVER not in arguments:
            return "Could not find a receiver"
        if SendMessageAction.CONTENT not in arguments:
            return "Message contained no content"
        # expand
        return None
    
    def execute(self, arguments : dict) -> None:
        if SendMessageAction._sanity_check(arguments):
            print(SendMessageAction._sanity_check(arguments))
            return
        
        callback = SendMessageAction.message_map.get(arguments[SendMessageAction.RECEIVER])
        if callback is None:
            response = input(f"{arguments[SendMessageAction.RECEIVER]}>")
            arguments[Action.CALLER_AGENT].send_message(response)
        else:
            callback(arguments[SendMessageAction.CONTENT])

    
    @staticmethod
    def init(agents : list[Agent]) -> None:
        for agent in agents:
            SendMessageAction.message_map[agent.get_name()] = agent.send_message

        