from pathlib import Path
from actions.action import Action
from utils.file_utils import FileUtils


class WriteFileAction(Action):

    FILE_PATH = "file_path"
    CONTENT = "content"

    def get_name(self) -> str:
        return "WriteFile"

    def get_description(self) -> str:
        return "Writes the content to the file_path. Relative to root"

    def get_arguments(self) -> dict:
        return {WriteFileAction.FILE_PATH : "The path to the file. E.g folder/subfolder/executeable.typ",
            WriteFileAction.CONTENT : "The intended content in the file"
        }
    
    def execute(self, arguments : dict) -> str:
        # TODO sanity check
        relative_path = arguments[WriteFileAction.FILE_PATH]
        full_path : Path = FileUtils._get_root() / relative_path
        full_path.parent.mkdir(parents=True, exist_ok=True)

        with open(full_path, 'w') as file:
            file.write(arguments[WriteFileAction.CONTENT])

        return f"Content written to {relative_path} successfully"