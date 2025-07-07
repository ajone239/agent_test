from agent_test.agent import Agent
from agent_test.tools.math_tool import CalculatorTool
from agent_test.tools.time_tool import TimeTool


if __name__ == "__main__":
    agent = Agent()
    agent.add_tool(TimeTool())
    agent.add_tool(CalculatorTool())
    agent.run()
