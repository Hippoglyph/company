from functools import cache
import os
from pathlib import Path
import subprocess
import docker
from docker.models.containers import Container

class Terminal:

    def __init__(self, run_id : str):
        self.container = Terminal._get_container(run_id)

    def bash(self, cmd : str) -> str:
        exec_result = self.container.exec_run(f"sh -c '{cmd}'", user="Agent")
        exit_code = exec_result.exit_code
        output = exec_result.output.decode('utf-8').strip()
        
        if exit_code != 0:
            return f"Command failed with exit code {exit_code}: {output}"
        
        return output
    
    def close(self) -> None:
        self.container.stop()

    def write_file(self, file_path: str, content: str) -> str:
        if self.file_exists(file_path):
            return f"Could not write to file {file_path}. Already exists."
        
        temp_file_path = Terminal.get_tmp_folder() / "tmp"
        with open(temp_file_path, 'w') as temp_file:
            temp_file.write(content)

        target_directory = self.bash(f"dirname {file_path}")
        self.bash(f"mkdir -p {target_directory}")

        try:
            subprocess.run(["docker", "cp", temp_file_path, f"{self.container.name}:/app/{file_path}"], check=True, stdout=subprocess.DEVNULL)
            os.remove(temp_file_path)
            return f"Successfully wrote to {file_path}"
        except subprocess.CalledProcessError:
            os.remove(temp_file_path)
            return f"Error writing to {file_path}"
        
    def file_exists(self, file_path: str) -> bool:
        # Check if the file already exists in the container
        check_file_cmd = f"test -f /app/{file_path} && echo 'exists' || echo 'not exists'"
        return self.bash(check_file_cmd).strip() == 'exists'

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
    @cache
    def get_tmp_folder() -> Path:
        root = Path(os.getcwd())
        while root.parent != root:
            if (root / '.git').exists() or (root / '.venv').exists():
                break
            root = root.parent
        else:
            raise FileNotFoundError("Project root not found. Make sure you have a .git folder or .project-root file in your project root.")
        return root / "work_folder"
