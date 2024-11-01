from functools import cache
import os
import subprocess
import docker
from docker import DockerClient
from docker.models.containers import Container

from utils.file_utils import FileUtils

class Terminal:

    def __init__(self, run_id : str):
        self.container = Terminal._get_container(run_id)

    def bash(self, cmd : str) -> str:
        exec_result = self.container.exec_run(f"sh -c '{cmd}'", tty=True, user="Agent")
        return exec_result.output.decode('utf-8').strip()
    
    def close(self) -> None:
        self.container.stop()

    def write_file(self, file_path: str, content: str) -> str:
        temp_file_path = FileUtils.get_root() / "tmp"
        with open(temp_file_path, 'w') as temp_file:
            temp_file.write(content)

        target_directory = self.bash(f"dirname {file_path}")
        self.bash(f"mkdir -p {target_directory}")

        subprocess.run(["docker", "cp", temp_file_path, f"{self.container.name}:app/{file_path}"], check=True)
        os.remove(temp_file_path)
        return f"Successfully wrote to {file_path}" # TODO error handling

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
