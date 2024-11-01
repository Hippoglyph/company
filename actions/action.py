class Action:

    NAME = "action_name"

    CALLER_AGENT = "caller_agent"

    def get_name(self) -> str:
        pass

    def get_description(self) -> str:
        pass

    def get_arguments(self) -> dict:
        return []
    
    def execute(self, arguments : dict) -> str:
        pass
