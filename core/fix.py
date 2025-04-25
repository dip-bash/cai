import os
import subprocess
import google.generativeai as genai
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Confirm

load_dotenv()
console = Console()

class ErrorFixer:
    def __init__(self):
        self.gemini = genai.GenerativeModel('gemini-1.5-flash')
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    
    def get_last_command(self):
        try:
            # Get second-to-last command from Fish history
            cmd = "history | head -n 2 | tail -n 1"
            result = subprocess.run(
                ["fish", "-c", cmd],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            console.print(f"[yellow]History error:[/] {e.stderr}")
            return None
        except Exception as e:
            console.print(f"[yellow]Error:[/] {str(e)}")
            return None

    def analyze_error(self, command: str):
        if not command:
            console.print("[red]Error:[/] No command to analyze")
            return

        console.print(f"\n🔧 Analyzing: [bold yellow]{command}[/]")
        
        # Execute command safely
        process = subprocess.Popen(
            command, 
            shell=True,
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        stdout, stderr = process.communicate()
        
        if process.returncode == 0:
            console.print("[green]✓ Command succeeded! No errors found[/]")
            return

        # Analyze error with AI
        prompt = f"Fish shell command failed: {command}\nError:\n{stderr}\nExplain why this error occurred and suggest fixes and make it shorter. Answer format will be -> reason: \n fix:"
        response = self.gemini.generate_content(prompt)
        
        console.print("\n[red]🚨 Error Analysis:[/]")
        console.print(Markdown(response.text))
        
        console.print("\n[bold]Original error:[/]")
        console.print(Markdown(f"```\n{stderr}\n```"))

    def safe_execute(self):
        last_cmd = self.get_last_command()
        
        if not last_cmd or "cai --fix" in last_cmd:
            console.print("[red]Error:[/] No recent command found")
            console.print("Usage steps:")
            console.print("1. Run a command that fails")
            console.print("2. Immediately run: python3 cai.py --fix")
            return

        console.print(f"\nDetected command: [bold yellow]{last_cmd}[/]")
        if Confirm.ask("\n⚠️  Re-run to analyze errors?", default=False):
            self.analyze_error(last_cmd)
        else:
            console.print("[bold]Cancelled[/]")
