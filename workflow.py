from actions.send_message_action import SendMessageAction
from agents.agent_tracker import AgentTracker
from factory.agent_factory import AgentFactory
from logs.graph.graph_maker import GraphMaker

def run():
    
    agents = AgentFactory.build()

    graph = GraphMaker()
    graph.new_graph("graph", agents)

    for agent_candidate in agents:
        if agent_candidate.is_human(): # Find first human
            agent = agent_candidate
            break

    response = agent.send_message("Welcome to The Company. How can we help you?")
    while True:
        action, arguments = agent.choose_action(response)
        graph.action(action=action, arguments=arguments, response=response)
        if isinstance(action, SendMessageAction):
            agent = AgentTracker.get(action.get_receiver_name(arguments))
        response = agent.send_message(action.execute(arguments))