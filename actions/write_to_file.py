from functools import cache
import os
from pathlib import Path
from actions.action import Action


class WriteToFile(Action):

    FILE_PATH = "file_path"
    CONTENT = "content"

    def get_name(self) -> str:
        return "WriteToFile"

    def get_description(self) -> str:
        return "Writes the content to the file_path. Relative to root"

    def get_arguments(self) -> dict:
        return {WriteToFile.FILE_PATH : "The path to the file. E.g folder/subfolder/executeable.typ",
            WriteToFile.CONTENT : "The intended content in the file"
        }
    
    @staticmethod
    @cache
    def _get_root() -> Path:
        root = Path(os.getcwd())
        while root.parent != root:
            if (root / '.git').exists() or (root / '..venv').exists():
                break
            root = root.parent
        else:
            raise FileNotFoundError("Project root not found. Make sure you have a .git folder or .project-root file in your project root.")
        return root / "work_folder"
    
    def execute(self, arguments : dict) -> str:
        # TODO sanity check
        relative_path = arguments[WriteToFile.FILE_PATH]
        full_path : Path = WriteToFile._get_root() / relative_path
        full_path.parent.mkdir(parents=True, exist_ok=True)

        with open(full_path, 'w') as file:
            file.write(arguments[WriteToFile.CONTENT])

        return f"Content written to {relative_path} successfully"