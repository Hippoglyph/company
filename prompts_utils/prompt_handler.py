from functools import cache
import os
from actions.action import Action


class PromptHandler:

    PARENT_FILE_PATH = os.path.dirname(os.path.abspath(__file__))
    MAIN_PROMPT_REPLACE = "main_prompt"
    AGENT_PROMPT_REPLACE  = "agent_prompt"
    ACTIONS_PROMPT_REPLACE = "actions"

    @staticmethod
    def get_agent_prompt(agent_name : str, actions : list[Action]) -> str:
        main_prompt = PromptHandler._get_main_prompt()
        main_mission = PromptHandler._get_main_mission_prompt()
        agent_mission = PromptHandler._read_file(agent_name)
        return main_prompt.format(**{
            PromptHandler.ACTIONS_PROMPT_REPLACE : PromptHandler._get_actions_format(actions),
            PromptHandler.MAIN_PROMPT_REPLACE : main_mission,
            PromptHandler.AGENT_PROMPT_REPLACE : agent_mission
        })
    
    def _get_actions_format(actions : list[Action]) -> str:
        return "\n".join([PromptHandler._get_action_format(action) for action in actions])
    
    def _get_action_format(action : Action) -> str:
        return f"```{Action.NAME}\n{Action.NAME}: {action.get_name()}\ndescription: {action.get_description()}\n---\n{PromptHandler._get_action_arguments_format(action)}\n```"
    
    def _get_action_arguments_format(action : Action) -> str:
        return "\n\n".join([f"argument name: {name}\nargument description: {description}" for name, description in action.get_arguments().items()])

    @staticmethod
    def _get_main_mission_prompt() -> str:
        return PromptHandler._read_file("main_mission")
    
    @staticmethod
    def _get_main_prompt() -> str:
        return PromptHandler._read_file("main")
    
    @staticmethod
    @cache
    def get_action(action_name : str, **kwarg) -> str:
        action_rows = ["<action>"]
        action_rows += [f"<action_name>{action_name}</action_name>"]
        for key, value in kwarg.items():
            action_rows += [f"<{key}>{value}</{key}>"]
        action_rows += ["</action>"]
        return "\n".join(action_rows)

    @staticmethod
    @cache
    def _read_file(file_name : str) -> str:
        file_path = os.path.join(PromptHandler.PARENT_FILE_PATH, "prompts", f"{file_name}.md")
        with open(file_path, "r") as file:
            return file.read()
    
