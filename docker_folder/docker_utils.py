from functools import cache
import docker
from docker.models.containers import Container

class DockerUtils:
    
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
    def bash(container_name : str, cmd : str) -> str:
        exec_result = DockerUtils._get_container(container_name).exec_run(cmd, tty=True)
        return exec_result.output.decode('utf-8')
    
    @staticmethod
    def stop(container_name : str) -> None:
        DockerUtils._get_container(container_name).stop()