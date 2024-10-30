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
            content = agent.system_message[:]
            print(content)
            tooltip_content = html.escape(content)
            self.graph.node(agent.get_name(), agent.get_name(), tooltip = tooltip_content)
            break

        self.render()

    def sanitize_tooltip(self, content: str) -> str:
        """Sanitize the tooltip content by escaping special HTML characters."""
        sanitized_content = html.escape(content)
        return (
            f"<TABLE BORDER='0' CELLBORDER='1' CELLSPACING='0' "
            f"STYLE='max-height: 150px; overflow-y: auto; display: block;'>"
            f"<TR><TD>{sanitized_content}</TD></TR></TABLE>"
        )

    def render(self) -> None:
        file_path = os.path.join(GraphMaker.PARENT_FILE_PATH, "tmp", self.name)
        self.graph.render(file_path, format='svg')
        
