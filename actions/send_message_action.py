from actions.action import Action
from agents.agent_tracker import AgentTracker


class SendMessageAction(Action):

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
    
    def execute(self, arguments : dict) -> tuple[str, str]:
        if SendMessageAction._sanity_check(arguments):
            print(SendMessageAction._sanity_check(arguments))
            return None, None
        
        agent = AgentTracker.get(arguments[SendMessageAction.RECEIVER])
        if agent is None:
            human_input = input(">")
            return arguments[Action.CALLER_AGENT].get_name(), arguments[Action.CALLER_AGENT].send_message(human_input)
        header = f"{arguments[Action.CALLER_AGENT].get_name()}:\n"
        return arguments[SendMessageAction.RECEIVER], agent.send_message(header + arguments[SendMessageAction.CONTENT])
        