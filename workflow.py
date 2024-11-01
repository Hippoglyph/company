from actions.send_message_action import SendMessageAction
from agents.agent_tracker import AgentTracker
from factory.agent_factory import AgentFactory
from logs.graph.log import Log

def run():
    run_id = "test_run"
    agents = AgentFactory.build(run_id)

    log = Log(run_id, agents)

    for agent_candidate in agents:
        if agent_candidate.is_human(): # Find first human
            agent = agent_candidate
            break

    response = agent.send_message("Welcome to The Company. How can we help you?")
    while True:
        action, arguments = agent.choose_action(response)
        if isinstance(action, SendMessageAction):
            agent = AgentTracker.get(action.get_receiver_name(arguments))
        action_response = action.execute(arguments)
        log.log(action=action, arguments=arguments, response=response, action_response = action_response)
        response = agent.send_message(action_response)