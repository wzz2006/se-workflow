from core.state import WorkflowState

class BaseAgent:
    name = "base"

    def run(self, state: WorkflowState) -> WorkflowState:
        """所有 Agent 必须实现这个方法"""
        raise NotImplementedError("Agent must implement run() method")