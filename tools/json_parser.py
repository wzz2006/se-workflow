import json
import re

def extract_json(text: str) -> dict:
    """从 LLM 的原始输出中容错提取 JSON"""
    text = text.strip()
    
    # 1. 直接解析
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
        
    # 2. 提取 ```json ... ``` 代码块
    match = re.search(r'```(?:json)?(.*?)```', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1).strip())
        except json.JSONDecodeError:
            pass
            
    # 3. 提取第一个 { 到最后一个 } 之间的内容
    start = text.find('{')
    end = text.rfind('}')
    if start != -1 and end != -1 and start < end:
        try:
            return json.loads(text[start:end+1])
        except json.JSONDecodeError:
            pass
            
    raise ValueError("无法从输出中解析出合法的 JSON")