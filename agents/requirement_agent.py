from core.state import WorkflowState
from agents.base import BaseAgent
from tools.llm import call_llm
from tools.json_parser import extract_json
from prompts.requirement_prompt import SYSTEM_PROMPT

class RequirementAgent(BaseAgent):
    name = "RequirementAgent"

    def run(self, state: WorkflowState) -> WorkflowState:
        if not state.raw_input.strip():
            state.errors.append("需求输入为空")
            return state
            
        try:
            raw_response = call_llm(SYSTEM_PROMPT, state.raw_input)
            state.requirements = extract_json(raw_response)
            state.emit(self.name, "DesignAgent", f"LLM 解析出 {len(state.requirements.get('features', []))} 个功能点")
        except Exception as e:
            state.errors.append(f"需求分析失败: {str(e)}")
            
        return state