import json
from typing import List, Dict, Any
import ollama
from .llm import ChatModel
from .tools import (
    list_files, read_file, write_file, edit_file, run_command,
    search_file, grep_search, find_files,
    delete_file, create_directory, move_file, copy_file, append_to_file, get_file_info,
    git_status, git_diff, git_log, git_commit, git_add,
    install_package, list_installed_packages,
    check_syntax, lint_file, format_file,
    python_repl
)
from .prompts import SYSTEM_PROMPT
from rich.console import Console

console = Console()

class Agent:
    def __init__(self, model_name: str = "qwen3:4b"):
        self.model_name = model_name
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
            "check_syntax": check_syntax,
            "lint_file": lint_file,
            "format_file": format_file,
            "python_repl": python_repl,
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
            },
            {
                "type": "function",
                "function": {
                    "name": "check_syntax",
                    "description": "Check a Python file for syntax errors using ast.parse(). Fast validation.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {"type": "string", "description": "Path to the Python file to check"}
                        },
                        "required": ["path"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "lint_file",
                    "description": "Lint a Python file using ruff. Checks for style issues, bugs, and errors. Can auto-fix issues.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {"type": "string", "description": "Path to the Python file to lint"},
                            "fix": {"type": "boolean", "description": "If true, automatically fix issues where possible"}
                        },
                        "required": ["path"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "format_file",
                    "description": "Format a Python file using ruff. Applies PEP 8 and best practice formatting.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {"type": "string", "description": "Path to the Python file to format"}
                        },
                        "required": ["path"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "python_repl",
                    "description": "Execute Python code in a safe sandbox. Use this for calculations, data processing, or verifying logic. Captures stdout/stderr. Timeout: 5s.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "code": {"type": "string", "description": "The Python code to execute"}
                        },
                        "required": ["code"]
                    }
                }
            }
        ]

    def chat(self, user_input: str):
        self.messages.append({"role": "user", "content": user_input})
        
        from rich.live import Live
        from rich.spinner import Spinner
        from rich.panel import Panel
        from rich.markdown import Markdown
        from rich.console import Group
        
        while True:
            full_content = ""
            tool_calls = []
            
            # Streaming generation
            with Live(Spinner("dots", text="Thinking...", style="cyan"), refresh_per_second=10, console=console) as live:
                stream = self.llm.generate_stream(self.messages, tools=self.tool_definitions)
                
                for chunk in stream:
                    if "error" in chunk:
                        live.update(f"[red]Error:[/red] {chunk['error']}")
                        return

                    if "message" in chunk:
                        msg = chunk["message"]
                        
                        # Handle content
                        if "content" in msg and msg["content"]:
                            full_content += msg["content"]
                            live.update(Markdown(full_content))
                        
                        # Handle tool calls (Ollama usually sends them in the final chunk or distinct chunks)
                        if "tool_calls" in msg and msg["tool_calls"]:
                            tool_calls.extend(msg["tool_calls"])

            # Append assistant message to history
            assistant_msg = {"role": "assistant", "content": full_content}
            if tool_calls:
                assistant_msg["tool_calls"] = tool_calls
            self.messages.append(assistant_msg)

            # If no tool calls, we are done
            if not tool_calls:
                break
            
            # Execute tools
            for tool_call in tool_calls:
                function_name = tool_call["function"]["name"]
                arguments = tool_call["function"]["arguments"]
                
                # Visual feedback for tool execution
                console.print(Panel(
                    Group(
                        f"[bold blue]Tool:[/bold blue] {function_name}",
                        f"[dim]Args:[/dim] {json.dumps(arguments, indent=2)}"
                    ),
                    title="Executing Tool",
                    border_style="blue"
                ))
                
                with console.status(f"[bold blue]Running {function_name}...[/bold blue]", spinner="bouncingBar"):
                    if function_name in self.tools:
                        try:
                            result = self.tools[function_name](**arguments)
                            content = str(result)
                        except Exception as e:
                            content = f"Error executing tool: {str(e)}"
                    else:
                        content = f"Error: Tool {function_name} not found"

                # Show tool output
                console.print(Panel(
                    str(content)[:500] + ("..." if len(str(content)) > 500 else ""),
                    title=f"Output: {function_name}",
                    border_style="green" if "Error" not in str(content) else "red"
                ))

                self.messages.append({
                    "role": "tool",
                    "content": content,
                    "name": function_name
                })

    def get_current_model(self) -> str:
        """Get the name of the currently active model."""
        return self.model_name
    
    def switch_model(self, model_name: str) -> bool:
        """
        Switch to a different model.
        
        Args:
            model_name: Name of the model to switch to
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Test if the model exists by trying to use it
            self.llm = ChatModel(model=model_name)
            self.model_name = model_name
            console.print(f"[bold green]✓ Switched to model: {model_name}[/bold green]")
            return True
        except Exception as e:
            console.print(f"[bold red]✗ Failed to switch model:[/bold red] {str(e)}")
            return False
    
    def list_available_models(self) -> List[Dict[str, Any]]:
        """
        List all available Ollama models.
        
        Returns:
            List of model information dictionaries
        """
        try:
            models = ollama.list()
            return models.get('models', [])
        except Exception as e:
            console.print(f"[bold red]Error listing models:[/bold red] {str(e)}")
            return []


