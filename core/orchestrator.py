import yaml
from core.state import WorkflowState
from agents.requirement_agent import RequirementAgent
from agents.design_agent import DesignAgent
from agents.review_agent import ReviewAgent
# 注意：阶段 4 稍后会在这里引入 CodeGenAgent

class Orchestrator:
    def __init__(self, config_path="config/workflow.yaml"):
        # 1. 加载 YAML 配置
        with open(config_path, "r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f)
        
        self.max_retry = self.config.get("max_retry", 2)
        
        # 2. Agent 注册表（这就是可扩展性的核心：新增 Agent 只需在这里注册）
        self.agents = {
            "RequirementAgent": RequirementAgent(),
            "DesignAgent": DesignAgent(),
            "ReviewAgent": ReviewAgent(),
        }

    def run(self, raw_input: str) -> WorkflowState:
        state = WorkflowState(raw_input=raw_input)
        state.logs.append("=== Workflow 开始 (由 YAML 配置驱动) ===")

        # 找到起始节点
        current_node_id = self.config["nodes"][0]["id"]
        
        while current_node_id != "END":
            # 获取节点配置
            node_config = next((n for n in self.config["nodes"] if n["id"] == current_node_id), None)
            if not node_config:
                state.logs.append(f"错误：未找到节点 {current_node_id}")
                break

            # 如果节点被禁用（比如 enable_codegen: false），跳过并直接走向 next
            if node_config.get("enabled") is False:
                state.logs.append(f"--> 跳过节点: [{current_node_id}] (已禁用)")
                current_node_id = node_config.get("next", "END")
                continue

            agent_name = node_config["agent"]
            agent_instance = self.agents.get(agent_name)
            
            if not agent_instance:
                state.logs.append(f"错误：未注册 Agent {agent_name}")
                break

            # --- 执行 Agent ---
            print(f"--> 正在执行节点: [{current_node_id}] ({agent_name})...")
            state = agent_instance.run(state)

            # 如果发生致命错误，中断流程
            if state.errors:
                state.logs.append(f"=== 执行报错，流程终止: {state.errors[-1]} ===")
                break

            # --- 决定下一个节点 ---
            # 如果是 ReviewAgent，检查是否通过
            if current_node_id == "review" and not state.review.get("passed"):
                # 审查未通过，进入重试逻辑
                state.retry_count += 1
                if state.retry_count > self.max_retry:
                    state.logs.append(f"=== Workflow 终止：达到最大重试次数 {self.max_retry} ===")
                    state.errors.append("审查持续不通过，人工介入")
                    break
                
                next_node = node_config.get("on_fail", "END")
                state.logs.append(f"--- 审查未通过，触发 on_fail，回流至 [{next_node}] (第 {state.retry_count} 次重试) ---")
            else:
                # 正常通过，走向 next
                next_node = node_config.get("next", "END")
                if next_node == "END":
                    state.logs.append("=== Workflow 正常结束 ===")
            
            current_node_id = next_node

        return state