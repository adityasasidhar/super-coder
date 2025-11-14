import os
import json
import subprocess
from typing import TypedDict, Annotated, Sequence
import operator

from langchain.tools import tool
from langchain_core.messages import BaseMessage, HumanMessage, ToolMessage
from langchain_ollama import ChatOllama
from duckduckgo_search import DDGS
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode


@tool
def search_web(query: str) -> str:
    """Searches the web using DuckDuckGo for the given query and returns the top results."""
    try:
        with DDGS() as ddgs:
            results = [r for r in ddgs.text(query, max_results=5)]
            return json.dumps(results) if results else "No results found."
    except Exception as e:
        return f"Error during web search: {e}"


@tool
def execute_python_code(code: str) -> str:
    """
    Executes a string of Python code in a sandboxed subprocess.
    Returns the combined stdout and stderr.
    The code should be a complete script. Use print() to generate output.
    """
    try:
        result = subprocess.run(
            ['/usr/bin/python3', '-c', code],
            capture_output=True,
            text=True,
            timeout=30,
            check=True
        )
        return f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        return f"EXECUTION FAILED:\nSTDOUT:\n{e.stdout}\nSTDERR:\n{e.stderr}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"


@tool
def read_file(file_path: str) -> str:
    """Reads the content of a file specified by file_path."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e}"


@tool
def write_file(file_path: str, content: str) -> str:
    """Writes the given content to a file specified by file_path. Overwrites the file if it exists."""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Successfully wrote to {file_path}"
    except Exception as e:
        return f"Error writing to file: {e}"


@tool
def list_files(directory: str = ".") -> str:
    """Lists all files and directories in a given directory."""
    try:
        return "\n".join(os.listdir(directory))
    except Exception as e:
        return f"Error listing files: {e}"


@tool
def execute_shell_command(command: str) -> str:
    """
    Executes a shell command and returns its output.
    DANGER: This tool allows arbitrary command execution. Use with extreme caution.
    Only run commands you understand and are sure are safe.
    Good examples: `ls -l`, `pwd`. Bad examples: `rm -rf /`.
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        return f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        return f"COMMAND FAILED:\nSTDOUT:\n{e.stdout}\nSTDERR:\n{e.stderr}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"


llm = ChatOllama(
    # Core
    model="qwen3:1.7b",
    temperature=0.7,
    top_p=0.95,
    num_predict=12000,
    num_ctx=16000,
    top_k=40,
    repeat_penalty=1.1,
    seed=42,
    reasoning=True,
    validate_model_on_init=True,
    verbose=True,
)

if __name__ == "__main__":
    tools = [
        search_web,
        execute_python_code,
        read_file,
        write_file,
        list_files,
        execute_shell_command,
    ]
    llm_with_tools = llm.bind_tools(tools)

    # 1. Define the Agent State
    class AgentState(TypedDict):
        messages: Annotated[Sequence[BaseMessage], operator.add]

    # 2. Define the Graph Nodes
    def should_continue(state: AgentState) -> str:
        """Decide whether to continue or end the loop."""
        last_message = state["messages"][-1]
        if not last_message.tool_calls:
            return "end"
        return "continue"

    def call_model(state: AgentState) -> dict:
        """The 'agent' node: calls the LLM to decide the next action."""
        response = llm_with_tools.invoke(state["messages"])
        return {"messages": [response]}

    # 3. Define the Graph
    workflow = StateGraph(AgentState)

    # Add the nodes
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", ToolNode(tools))

    # Set the entrypoint
    workflow.set_entry_point("agent")

    # Add the conditional edges
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "continue": "tools",
            "end": END,
        },
    )

    # Add the normal edge
    workflow.add_edge("tools", "agent")

    # Compile the graph into a runnable app
    app = workflow.compile()

    # 4. Run the agent in an interactive loop
    system_message = (
        "You are a world-class software engineering assistant. Your goal is to help the user by breaking down their request "
        "into a step-by-step plan and executing it using the tools at your disposal.\n\n"
        "**Core Workflow:**\n"
        "1.  **Analyze & Plan**: Carefully analyze the user's request and create a clear, step-by-step plan. "
        "Think about which tools are best for each step.\n"
        "2.  **Execute with Tools**: Use the available tools to execute your plan. You can search the web, read/write files, and execute code or shell commands.\n"
        "3.  **Observe & Refine**: After each tool use, observe the output and adjust your plan if necessary. If something fails, try to understand why and correct your approach.\n"
        "4.  **Final Answer**: Once all steps are complete, provide a comprehensive, final answer to the user, summarizing what you did and the outcome.\n\n"
        "**Safety Guidelines:**\n"
        "- Before modifying a file, always read it first to understand its contents.\n"
        "- Use the `execute_shell_command` tool with extreme caution. Double-check any commands before running them."
    )

    print("🚀 Cursor Agent Initialized. I'm ready to assist you.")
    print("Type 'exit' or 'quit' to end the session.")

    thread = {"configurable": {"thread_id": "main-thread"}}

    while True:
        user_input = input("\n> ")
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting agent session. Goodbye!")
            break

        # Stream the events from the graph to see the agent's process
        events = app.stream(
            {"messages": [HumanMessage(content=user_input)]},
            config=thread,
        )
        
        print("\n🤖 Agent is thinking...", flush=True)
        has_printed_reasoning_header = False
        has_printed_answer_header = False

        for event in events:
            if "tools" in event:
                if not has_printed_reasoning_header and not has_printed_answer_header:
                    print("\n", flush=True)  # Newline before tool calls
                tool_calls = event["tools"]["messages"][0].tool_calls
                for tc in tool_calls:
                    print(f"   - Calling tool `{tc['name']}` with args: {tc['args']}", flush=True)

            if "agent" in event:
                message_chunk = event["agent"]["messages"][0]

                # Handle and stream reasoning content if available
                if reasoning_content := message_chunk.additional_kwargs.get("reasoning_content"):
                    if not has_printed_reasoning_header:
                        print("\n🤔 Reasoning:", flush=True)
                        has_printed_reasoning_header = True
                    print(reasoning_content, end="", flush=True)

                # Handle and stream the final answer content
                if message_chunk.content:
                    if not has_printed_answer_header:
                        # Add a newline if reasoning was printed, for better separation
                        if has_printed_reasoning_header:
                            print("\n")
                        print("\n✅ Final Answer:", flush=True)
                        has_printed_answer_header = True
                    print(message_chunk.content, end="", flush=True)

        # Add a final newline for clean formatting
        print("\n")