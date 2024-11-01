from actions.action import Action
from agents.agent import Agent
from logs.graph.graph_maker import GraphMaker

class Log:

    def __init__(self, run_id : str, agents : list[Agent]):
        self.graph = GraphMaker()
        self.graph.new_graph(run_id, agents)

    def log(self, action : Action, arguments : dict, response : str) -> None:
        self.graph.action(action=action, arguments=arguments, response=response)