from agents.agent import Agent
from llm.llm_enum import LLMEnum


class AgentConstruct:

    def __init__(self, name : str):
        self.name = name
        self.system_message = None
        self.llm = None

    def with_system_message(self, system_message : str) -> "AgentConstruct":
        self.system_message = system_message
        return self
    
    def with_llm(self, llm) -> "AgentConstruct":
        self.llm = llm
        return self
    
    def build(self) -> Agent:
        if self.name is None or len(self.name) <= 0:
            raise RuntimeError(f"Agent must have a name")
        if self.system_message is None:
            raise RuntimeError(f"Agent {self.name} has not system_message")
        if self.llm is None:
            self.llm = LLMEnum.default_llm()

        return Agent(name = self.name, llm=self.llm, system_message=self.system_message)