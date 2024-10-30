from actions.action import Action
from agents.agent import Agent


class SendMessageAction(Action):

    message_map = {}

    def __init__(self, relations_names : list[str]):
        self.relations_names = relations_names

    def get_name(self) -> str:
        return "SendMessage"

    def get_description(self) -> str:
        return "Sends a message to an agent"

    def get_arguments(self) -> dict:
        return {"receiver" : f"The name of the agent that you wish to send a message to. Agent names: {", ".join(self.relations_names)}",
            "content" : "The message content"
        }
    
    @staticmethod
    def init(agents : list[Agent]) -> None:
        for agent in agents:
            SendMessageAction.message_map[agent.get_name()] = agent.send_message

        