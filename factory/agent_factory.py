from actions.send_message_action import SendMessageAction
from agents.agent import Agent
from agents.agent_names import AgentNames
from factory.agent_construct import AgentConstruct


class AgentFactory:

    @staticmethod
    def create_agents() -> list[AgentConstruct]:
        agents = []

        agents += [
            AgentConstruct(AgentNames.CODER)
                .with_action(SendMessageAction([AgentNames.ARCHITECT]))
        ]
        return agents
    
    @staticmethod
    def build() -> list[Agent]:
        return [agent.build() for agent in AgentFactory.create_agents()]


