import sys
import argparse
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.markdown import Markdown
from core.cmd import man_explain
from core.query import ChatManager
from core.fix import ErrorFixer

console = Console()

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="💻 AI Terminal Assistant", 
        add_help=False,
        usage="cai.py [-h] [-c] [--fix] [query]"
    )
    parser.add_argument('-h', '--help', action='store_true',
                      help="Show this help message")
    parser.add_argument('-c', '--chat', action='store_true',
                      help="Interactive chat about current analysis")
    parser.add_argument('--fix', action='store_true',
                      help="Analyze and fix last command's error")
    parser.add_argument('query', nargs='?', 
                      help="Direct question for immediate response")
    return parser.parse_args()

def show_help():
    """Display formatted help message"""
    help_text = """\n
    [bold cyan]Usage:[/]
      cai               # Interactive chat with persona
      cai [question]    # Direct question (no persona)
      man cmd | cai     # Explain man page
      cmd | cai -c      # Analyze command output and chat
      cai --fix         # Fix last command error

    [bold yellow]Options:[/]
      -h, --help     Show this help message
      -c, --chat     Interactive chat about analysis
      --fix          Diagnose and fix command errors
    """
    console.print(Panel.fit(help_text, 
                          title="[bold green]📖 CAI Help[/]", 
                          border_style="blue",
                          padding=(1, 2)))
    

def general_chat():
    chat = ChatManager(use_persona=True)
    console.print(
        Panel.fit("[bold green]💬 CAI Chat[/] (type 'exit' to quit)", 
                border_style="green")
    )
    
    while True:
        try:
            user_input = Prompt.ask("[bold yellow]me[/]").strip()
            if user_input.lower() in ('exit', 'quit'):
                break
                
            response = chat.send_message(user_input)
            console.print("[bold green]cai:[/]")
            console.print(response)
        except (KeyboardInterrupt, EOFError):
            console.print("\n[bold red]Exiting chat...[/]")
            break

def handle_piped_input(args):
    input_text = sys.stdin.read()
    if not input_text:
        console.print("[bold red]Error:[/] No input received")
        return
    
    man_explain(input_text)
    
    if args.chat:
        # Switch to terminal input for chat
        sys.stdin = open('/dev/tty')
        analysis_chat()

def analysis_chat():
    chat = ChatManager(use_persona=False)
    console.print(
        Panel.fit("[bold green]💬 Analysis Mode[/] (type 'exit' to quit)", 
                border_style="green")
    )
    
    try:
        while True:
            try:
                user_input = Prompt.ask("[bold yellow]me[/]").strip()
                if user_input.lower() in ('exit', 'quit'):
                    break
                    
                response = chat.send_message(user_input)
                console.print("[bold green]cai:[/]")
                console.print(response)
            except EOFError:
                console.print("\n[bold yellow]Input closed[/]")
                break
    except KeyboardInterrupt:
        console.print("\n[bold red]Exiting...[/]")

def main():
    args = parse_arguments()

    if args.help:
        show_help()
        return

    if args.fix:
        ErrorFixer().safe_execute()
        return

    if args.query:
        try:
            chat = ChatManager(use_persona=False)
            response = chat.single_query(args.query)
            console.print(response)
        except Exception as e:
            console.print(f"[bold red]Error:[/] {str(e)}")
        return

    if not sys.stdin.isatty():
        handle_piped_input(args)
    else:
        general_chat()

if __name__ == "__main__":
    try:
        main()
    except argparse.ArgumentError:
        show_help()
