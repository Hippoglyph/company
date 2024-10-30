from dotenv import load_dotenv
load_dotenv(override=True)

from agents.agent import Agent
from llm.llm_enum import LLMEnum

llm = LLMEnum.LLaMa3_8b.value

agent = Agent(llm=llm, system_message="You writer assistant that spawns ideas")

while True:
    user = input(">")
    agent.send_message(user)