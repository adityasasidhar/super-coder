import typer
from rich.console import Console
from rich.prompt import Prompt
from .agent import Agent

app = typer.Typer()
console = Console()

@app.callback()
def callback():
    """
    Ollama Coder CLI
    """

@app.command()
def start(model: str = "qwen3:4b"):
    """
    Start the Ollama Coder assistant.
    """
    console.print(f"[bold green]Starting Ollama Coder with model: {model}[/bold green]")
    agent = Agent(model_name=model)
    
    while True:
        try:
            user_input = Prompt.ask("[bold yellow]You[/bold yellow]")
            if user_input.lower() in ["exit", "quit"]:
                break
            
            agent.chat(user_input)
            
        except KeyboardInterrupt:
            console.print("\n[bold red]Exiting...[/bold red]")
            break
        except Exception as e:
            console.print(f"[red]Error:[/red] {e}")

if __name__ == "__main__":
    app()
