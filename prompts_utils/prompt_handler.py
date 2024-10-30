from functools import cache
import os


class PromptHandler:

    PARENT_FILE_PATH = os.path.dirname(os.path.abspath(__file__))
    MAIN_PROMPT_REPLACE = "main_prompt"
    AGENT_PROMPT_REPLACE  = "agent_prompt"

    @staticmethod
    def get_coder_prompt() -> str:
        return PromptHandler._get_agent_prompt("coder")
    
    @staticmethod
    def _get_agent_prompt(agent_file_name : str) -> str:
        main_prompt = PromptHandler._get_main_prompt()
        main_mission = PromptHandler._get_main_mission_prompt()
        agent_mission = PromptHandler._read_file(agent_file_name)
        return main_prompt.format(**{
            PromptHandler.MAIN_PROMPT_REPLACE : main_mission,
            PromptHandler.AGENT_PROMPT_REPLACE : agent_mission
        })

    @staticmethod
    def _get_main_mission_prompt() -> str:
        return PromptHandler._read_file("main_mission")
    
    @staticmethod
    def _get_main_prompt() -> str:
        return PromptHandler._read_file("main")

    @staticmethod
    @cache
    def _read_file(file_name : str) -> str:
        file_path = os.path.join(PromptHandler.PARENT_FILE_PATH, "prompts", f"{file_name}.md")
        with open(file_path, "r") as file:
            return file.read()
    
