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
        self.name = name
        self.edge_id = 0

        for agent in agents:
            tooltip_content = html.escape(agent.system_message)
            self.graph.node(agent.get_name(), agent.get_name(), tooltip = tooltip_content)

        self.render()

    def action(self, action : Action, arguments : dict, response : str) -> None:
        self.edge_id += 1
        if isinstance(action, SendMessageAction):
            tooltip_content = html.escape(response)
            self.graph.edge(arguments[Action.CALLER_AGENT].get_name(), arguments[SendMessageAction.RECEIVER], label=str(self.edge_id), tooltip = tooltip_content)
        else:
            print("Log action TODO")
            #raise RuntimeError("Graph: No action but SendMessage is implmented yet")

        self.render()

    def render(self) -> None:
        file_path = os.path.join(GraphMaker.PARENT_FILE_PATH, "tmp", self.name)
        self.graph.render(file_path, format='svg')
        self.create_html_with_js(file_path + '.svg')

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
        
