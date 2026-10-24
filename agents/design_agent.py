from core.state import WorkflowState
from agents.base import BaseAgent

class DesignAgent(BaseAgent):
    name = "DesignAgent"

    def run(self, state: WorkflowState) -> WorkflowState:
        if not state.requirements.get("features"):
            state.errors.append("无需求可设计")
            return state

        features = state.requirements["features"]
        modules = []
        
        # Mock 逻辑：如果是第一次设计且功能点大于2个，故意漏掉 interface，让审查去挑刺
        # 这样编排器就能触发重试流程
        is_first_try = state.retry_count == 0
        
        for i, feat in enumerate(features):
            mod = {
                "name": f"Module_{i+1}",
                "responsibility": f"实现：{feat}"
            }
            if len(features) <= 2 or not is_first_try:
                mod["interface"] = f"def func_{i+1}(): pass"
            
            modules.append(mod)

        state.design = {
            "modules": modules,
            "data_flow": "输入 -> 处理 -> 输出",
            "pseudocode": "// 伪代码省略"
        }
        
        state.emit(self.name, "ReviewAgent", f"产出 {len(modules)} 个模块设计 (重试次数: {state.retry_count})")
        return state