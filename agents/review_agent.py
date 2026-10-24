from core.state import WorkflowState
from agents.base import BaseAgent

class ReviewAgent(BaseAgent):
    name = "ReviewAgent"

    def run(self, state: WorkflowState) -> WorkflowState:
        issues = []
        modules = state.design.get("modules", [])
        
        if not modules:
            issues.append("设计为空")

        # 检查每个模块是否包含 interface
        for m in modules:
            if "interface" not in m:
                issues.append(f"模块 [{m['name']}] 缺少接口定义 (interface)")

        passed = len(issues) == 0
        
        state.review = {
            "issues": issues,
            "passed": passed
        }
        
        msg = "审查通过" if passed else f"审查发现 {len(issues)} 个问题"
        state.emit(self.name, "Orchestrator", msg)
        return state