from dotenv import load_dotenv
load_dotenv(override=True)

from factory.agent_factory import AgentFactory

from agents.agent import Agent
from llm.llm_enum import LLMEnum

agents = AgentFactory.create_agents()

coder = agents[0].build()
print(coder.system_message)

# while True:
#     user = input(">")
#     agent.send_message(user)