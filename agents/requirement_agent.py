from core.state import WorkflowState
from agents.base import BaseAgent

class RequirementAgent(BaseAgent):
    name = "RequirementAgent"

    def run(self, state: WorkflowState) -> WorkflowState:
        if not state.raw_input.strip():
            state.errors.append("需求输入为空")
            return state
            
        # 模拟：按句号拆分功能点
        features = [s.strip() for s in state.raw_input.replace("。", ".").split(".") if s.strip()]
        
        state.requirements = {
            "features": features,
            "constraints": ["模拟约束：需支持并发"],
            "acceptance": ["模拟验收：跑通即可"]
        }
        
        state.emit(self.name, "DesignAgent", f"解析出 {len(features)} 个功能点")
        return state