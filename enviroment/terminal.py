from functools import cache
import docker
from docker.models.containers import Container

class Terminal:

    def __init__(self, run_id : str):
        self.run_id = run_id

    def bash(self, cmd : str) -> str:
        #return Terminal._run_command_in_docker_bash(self.run_id, cmd)
        print(Terminal._run_command_in_docker_bash(self.run_id, cmd))
    
    def close(self) -> None:
        Terminal._get_container(self.run_id).stop()

    @cache
    @staticmethod
    def _get_container(container_name : str) -> Container:
        client = docker.from_env()
        try:
            container = client.containers.get(container_name)
            if container.status != "running":
                container.start()
            return container
        except docker.errors.NotFound:
            return client.containers.run("company-image", name=container_name, detach=True, tty=True)
        
    @staticmethod
    def _run_command_in_docker_bash(container_name : str, cmd : str) -> str:
        container = Terminal._get_container(container_name)
        exec_result = container.exec_run(f"sh -c '{cmd}'", tty=True, user="Agent")
        return exec_result.output.decode('utf-8')

