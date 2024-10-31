from functools import cache
import os
from pathlib import Path


class FileUtils:

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