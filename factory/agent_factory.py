
from actions.send_message_action import SendMessageAction
from agents.agent import Agent
from agents.agent_names import AgentNames
from agents.agent_tracker import AgentTracker
from factory.agent_construct import AgentConstruct


class AgentFactory:

    @staticmethod
    def create_agents() -> list[AgentConstruct]:
        agents = []

        agents += [
            AgentConstruct(AgentNames.CODER)
                .with_action(SendMessageAction([AgentNames.ARCHITECT, AgentNames.CODE_REVIEWER]))
            ,
            AgentConstruct(AgentNames.CODE_REVIEWER)
                .with_action(SendMessageAction([AgentNames.CODER]))
        ]
        return agents
    
    def initilize_actions(agents : list[Agent]) -> None:
        AgentTracker.init(agents)
    
    @staticmethod
    def build() -> list[Agent]:
        agents = [agent.build() for agent in AgentFactory.create_agents()]
        AgentFactory.initilize_actions(agents)
        return agents


