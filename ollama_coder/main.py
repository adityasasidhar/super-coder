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
    
    from prompt_toolkit import PromptSession
    from prompt_toolkit.history import InMemoryHistory
    from prompt_toolkit.styles import Style

    session = PromptSession(history=InMemoryHistory())
    
    style = Style.from_dict({
        'prompt': 'bold yellow',
    })

    while True:
        try:
            user_input = session.prompt([('class:prompt', 'You: ')], style=style)
            
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
