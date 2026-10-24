from core.state import WorkflowState
from agents.base import BaseAgent
from tools.llm import call_llm
from tools.json_parser import extract_json
from prompts.review_prompt import SYSTEM_PROMPT
import json

class ReviewAgent(BaseAgent):
    name = "ReviewAgent"

    def run(self, state: WorkflowState) -> WorkflowState:
        if not state.design:
            state.errors.append("无设计可审查")
            return state

        user_prompt = f"原始需求：\n{json.dumps(state.requirements, ensure_ascii=False)}\n\n设计方案：\n{json.dumps(state.design, ensure_ascii=False)}"

        try:
            raw_response = call_llm(SYSTEM_PROMPT, user_prompt)
            state.review = extract_json(raw_response)
            
            # 强制把 passed 转为布尔值，防止 LLM 输出字符串 "true"
            if isinstance(state.review.get("passed"), str):
                state.review["passed"] = state.review["passed"].lower() == "true"
                
            msg = "审查通过" if state.review.get("passed") else f"审查发现 {len(state.review.get('issues', []))} 个问题"
            state.emit(self.name, "Orchestrator", msg)
        except Exception as e:
            state.errors.append(f"代码审查失败: {str(e)}")

        return state