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
        base_prompt = f"需求如下：\n{json.dumps(state.requirements, ensure_ascii=False)}\n"
        
        if state.review and not state.review.get("passed"):
            base_prompt += f"\n上一版设计存在以下问题，请修复：\n{state.review.get('issues')}"

        user_prompt = base_prompt
        
        # 尝试最多 2 次
        for attempt in range(2):
            try:
                raw_response = call_llm(SYSTEM_PROMPT, user_prompt)
                state.design = extract_json(raw_response)
                state.emit(self.name, "ReviewAgent", f"LLM 产出 {len(state.design.get('modules', []))} 个模块设计 (重试次数: {state.retry_count})")
                return state  # 成功解析，直接返回
            except Exception as e:
                if attempt == 1:
                    # 第二次还是失败，才记录错误
                    state.errors.append(f"代码设计失败 (已重试): {str(e)}")
                else:
                    # 第一次失败，追加提示并重试
                    print(f"⚠️ 设计输出解析失败，正在重试 (第 {attempt+1} 次)...")
                    user_prompt = base_prompt + "\n\n【注意】上次输出被截断或格式错误，请务必精简内容，严格输出合法的 JSON，不要包含 Markdown 代码块标记！"

        return state