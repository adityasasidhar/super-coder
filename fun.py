from langchain.messages import HumanMessage
from langchain_core.messages import ChatMessage, ToolMessage, SystemMessage
from langchain_ollama import ChatOllama
from langchain.tools import tool

@tool
def add(x: float, y: float) -> float:
    """Add two numbers together."""
    return x + y

@tool
def subtract(x: float, y: float) -> float:
    """Subtract two numbers."""
    return x - y

@tool
def multiply(x: float, y: float) -> float:
    """Multiply two numbers."""
    return x * y

@tool
def divide(x: float, y: float) -> float:
    """Divide two numbers."""
    return x / y

llm = ChatOllama(
    # Core
    model="qwen3:0.6b",
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

tools = [add]
llm_with_tools = llm.bind_tools(tools)

messages = [
    ChatMessage(role= "control", content= "thinking"),
    HumanMessage("Can you add 12345 and 67890?")
    ]

# First, let the model decide if it needs to use a tool
ai_msg = llm_with_tools.invoke(messages)
messages.append(ai_msg)

# Second, if a tool is called, execute it and return the result to the model
if ai_msg.tool_calls:
    for tool_call in ai_msg.tool_calls:
        # Here you would lookup the tool by name and execute it.
        # For this example, we know it's the 'add' tool.
        if tool_call["name"] == "add":
            result = add.invoke(tool_call["args"])
            tool_message = ToolMessage(content=str(result), tool_call_id=tool_call["id"])
            messages.append(tool_message)

# Get the final response from the model
response = llm_with_tools.invoke(messages)

print(response)

# Print everything in a structured way
print("="*80)
print("REASONING CONTENT:")
print("="*80)
if 'reasoning_content' in response.additional_kwargs:
    print(response.additional_kwargs['reasoning_content'])
else:
    print("No reasoning content available")

print("\n" + "="*80)
print("MAIN CONTENT/ANSWER:")
print("="*80)
print(response.content)

print("\n" + "="*80)
print("RESPONSE METADATA:")
print("="*80)
for key, value in response.response_metadata.items():
    print(f"{key}: {value}")

print("\n" + "="*80)
print("USAGE METADATA:")
print("="*80)
if hasattr(response, 'usage_metadata'):
    for key, value in response.usage_metadata.items():
        print(f"{key}: {value}")

# If you want to save to a file
with open('model_output.txt', 'w', encoding='utf-8') as f:
    f.write("REASONING:\n")
    f.write(response.additional_kwargs.get('reasoning_content', 'N/A'))
    f.write("\n\nANSWER:\n")
    f.write(response.content)