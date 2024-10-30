from dotenv import load_dotenv
load_dotenv(override=True)

from factory.agent_factory import AgentFactory

agents = AgentFactory.build()

coder = agents[0]
#print(coder.system_message)

while True:
    user = input(">")
    coder.send_message(user)