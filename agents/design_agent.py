from core.state import WorkflowState
from agents.base import BaseAgent
from tools.llm import call_llm
from tools.json_parser import extract_json
from prompts.design_prompt import SYSTEM_PROMPT
import json

class DesignAgent(BaseAgent):
    name = "DesignAgent"

    def run(self, state: WorkflowState) -> WorkflowState:
        if not state.requirements:
            state.errors.append("无需求可设计")
            return state

        # 把需求转成字符串发给 LLM
        user_prompt = f"需求如下：\n{json.dumps(state.requirements, ensure_ascii=False)}\n"
        
        # 如果之前审查没通过，把审查意见带上，让它修改
        if state.review and not state.review.get("passed"):
            user_prompt += f"\n上一版设计存在以下问题，请修复：\n{state.review.get('issues')}"

        try:
            raw_response = call_llm(SYSTEM_PROMPT, user_prompt)
            state.design = extract_json(raw_response)
            state.emit(self.name, "ReviewAgent", f"LLM 产出 {len(state.design.get('modules', []))} 个模块设计 (重试次数: {state.retry_count})")
        except Exception as e:
            state.errors.append(f"代码设计失败: {str(e)}")

        return state