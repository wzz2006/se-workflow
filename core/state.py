from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class WorkflowState:
    raw_input: str = ""
    requirements: Dict[str, Any] = field(default_factory=dict)  # 需求Agent写
    design: Dict[str, Any] = field(default_factory=dict)        # 设计Agent写
    review: Dict[str, Any] = field(default_factory=dict)        # 审查Agent写
    code: Dict[str, Any] = field(default_factory=dict)          # CodeGenAgent写（预留）
    
    messages: List[Dict[str, str]] = field(default_factory=list) # Agent间通信消息
    logs: List[str] = field(default_factory=list)                # 执行日志
    errors: List[str] = field(default_factory=list)              # 错误收集
    retry_count: int = 0

    def emit(self, sender: str, receiver: str, content: str):
        """记录 Agent 之间的消息传递"""
        self.messages.append({"from": sender, "to": receiver, "content": content})
        self.logs.append(f"[{sender} -> {receiver}] {content}")