from core.state import WorkflowState
from agents.requirement_agent import RequirementAgent
from agents.design_agent import DesignAgent
from agents.review_agent import ReviewAgent

class Orchestrator:
    def __init__(self, max_retry=2):
        # Agent 注册表
        self.agents = {
            "req": RequirementAgent(),
            "design": DesignAgent(),
            "review": ReviewAgent()
        }
        self.max_retry = max_retry

    def run(self, raw_input: str) -> WorkflowState:
        state = WorkflowState(raw_input=raw_input)
        state.logs.append("=== Workflow 开始 ===")

        # 1. 需求分析
        state = self.agents["req"].run(state)
        if state.errors:
            state.logs.append("需求阶段报错，流程终止")
            return state

        # 2. 设计 -> 审查（带循环回退）
        while True:
            # 执行设计
            state = self.agents["design"].run(state)
            
            # 执行审查
            state = self.agents["review"].run(state)
            
            # 检查是否通过
            if state.review.get("passed"):
                state.logs.append("=== Workflow 完成：审查通过 ===")
                break
                
            # 如果没通过，准备重试
            state.retry_count += 1
            if state.retry_count > self.max_retry:
                state.logs.append(f"=== Workflow 终止：达到最大重试次数 {self.max_retry} ===")
                state.errors.append("审查持续不通过，人工介入")
                break
                
            state.logs.append(f"--- 审查未通过，回流至 DesignAgent (第 {state.retry_count} 次重试) ---")

        return state