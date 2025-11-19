import json
from typing import List, Dict, Any
from .llm import ChatModel
from .tools import (
    list_files, read_file, write_file, edit_file, run_command,
    search_file, grep_search, find_files,
    delete_file, create_directory, move_file, copy_file, append_to_file, get_file_info,
    git_status, git_diff, git_log, git_commit, git_add,
    install_package, list_installed_packages
)
from .prompts import SYSTEM_PROMPT
from rich.console import Console

console = Console()

class Agent:
    def __init__(self, model_name: str = "qwen3:4b"):
        self.llm = ChatModel(model=model_name)
        self.messages: List[Dict[str, str]] = [{"role": "system", "content": SYSTEM_PROMPT}]
        self.tools = {
            "list_files": list_files,
            "read_file": read_file,
            "write_file": write_file,
            "edit_file": edit_file,
            "run_command": run_command,
            "search_file": search_file,
            "grep_search": grep_search,
            "find_files": find_files,
            "delete_file": delete_file,
            "create_directory": create_directory,
            "move_file": move_file,
            "copy_file": copy_file,
            "append_to_file": append_to_file,
            "get_file_info": get_file_info,
            "git_status": git_status,
            "git_diff": git_diff,
            "git_log": git_log,
            "git_commit": git_commit,
            "git_add": git_add,
            "install_package": install_package,
            "list_installed_packages": list_installed_packages,
        }
        self.tool_definitions = [
            {
                "type": "function",
                "function": {
                    "name": "list_files",
                    "description": "List files in a directory",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {"type": "string", "description": "The directory path"}
                        },
                        "required": ["path"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "read_file",
                    "description": "Read the content of a file",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {"type": "string", "description": "The file path"}
                        },
                        "required": ["path"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "write_file",
                    "description": "Write content to a file",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {"type": "string", "description": "The file path"},
                            "content": {"type": "string", "description": "The content to write"}
                        },
                        "required": ["path", "content"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "edit_file",
                    "description": "Replace text in a file",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {"type": "string", "description": "The file path"},
                            "old_text": {"type": "string", "description": "The text to replace"},
                            "new_text": {"type": "string", "description": "The new text"}
                        },
                        "required": ["path", "old_text", "new_text"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "run_command",
                    "description": "Run a shell command",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "command": {"type": "string", "description": "The command to run"}
                        },
                        "required": ["command"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "search_file",
                    "description": "Search for a pattern in a file",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {"type": "string", "description": "The file path"},
                            "pattern": {"type": "string", "description": "The pattern to search for"},
                            "use_regex": {"type": "boolean", "description": "Whether to use regex"}
                        },
                        "required": ["path", "pattern"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "grep_search",
                    "description": "Search for a pattern across multiple files in a directory",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "directory": {"type": "string", "description": "The directory to search"},
                            "pattern": {"type": "string", "description": "The pattern to search for"},
                            "file_pattern": {"type": "string", "description": "File pattern to match (e.g., '*.py')"}
                        },
                        "required": ["directory", "pattern"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "find_files",
                    "description": "Find files by name pattern",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "directory": {"type": "string", "description": "The directory to search"},
                            "name_pattern": {"type": "string", "description": "File name pattern (e.g., '*.py')"}
                        },
                        "required": ["directory", "name_pattern"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_file",
                    "description": "Delete a file",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {"type": "string", "description": "The file path to delete"}
                        },
                        "required": ["path"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "create_directory",
                    "description": "Create a new directory",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {"type": "string", "description": "The directory path to create"}
                        },
                        "required": ["path"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "move_file",
                    "description": "Move or rename a file",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "source": {"type": "string", "description": "Source file path"},
                            "destination": {"type": "string", "description": "Destination file path"}
                        },
                        "required": ["source", "destination"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "copy_file",
                    "description": "Copy a file",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "source": {"type": "string", "description": "Source file path"},
                            "destination": {"type": "string", "description": "Destination file path"}
                        },
                        "required": ["source", "destination"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "append_to_file",
                    "description": "Append content to a file",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {"type": "string", "description": "The file path"},
                            "content": {"type": "string", "description": "The content to append"}
                        },
                        "required": ["path", "content"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_file_info",
                    "description": "Get file metadata (size, modified time, etc.)",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {"type": "string", "description": "The file path"}
                        },
                        "required": ["path"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "git_status",
                    "description": "Get git status of the repository",
                    "parameters": {
                        "type": "object",
                        "properties": {}
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "git_diff",
                    "description": "Show git diff for uncommitted changes",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "file_path": {"type": "string", "description": "Optional file path to diff"}
                        }
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "git_log",
                    "description": "View git commit history",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "num_commits": {"type": "integer", "description": "Number of commits to show"}
                        }
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "git_commit",
                    "description": "Commit staged changes with a message",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "message": {"type": "string", "description": "Commit message"}
                        },
                        "required": ["message"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "git_add",
                    "description": "Stage a file for commit",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "file_path": {"type": "string", "description": "File path to stage"}
                        },
                        "required": ["file_path"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "install_package",
                    "description": "Install a Python package using pip",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "package_name": {"type": "string", "description": "Package name to install"}
                        },
                        "required": ["package_name"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_installed_packages",
                    "description": "List all installed Python packages",
                    "parameters": {
                        "type": "object",
                        "properties": {}
                    }
                }
            }
        ]

    def chat(self, user_input: str):
        self.messages.append({"role": "user", "content": user_input})
        
        while True:
            response = self.llm.generate(self.messages, tools=self.tool_definitions)
            
            if "error" in response:
                console.print(f"[red]Error:[/red] {response['error']}")
                break
                
            message = response["message"]
            self.messages.append(message)
            
            if not message.get("tool_calls"):
                console.print(f"[green]Assistant:[/green] {message['content']}")
                break
                
            for tool_call in message["tool_calls"]:
                function_name = tool_call["function"]["name"]
                arguments = tool_call["function"]["arguments"]
                
                console.print(f"[blue]Executing tool:[/blue] {function_name}")
                
                if function_name in self.tools:
                    result = self.tools[function_name](**arguments)
                    self.messages.append({
                        "role": "tool",
                        "content": str(result),
                        "name": function_name
                    })
                else:
                    self.messages.append({
                        "role": "tool",
                        "content": f"Error: Tool {function_name} not found",
                        "name": function_name
                    })

