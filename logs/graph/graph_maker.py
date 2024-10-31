from functools import cache
import html
import os
import graphviz

from agents.agent import Agent

class GraphMaker:
    
    PARENT_FILE_PATH = os.path.dirname(os.path.abspath(__file__))

    def new_graph(self, name : str, agents : list[Agent]) -> None:
        self.graph = graphviz.Digraph()
        self.name = name

        for agent in agents:
            tooltip_content = html.escape(agent.system_message)
            self.graph.node(agent.get_name(), agent.get_name(), tooltip = tooltip_content)

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
        
