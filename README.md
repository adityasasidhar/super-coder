# Space

A powerful CLI coding assistant powered by Ollama, designed to be a local alternative to Claude Code.

## Features

## Features

- **Local Inference**: Runs entirely on your machine using Ollama.
- **Plan-Execute Workflow**: Creates detailed plans for complex tasks and asks for approval before execution.
- **Rich UI**:
    - **Live Spinners**: Visual feedback while the agent is thinking.
    - **Streaming Output**: Real-time text generation.
    - **Panel Layouts**: Beautifully formatted tool outputs and interactions.
    - **Enhanced Input**: Command history (Up/Down arrows) and multi-line support.
- **File Operations**: Read, write, edit, delete, copy, and move files.
- **Code Search**: Search for patterns within files or across directories.
- **Git Integration**: Manage version control directly from the assistant.
- **Package Management**: Install and list Python packages.
- **Command Execution**: Run shell commands safely.

## Prerequisites

1. **Ollama**: Install Ollama from [ollama.com](https://ollama.com).
2. **Models**: Pull the required models (default is `qwen3:4b`).
   ```bash
   ollama pull qwen3:4b
   ```

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd ollama-coder
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   # OR manually
   pip install ollama typer rich prompt_toolkit
   ```

## Usage

## Usage

Using the virtual environment:
```bash
.venv/bin/python -m ollama_coder.main start
```

Specify a different model:
```bash
.venv/bin/python -m ollama_coder.main start --model llama3
```

## 🧠 Workflow & Planning

### 1. Planning Mode (Complex Tasks)
For tasks that require multiple steps (like building a website or refactoring a module), the assistant follows a strict **Plan-Execute** workflow:

1.  **Analysis**: The agent analyzes your request to understand the scope.
2.  **Plan Generation**: It creates a detailed, step-by-step plan outlining exactly which files will be created or modified.
3.  **User Review**: The plan is presented to you. You can approve it (type `yes`, `proceed`) or provide feedback to refine it.
4.  **Execution**: Only after approval does the agent start creating files or running commands.

**Example Interaction:**
> **You**: "Create a personal portfolio website."
> **Agent**: "I'll build a portfolio with the following steps:
> 1. Create `index.html` with sections for About, Projects, and Contact.
> 2. Create `style.css` with a responsive grid layout.
> 3. Create `script.js` for smooth scrolling navigation.
> Does this plan look good?"
> **You**: "Yes, but add a dark mode toggle."
> **Agent**: "Understood. I've updated the plan to include dark mode styles and JS logic. Proceeding?"

### 2. Direct Mode (Simple Tasks)
For quick actions, the agent acts immediately without unnecessary dialogue:
> **You**: "Read the contents of main.py"
> **Agent**: [Reads and displays file content immediately]

## Available Tools

| Category | Tools |
|----------|-------|
| **File Ops** | `list_files`, `read_file`, `write_file`, `edit_file`, `delete_file`, `copy_file`, `move_file` |
| **Search** | `search_file`, `grep_search`, `find_files` |
| **Git** | `git_status`, `git_diff`, `git_log`, `git_add`, `git_commit` |
| **System** | `run_command`, `install_package`, `list_installed_packages` |

## Examples

**Create a new project:**
> "Create a directory called 'my-app' and add a main.py that prints hello world"

**Refactor code:**
> "Search for all print statements in src/ and replace them with logging"

**Git workflow:**
> "Check git status, add all changes, and commit with message 'Initial commit'"
