# Space: Local AI Coding Assistant

Space is a powerful, fully local CLI coding assistant powered by Ollama. It is designed to be a private, secure, and capable alternative to cloud-based coding assistants, offering a rich terminal user interface and a wide range of file and system operations.

## 🚀 Features

-   **100% Local Inference**: Runs entirely on your machine using Ollama models (e.g., Qwen, Llama 3). No data leaves your system.
-   **Plan-Execute Workflow**: For complex tasks, Space creates detailed implementation plans and requests user approval before making changes.
-   **Rich Terminal UI**:
    -   **Live Spinners**: Visual feedback during AI processing.
    -   **Streaming Output**: Real-time response generation.
    -   **Markdown Rendering**: Beautifully formatted text and code in the terminal.
    -   **Panel Layouts**: Organized output for tools and messages.
-   **Comprehensive Toolset**:
    -   **File Operations**: Read, write, edit, delete, copy, move, and append to files.
    -   **Search**: Regex search within files, grep across directories, and file finding.
    -   **Git Integration**: Check status, view diffs, log history, stage files, and commit changes.
    -   **Code Quality**: Syntax checking, linting (Ruff), and auto-formatting.
    -   **System**: Run shell commands and manage Python packages.
    -   **Sandbox**: Execute Python code in a safe, isolated environment.

## 📋 Prerequisites

1.  **Ollama**: Install Ollama from [ollama.com](https://ollama.com).
2.  **Python 3.10+**: Ensure you have a recent version of Python installed.
3.  **Models**: Pull a coding-capable model. `qwen2.5-coder` or `qwen3` are recommended.
    ```bash
    ollama pull qwen2.5-coder:7b
    ```

## 🛠️ Installation

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd space-coder
    ```

2.  **Create a virtual environment**:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## 💻 Usage

Start the assistant using the CLI entry point:

```bash
python -m ollama_coder.main start
```

### Command Line Options

-   `--model`: Specify the Ollama model to use (default: `qwen3:4b`).
    ```bash
    python -m ollama_coder.main start --model llama3
    ```

### Special Slash Commands

Inside the chat interface, you can use these commands:

-   `/models`: List all available Ollama models on your system.
-   `/model <name>`: Switch to a different model instantly.
-   `/current`: Show the currently active model.
-   `/help`: Display the help menu.
-   `exit` or `quit`: Close the application.

## 🧠 Workflows

### 1. Planning Mode (Complex Tasks)
When you ask for a complex change (e.g., "Refactor the database module" or "Create a new web app"), Space enters **Planning Mode**:
1.  **Analyzes** the request.
2.  **Generates** a step-by-step implementation plan.
3.  **Asks** for your approval.
4.  **Executes** the plan only after you say "yes".

### 2. Direct Mode (Simple Tasks)
For straightforward requests, Space acts immediately:
-   "Read main.py" -> Displays content.
-   "Run ls -la" -> Shows directory listing.

## 🧰 Available Tools

| Category | Tool Name | Description |
| :--- | :--- | :--- |
| **File Ops** | `list_files` | List directory contents. |
| | `read_file` | Read file content. |
| | `write_file` | Write content to a file (creates dirs). |
| | `edit_file` | Replace exact text block in a file. |
| | `delete_file` | Remove a file. |
| | `copy_file` | Copy a file. |
| | `move_file` | Move or rename a file. |
| | `append_to_file` | Append text to a file. |
| | `get_file_info` | Get size and modification time. |
| **Search** | `search_file` | Search text/regex in a single file. |
| | `grep_search` | Search pattern across a directory. |
| | `find_files` | Find files by filename pattern. |
| **Git** | `git_status` | Show working tree status. |
| | `git_diff` | Show changes. |
| | `git_log` | View commit history. |
| | `git_add` | Stage files. |
| | `git_commit` | Commit changes. |
| **Code Quality** | `check_syntax` | Fast Python syntax validation. |
| | `lint_file` | Lint with Ruff (supports auto-fix). |
| | `format_file` | Format code with Ruff. |
| **System** | `run_command` | Execute shell commands (bash). |
| | `install_package` | Install pip packages. |
| | `list_installed_packages` | List pip packages. |
| **Sandbox** | `python_repl` | Execute Python code in a safe sandbox. |

## 📝 Examples

**Create a new project:**
> "Create a directory called 'my-app', add a main.py that prints hello world, and a requirements.txt."

**Refactor code:**
> "Search for all print statements in src/ and replace them with logging calls. Then format the files."

**Git workflow:**
> "Check git status, add all changes, and commit with message 'Initial feature implementation'."

**Data Analysis:**
> "Read data.csv and use python code to calculate the average of the 'score' column."
