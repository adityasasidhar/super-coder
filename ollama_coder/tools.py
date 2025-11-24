import os
import subprocess
import re
import shutil
from pathlib import Path


def list_files(path: str = ".") -> str:
    """List files in a directory."""
    try:
        files = os.listdir(path)
        return "\n".join(files)
    except Exception as e:
        return f"Error listing files: {e}"


def read_file(path: str) -> str:
    """Read the content of a file."""
    try:
        with open(path, "r") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e}"


def write_file(path: str, content: str) -> str:
    """Write content to a file."""
    try:
        with open(path, "w") as f:
            f.write(content)
        return f"Successfully wrote to {path}"
    except Exception as e:
        return f"Error writing file: {e}"


def edit_file(path: str, old_text: str, new_text: str) -> str:
    """Replace old_text with new_text in a file."""
    try:
        with open(path, "r") as f:
            content = f.read()

        if old_text not in content:
            return "Error: old_text not found in file."

        new_content = content.replace(old_text, new_text)

        with open(path, "w") as f:
            f.write(new_content)

        return f"Successfully edited {path}"
    except Exception as e:
        return f"Error editing file: {e}"


def run_command(command: str) -> str:
    """Run a shell command."""
    try:
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, timeout=60
        )
        output = result.stdout
        if result.stderr:
            output += f"\nStderr: {result.stderr}"
        return output
    except Exception as e:
        return f"Error running command: {e}"


# Search and Analysis Tools
def search_file(path: str, pattern: str, use_regex: bool = False) -> str:
    """Search for a pattern in a file."""
    try:
        with open(path, "r") as f:
            content = f.read()

        lines = content.split("\n")
        matches = []

        for i, line in enumerate(lines, 1):
            if use_regex:
                if re.search(pattern, line):
                    matches.append(f"Line {i}: {line}")
            else:
                if pattern in line:
                    matches.append(f"Line {i}: {line}")

        if matches:
            return "\n".join(matches)
        else:
            return f"No matches found for '{pattern}' in {path}"
    except Exception as e:
        return f"Error searching file: {e}"


def grep_search(directory: str, pattern: str, file_pattern: str = "*") -> str:
    """Search for a pattern across multiple files in a directory."""
    try:
        matches = []
        search_path = Path(directory)

        for file_path in search_path.rglob(file_pattern):
            if file_path.is_file():
                try:
                    with open(file_path, "r") as f:
                        for i, line in enumerate(f, 1):
                            if pattern in line:
                                matches.append(f"{file_path}:{i}: {line.strip()}")
                except:
                    continue

        if matches:
            return "\n".join(matches[:50])  # Limit to 50 matches
        else:
            return f"No matches found for '{pattern}' in {directory}"
    except Exception as e:
        return f"Error searching directory: {e}"


def find_files(directory: str, name_pattern: str) -> str:
    """Find files by name pattern."""
    try:
        search_path = Path(directory)
        matches = []

        for file_path in search_path.rglob(name_pattern):
            matches.append(str(file_path))

        if matches:
            return "\n".join(matches)
        else:
            return f"No files found matching '{name_pattern}' in {directory}"
    except Exception as e:
        return f"Error finding files: {e}"


# Advanced File Operations
def delete_file(path: str) -> str:
    """Delete a file."""
    try:
        os.remove(path)
        return f"Successfully deleted {path}"
    except Exception as e:
        return f"Error deleting file: {e}"


def create_directory(path: str) -> str:
    """Create a new directory."""
    try:
        os.makedirs(path, exist_ok=True)
        return f"Successfully created directory {path}"
    except Exception as e:
        return f"Error creating directory: {e}"


def move_file(source: str, destination: str) -> str:
    """Move or rename a file."""
    try:
        shutil.move(source, destination)
        return f"Successfully moved {source} to {destination}"
    except Exception as e:
        return f"Error moving file: {e}"


def copy_file(source: str, destination: str) -> str:
    """Copy a file."""
    try:
        shutil.copy2(source, destination)
        return f"Successfully copied {source} to {destination}"
    except Exception as e:
        return f"Error copying file: {e}"


def append_to_file(path: str, content: str) -> str:
    """Append content to a file."""
    try:
        with open(path, "a") as f:
            f.write(content)
        return f"Successfully appended to {path}"
    except Exception as e:
        return f"Error appending to file: {e}"


def get_file_info(path: str) -> str:
    """Get file metadata."""
    try:
        stat = os.stat(path)
        info = f"Path: {path}\n"
        info += f"Size: {stat.st_size} bytes\n"
        info += f"Modified: {stat.st_mtime}\n"
        info += f"Is Directory: {os.path.isdir(path)}\n"
        return info
    except Exception as e:
        return f"Error getting file info: {e}"


# Git Integration
def git_status() -> str:
    """Get git status."""
    return run_command("git status")


def git_diff(file_path: str = "") -> str:
    """Show git diff."""
    if file_path:
        return run_command(f"git diff {file_path}")
    return run_command("git diff")


def git_log(num_commits: int = 10) -> str:
    """View git commit history."""
    return run_command(f"git log -n {num_commits} --oneline")


def git_commit(message: str) -> str:
    """Commit staged changes."""
    return run_command(f'git commit -m "{message}"')


def git_add(file_path: str) -> str:
    """Stage a file for commit."""
    return run_command(f"git add {file_path}")


# Package Management
def install_package(package_name: str) -> str:
    """Install a Python package using pip."""
    return run_command(f"pip install {package_name}")


def list_installed_packages() -> str:
    """List installed Python packages."""
    return run_command("pip list")


# Code Quality Tools
def check_syntax(path: str) -> str:
    """
    Check Python file for syntax errors using ast.parse().
    Fast validation without external dependencies.
    """
    try:
        with open(path, "r") as f:
            code = f.read()

        import ast

        try:
            ast.parse(code)
            return f"✓ Syntax check passed for {path}"
        except SyntaxError as e:
            return f"✗ Syntax error in {path}:\n  Line {e.lineno}: {e.msg}\n  {e.text}"
    except Exception as e:
        return f"Error checking syntax: {e}"


def lint_file(path: str, fix: bool = False) -> str:
    """
    Lint a Python file using ruff.
    Checks for style issues, bugs, and errors.

    Args:
        path: Path to the Python file
        fix: If True, automatically fix issues where possible
    """
    try:
        if not os.path.exists(path):
            return f"Error: File {path} does not exist"

        # Run ruff check
        cmd = f"ruff check {path}"
        if fix:
            cmd += " --fix"

        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=30
        )

        output = result.stdout
        if result.stderr:
            output += f"\n{result.stderr}"

        if result.returncode == 0:
            if fix:
                return f"✓ Linting passed and fixes applied for {path}\n{output}"
            else:
                return f"✓ No linting issues found in {path}"
        else:
            return f"Linting issues found in {path}:\n{output}"
    except Exception as e:
        return f"Error linting file: {e}"


def format_file(path: str) -> str:
    """
    Format a Python file using ruff.
    Applies PEP 8 and best practice formatting.
    """
    try:
        if not os.path.exists(path):
            return f"Error: File {path} does not exist"

        # Run ruff format
        result = subprocess.run(
            f"ruff format {path}",
            shell=True,
            capture_output=True,
            text=True,
            timeout=30,
        )

        if result.returncode == 0:
            return f"✓ Successfully formatted {path}"
        else:
            error_msg = result.stderr or result.stdout
            return f"Error formatting {path}:\n{error_msg}"
    except Exception as e:
        return f"Error formatting file: {e}"


# Code Execution Sandbox
def python_repl(code: str) -> str:
    """
    Execute Python code in a safe sandbox environment.
    Captures stdout/stderr and enforces a timeout.
    """
    import io
    import contextlib
    import multiprocessing

    def _exec_code(code_str, queue):
        # Capture stdout/stderr
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()

        try:
            with (
                contextlib.redirect_stdout(stdout_capture),
                contextlib.redirect_stderr(stderr_capture),
            ):
                # Create a restricted globals dictionary if needed,
                # but for now we trust the agent but sandbox the process
                exec(code_str, {"__name__": "__main__"})

            queue.put(
                {
                    "stdout": stdout_capture.getvalue(),
                    "stderr": stderr_capture.getvalue(),
                    "success": True,
                }
            )
        except Exception:
            import traceback

            queue.put(
                {
                    "stdout": stdout_capture.getvalue(),
                    "stderr": traceback.format_exc(),
                    "success": False,
                }
            )

    # Use multiprocessing to allow timeout and isolation
    queue = multiprocessing.Queue()
    process = multiprocessing.Process(target=_exec_code, args=(code, queue))

    try:
        process.start()
        process.join(timeout=5)  # 5 second timeout

        if process.is_alive():
            process.terminate()
            process.join()
            return "Error: Code execution timed out (limit: 5 seconds)"

        if not queue.empty():
            result = queue.get()
            output = ""
            if result["stdout"]:
                output += f"Output:\n{result['stdout']}\n"
            if result["stderr"]:
                output += f"Errors:\n{result['stderr']}\n"

            if not output:
                output = "Code executed successfully (no output)"

            return output
        else:
            return "Error: Process finished but returned no result"

    except Exception as e:
        return f"Error executing code: {e}"
