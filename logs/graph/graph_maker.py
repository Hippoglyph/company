from functools import cache
import html
import os
import graphviz

from actions.action import Action
from actions.send_message_action import SendMessageAction
from agents.agent import Agent

class GraphMaker:
    
    PARENT_FILE_PATH = os.path.dirname(os.path.abspath(__file__))

    def new_graph(self, name : str, agents : list[Agent]) -> None:
        self.graph = graphviz.Digraph()
        self.graph_full = graphviz.Digraph()
        self.name = name
        self.edge_id = 0
        self.actions = {}

        for agent in agents:
            self._make_dubble_node(agent.get_name(), agent.system_message)
            actions = agent.get_actions()
            for action in actions:  
                self.actions[action.get_name()] = action
        
        for action_name, action in self.actions.items():
            if isinstance(action, SendMessageAction):
                continue
            self._make_dubble_node(action_name, action.get_description(), is_action = True)

        self.render()

    def action(self, action : Action, arguments : dict, response : str, action_response : str) -> None:
        self.edge_id += 1
        if isinstance(action, SendMessageAction):
            self._make_edge(arguments[Action.CALLER_AGENT].get_name(), arguments[SendMessageAction.RECEIVER], str(self.edge_id), action_response, response)
        else:
            self._make_edge(arguments[Action.CALLER_AGENT].get_name(), action.get_name(), str(self.edge_id), action.prettify(arguments), response)
            self.edge_id += 1
            self._make_edge(action.get_name(), arguments[Action.CALLER_AGENT].get_name(), str(self.edge_id), action_response, action_response)

        self.render()

    def render(self) -> None:
        file_path = os.path.join(GraphMaker.PARENT_FILE_PATH, "tmp", self.name)
        self.graph.render(file_path, format='svg')
        self.graph_full.render(file_path+"_full", format='svg')
        self.create_html_with_js(file_path + '.svg')
        self.create_html_with_js(file_path+"_full" + '.svg')

    @staticmethod
    @cache
    def _get_html_template() -> str:
        file_path = os.path.join(GraphMaker.PARENT_FILE_PATH, "resources", "html_template.html")
        with open(file_path, 'r') as f:
            html = f.read()
        return html

    def create_html_with_js(self, svg_file : str) -> None:
        with open(svg_file, 'r') as f:
            svg_content = f.read()
        template = GraphMaker._get_html_template()
        
        html_content = template.replace("!SVG_REPLACE!", svg_content)
        
        html_file = svg_file.replace('.svg', '.html')
        with open(html_file, 'w') as f:
            f.write(html_content)

    def _make_dubble_node(self, name : str, tooltip : str, is_action : bool = False) -> None:
        GraphMaker._make_node(self.graph, name, tooltip, is_action = is_action)
        GraphMaker._make_node(self.graph_full, name, tooltip, is_action = is_action)

    def _make_node(graph : graphviz.Digraph, name : str, tooltip : str, is_action : bool = False) -> None:
        graph.node(name, name, tooltip = html.escape(tooltip), style = "dashed" if is_action else "solid")

    def _make_edge(self, from_name : str, to_name : str, label : str, tooltip : str, tooltip_full : str) -> None:
        self.graph.edge(from_name, to_name, label=label, tooltip = html.escape(tooltip))
        self.graph_full.edge(from_name, to_name, label=label, tooltip = html.escape(tooltip_full))

        
