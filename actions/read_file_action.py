from pathlib import Path
from actions.action import Action
from utils.file_utils import FileUtils


class ReadFileAction(Action):

    FILE_PATH = "file_path"

    def get_name(self) -> str:
        return "ReadFile"

    def get_description(self) -> str:
        return "Read the content to the file_path. Relative to root"

    def get_arguments(self) -> dict:
        return {ReadFileAction.FILE_PATH : "The path to the file. E.g folder/subfolder/executeable.typ"}
    
    def execute(self, arguments : dict) -> str:
        # TODO sanity check
        relative_path = arguments[ReadFileAction.FILE_PATH]
        full_path : Path = FileUtils._get_root() / relative_path

        if not full_path.exists():
            return f"The file {relative_path} does not exist"
        
        with open(full_path, 'r') as file:
            content = file.readlines()

        return f"The file {relative_path} contained:\n{content}"