"""CLI 入口：运行 Workflow 并打印结果"""
import argparse
import sys
import json
from core.orchestrator import Orchestrator
from tools.printer import print_pretty


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="SE Workflow: 需求分析 -> 代码设计 -> 代码审查")
    p.add_argument("-i", "--input", default="examples/input_sample.txt", help="需求文本文件路径")
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    
    # 1. 读取输入
    try:
        with open(args.input, "r", encoding="utf-8") as f:
            raw_input = f.read()
    except FileNotFoundError:
        print(f"找不到输入文件: {args.input}")
        return 1

    # 2. 运行工作流
    orchestrator = Orchestrator()
    state = orchestrator.run(raw_input)

    # 3. 打印追踪日志
    print("\n========== 执行日志 ==========")
    for log in state.logs:
        print(log)
        
    # 4. 打印最终的结构化状态 (JSON格式)
    print("\n========== 最终状态 (JSON) ==========")
    print(json.dumps({
        "requirements": state.requirements,
        "design": state.design,
        "review": state.review,
        "code": state.code.get("content", "未执行代码生成"),
        "errors": state.errors,
        "retry_count": state.retry_count
    }, ensure_ascii=False, indent=2))
    
    # 5. 打印并保存生成的代码
    if state.code:
        # 调用美化打印函数
        print_pretty(state.code)

    return 0


if __name__ == "__main__":
    sys.exit(main())