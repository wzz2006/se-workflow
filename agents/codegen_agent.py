from core.state import WorkflowState
from agents.base import BaseAgent
from tools.llm import call_llm
from prompts.codegen_prompt import SYSTEM_PROMPT
import json
import re

class CodeGenAgent(BaseAgent):
    name = "CodeGenAgent"

    def run(self, state: WorkflowState) -> WorkflowState:
        if not state.design:
            state.errors.append("无设计可生成代码")
            return state

        # 把设计转为字符串
        user_prompt = f"基于以下设计生成代码：\n{json.dumps(state.design, ensure_ascii=False)}"

        try:
            raw_code = call_llm(SYSTEM_PROMPT, user_prompt)
            
            # 使用正则稳健提取：如果有 ```python 和 ``` 包裹，只提取中间的内容
            # 如果没有包裹，直接使用原文本
            match = re.search(r'```(?:python)?\n(.*?)```', raw_code, re.DOTALL)
            if match:
                code_text = match.group(1).strip()
            else:
                # 尝试直接清理首尾的 ``` 标记
                code_text = raw_code.strip()
                if code_text.startswith("```"):
                    lines = code_text.split("\n")
                    code_text = "\n".join(lines[1:]) # 去掉第一行
                if code_text.endswith("```"):
                    code_text = code_text[:-3].strip() # 去掉最后的 ```

            # 万一真的是空的，给个提示
            if not code_text:
                code_text = "# DeepSeek 没有返回代码内容，请重试。"

            state.code = {
                "language": "python", 
                "code": code_text,  # 确保这里用的是 "code"
                "explanation": "由 DeepSeek 根据审查通过的设计方案自动生成。",
                "usage": "可以直接运行或集成到你的项目中。",
                "dependencies": []
            }
            state.emit(self.name, "Orchestrator", "成功根据设计生成代码")
        except Exception as e:
            state.errors.append(f"代码生成失败: {str(e)}")

        return state