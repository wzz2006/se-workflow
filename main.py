"""CLI 入口（阶段0占位：仅验证环境与参数解析）。"""
import argparse
import sys


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="SE Workflow: 需求分析 -> 代码设计 -> 代码审查")
    p.add_argument("-i", "--input", default="examples/input_sample.txt")
    p.add_argument("--mock", action="store_true", help="使用 Mock Agent，不调用 LLM")
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    print(f"[stage0] input={args.input}, mock={args.mock}")
    print("[stage0] 环境就绪，等待阶段1实现 Orchestrator。")
    return 0


if __name__ == "__main__":
    sys.exit(main())