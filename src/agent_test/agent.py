import json
import re

from .tools.tools import Tool

from openai import OpenAI


class Agent:
    def __init__(self):
        self.tools = []
        self.memory = []
        self.max_memory = 10
        self.client = OpenAI()

    def add_tool(self, tool: Tool):
        self.tools.append(tool)

    def json_parser(self, input_string):
        try:
            # Remove code block markers if present
            code_block_pattern = r"```json\s*(\{.*?\})\s*```"
            match = re.search(code_block_pattern, input_string, re.DOTALL)
            if match:
                json_str = match.group(1)
            else:
                # If no code block, try to match any JSON object in the string
                json_object_pattern = r"(\{.*?\})"
                match = re.search(json_object_pattern, input_string, re.DOTALL)
                if match:
                    json_str = match.group(1)
                else:
                    raise ValueError(
                        "No JSON object found in the LLM response.")
            # Parse the JSON string
            json_dict = json.loads(json_str)
            if isinstance(json_dict, dict):
                return json_dict
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
        print(f"LLM response was: {input_string}")
        raise ValueError("Invalid JSON response from LLM.")

    def process_input(self, user_input):
        self.memory.append(f"User: {user_input}")
        self.memory = self.memory[-self.max_memory:]

        context = "\n".join(self.memory)
        tool_descriptions = "\n".join(
            [f"- {tool.name()}: {tool.description()}" for tool in self.tools]
        )

        prompt = f"""You are an assistant that helps process user requests by determining the appropriate action and arguments based on the user's input.
                Context:
                {context}

                Available tools:
                {tool_descriptions}

                Instructions:
                - Decide whether to use a tool or respond directly to the user.
                - If you choose to use a tool, output a JSON object with "action" and "args" fields.
                - If you choose to respond directly, set "action": "respond_to_user" and provide your response in "args".
                - **Important**: Provide the response **only** as a valid JSON object. Do not include any additional text or formatting.
                - Ensure that the JSON is properly formatted without any syntax errors.

                Response Format:
                {{"action": "<action_name>", "args": "<arguments>"}}

                Example Responses:
                - Using a tool: {{"action": "Time Tool", "args": "Asia/Tokyo"}}
                - Responding directly: {{"action": "respond_to_user", "args": "I'm here to help!"}}

                User Input: "{user_input}"
                """

        response = self.query_llm(prompt)
        self.memory.append(f"Agent: {response}")

        response_dict = self.json_parser(response)

        # Handle the tool or response
        if response_dict["action"] == "respond_to_user":
            return response_dict["args"]
        else:
            # Find and use the appropriate tool
            for tool in self.tools:
                if tool.name().lower() == response_dict["action"].lower():
                    return tool.use(response_dict["args"])

        return "I'm sorry, I couldn't process your request."

    def query_llm(self, prompt):

        response = self.client.responses.create(
            model="o4-mini",
            input=prompt,
        )

        return response.output_text

    def run(self):
        print("LLM Agent: Hello! How can I assist you today?")
        while True:
            user_input = input("\nYou: ").strip()
            if user_input.lower() in ["exit", "bye", "close"]:
                print("LLM Agent: See you later!")
                break
            response = self.process_input(user_input)
            print(f"\nLLM Agent: {response}")
