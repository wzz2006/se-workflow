import os
from dotenv import load_dotenv
from openai import OpenAI

# 加载 .env 文件中的环境变量
load_dotenv()

def call_llm(system_prompt: str, user_prompt: str) -> str:
    """调用 DeepSeek 接口，返回纯文本"""
    api_key = os.getenv("DEEPSEEK_API_KEY")
    base_url = os.getenv("LLM_BASE_URL", "https://api.deepseek.com")
    model = os.getenv("LLM_MODEL", "deepseek-flash")

    if not api_key:
        raise ValueError("未找到 DEEPSEEK_API_KEY，请检查 .env 文件")

    # 直接用浮点数设置全局超时，最高重试 2 次
    client = OpenAI(
        api_key=api_key, 
        base_url=base_url,
        timeout=120.0,  # 120秒超时
        max_retries=2
    )

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.1,  # 保证格式稳定
            max_tokens=6000,  # 允许更长的输出，防止 JSON 截断
        )
        return response.choices[0].message.content
    except Exception as e:
        raise RuntimeError(f"LLM 调用失败: {str(e)}")