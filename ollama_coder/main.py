import typer
from rich.console import Console
from .agent import Agent
from .ui import print_banner, startup_animation

app = typer.Typer()
console = Console()


@app.callback()
def callback():
    """
    Space CLI
    """


@app.command()
def start(model: str = "qwen3:4b"):
    """
    Start the Space assistant.
    """
    print_banner()
    startup_animation()

    console.print(f"[bold green]Starting Space with model: {model}[/bold green]")
    console.print("[dim]Type /help for available commands[/dim]\n")
    agent = Agent(model_name=model)

    from prompt_toolkit import PromptSession
    from prompt_toolkit.history import InMemoryHistory
    from prompt_toolkit.styles import Style

    session = PromptSession(history=InMemoryHistory())

    style = Style.from_dict(
        {
            "prompt": "bold yellow",
        }
    )

    while True:
        try:
            user_input = session.prompt([("class:prompt", "You: ")], style=style)

            if user_input.lower() in ["exit", "quit"]:
                break

            # Handle special commands
            if user_input.strip().startswith("/"):
                command_parts = user_input.strip().split(maxsplit=1)
                command = command_parts[0].lower()

                if command == "/models":
                    # List available models
                    from rich.table import Table

                    models = agent.list_available_models()

                    if models:
                        table = Table(
                            title="Available Ollama Models",
                            show_header=True,
                            header_style="bold magenta",
                        )
                        table.add_column("Model Name", style="cyan")
                        table.add_column("Size", style="green")
                        table.add_column("Modified", style="yellow")

                        for model in models:
                            name = model.get("name", "Unknown")
                            size = f"{model.get('size', 0) / (1024**3):.2f} GB"
                            modified = model.get("modified_at", "Unknown")
                            
                            # Convert datetime to string if needed
                            if hasattr(modified, 'strftime'):
                                modified = modified.strftime("%Y-%m-%d %H:%M")
                            elif modified != "Unknown":
                                modified = str(modified)
                            
                            # Mark current model
                            if name == agent.get_current_model():
                                name = f"→ {name} (current)"
                            table.add_row(name, size, modified)

                        console.print(table)
                    else:
                        console.print(
                            "[yellow]No models found or error occurred[/yellow]"
                        )
                    continue

                elif command == "/model":
                    # Switch model
                    if len(command_parts) < 2:
                        console.print("[yellow]Usage: /model <model_name>[/yellow]")
                    else:
                        new_model = command_parts[1].strip()
                        agent.switch_model(new_model)
                    continue

                elif command == "/current":
                    # Show current model
                    current = agent.get_current_model()
                    console.print(f"[bold cyan]Current model:[/bold cyan] {current}")
                    continue

                elif command == "/help":
                    # Show help for special commands
                    from rich.panel import Panel

                    help_text = """[bold]Special Commands:[/bold]
                                    [cyan]/models[/cyan]          - List all available Ollama models
                                    [cyan]/model <name>[/cyan]   - Switch to a different model
                                    [cyan]/current[/cyan]        - Show the currently active model
                                    [cyan]/help[/cyan]           - Show this help message
                                    [cyan]exit, quit[/cyan]      - Exit the application"""
                    console.print(Panel(help_text, title="Help", border_style="blue"))
                    continue

            agent.chat(user_input)

        except KeyboardInterrupt:
            console.print("\n[bold red]Exiting...[/bold red]")
            break
        except Exception as e:
            console.print(f"[red]Error:[/red] {e}")


if __name__ == "__main__":
    app()
