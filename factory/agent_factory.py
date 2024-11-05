from actions.bash_action import BashAction
from actions.read_file_action import ReadFileAction
from actions.send_message_action import SendMessageAction
from actions.write_file_action import WriteFileAction
from agents.agent import Agent
from agents.agent_names import AgentNames
from agents.agent_tracker import AgentTracker
from factory.agent_construct import AgentConstruct


class AgentFactory:

    @staticmethod
    def create_agents(run_id : str) -> list[AgentConstruct]:
        agents = []

        agents += [
            AgentConstruct(AgentNames.ARCHITECT)
                .with_action(SendMessageAction([AgentNames.CODER]))
                .with_action(BashAction(run_id))
                .is_human()
            ,
            AgentConstruct(AgentNames.CODER)
                .with_action(SendMessageAction([AgentNames.ARCHITECT, AgentNames.CODE_REVIEWER]))
                .with_action(WriteFileAction(run_id))
                .with_action(ReadFileAction(run_id))
                .with_action(BashAction(run_id))
            ,
            AgentConstruct(AgentNames.CODE_REVIEWER)
                .with_action(SendMessageAction([AgentNames.CODER]))
                .with_action(ReadFileAction(run_id))
                .with_action(BashAction(run_id))
        ]
        return agents
    
    def initilize_actions(agents : list[Agent]) -> None:
        AgentTracker.init(agents)
    
    @staticmethod
    def build(run_id : str) -> list[Agent]:
        agents = [agent.build() for agent in AgentFactory.create_agents(run_id)]
        AgentFactory.initilize_actions(agents)
        return agents


