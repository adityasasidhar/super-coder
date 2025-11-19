from langchain.messages import HumanMessage
from langchain_core.messages import ChatMessage, SystemMessage
from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="gpt-oss:20b",
    reasoning=True
    )

messages = [
    SystemMessage("No markdown language or special characters"),
    ChatMessage(role="control", content="thinking"),
    HumanMessage("What is 3^3?"),
]

response = llm.invoke(messages)
print(f"THINKING: {response.additional_kwargs}")
print(f"RESPONSE: {response.content}")