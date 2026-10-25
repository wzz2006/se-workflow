# tools/printer.py

class C:
    """ANSI 颜色代码常量"""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"


def print_pretty(result: dict) -> None:
    """美观地打印生成结果。"""
    lang = result.get("language", "unknown")
    code = result.get("code", "")
    explanation = result.get("explanation", "")
    usage = result.get("usage", "")
    deps = result.get("dependencies", []) or []

    if result.get("error"):
        print(f"{C.RED}[错误] {result['error']}{C.RESET}")
        return

    # 标题
    print()
    print(f"{C.BOLD}{C.CYAN}{'=' * 60}{C.RESET}")
    print(f"{C.BOLD}{C.CYAN}  代码生成结果{C.RESET}")
    print(f"{C.BOLD}{C.CYAN}{'=' * 60}{C.RESET}")

    # 语言
    print(f"{C.BOLD}语言:{C.RESET} {C.GREEN}{lang}{C.RESET}")
    print()

    # 代码块
    print(f"{C.BOLD}{C.YELLOW}── 代码 ──────────────────────────────────────{C.RESET}")
    print(f"{C.GREEN}{code}{C.RESET}")
    print(f"{C.BOLD}{C.YELLOW}──────────────────────────────────────────────{C.RESET}")
    print()

    # 说明
    if explanation:
        print(f"{C.BOLD}{C.MAGENTA}说明:{C.RESET} {explanation}")
        print()

    # 使用方式
    if usage:
        print(f"{C.BOLD}{C.MAGENTA}使用:{C.RESET} {usage}")
        print()

    # 依赖
    if deps:
        print(f"{C.BOLD}{C.MAGENTA}依赖:{C.RESET} {', '.join(deps)}")
    else:
        print(f"{C.BOLD}{C.MAGENTA}依赖:{C.RESET} {C.DIM}无{C.RESET}")

    print(f"{C.BOLD}{C.CYAN}{'=' * 60}{C.RESET}")
    print()