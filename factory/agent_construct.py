from actions.action import Action
from agents.agent import Agent
from llm.llm_enum import LLMEnum
from prompts_utils.prompt_handler import PromptHandler


class AgentConstruct:

    def __init__(self, name : str):
        self.name = name
        self.llm = None
        self.actions = []
        self.human = False
    
    def build(self) -> Agent:
        if self.name is None or len(self.name) <= 0:
            raise RuntimeError(f"Agent must have a name")
        if self.llm is None:
            self.llm = LLMEnum.default_llm()
        if len(self.actions) <= 0:
            raise RuntimeError(f"Agent {self.name} has no actions")

        system_message = PromptHandler.get_agent_prompt(self.name, self.actions)
        return Agent(name = self.name, llm=self.llm, system_message=system_message, actions=self.actions, human=self.human)

    def is_human(self, human : bool = True) -> "AgentConstruct":
        self.human = human
        return self
    
    def with_llm(self, llm) -> "AgentConstruct":
        self.llm = llm
        return self
    
    def with_action(self, action : Action) -> "AgentConstruct":
        self.actions += [action]
        return self