from factory.agent_construct import AgentConstruct
from prompts_utils.prompt_handler import PromptHandler


class AgentFactory:

    @staticmethod
    def create_agents() -> list[AgentConstruct]:
        agents = []

        agents += [
            AgentConstruct("Coder")
                .with_system_message(PromptHandler.get_coder_prompt())
        ]
        return agents