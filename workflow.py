from agents.agent_tracker import AgentTracker
from factory.agent_factory import AgentFactory
from logs.graph.graph_maker import GraphMaker

def run():

    agents = AgentFactory.build()

    graph = GraphMaker()
    graph.new_graph("graph", agents)

    agent = agents[0]

    seed_msg = input(">")
    response = agent.send_message(seed_msg)
    while True:
        action, arguments = agent.choose_action(response)
        agent_name, response = action.execute(arguments)
        agent = AgentTracker.get(agent_name)