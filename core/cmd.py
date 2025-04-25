import os
import re
import json
import hashlib
import datetime
from rich.text import Text
from typing import Optional, Dict
from rich.console import Console
from rich.markdown import Markdown
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
console = Console()

# Configuration
CACHE_DIR = './cache/man'
CONTEXT_FILE = './cache/context/last_context.json'
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    console.print("[bold red]Error:[/] Missing GEMINI_API_KEY in .env file")
    exit(1)

genai.configure(api_key=GEMINI_API_KEY)

def is_man_page(text: str) -> bool:
    return any(section in text for section in ['NAME\n', 'SYNOPSIS\n', 'DESCRIPTION\n'])

def detect_input_type(text: str) -> str:
    return 'man' if is_man_page(text) else 'cmd'

def get_command_name(text: str) -> str:
    if is_man_page(text):
        first_line = text.strip().split('\n')[0]
        match = re.match(r'^([A-Za-z0-9-]+)\([0-9]+\)', first_line)
        return match.group(1).lower() if match else 'unknown'
    else:
        return hashlib.md5(text.encode()).hexdigest()[:8]

def save_context(context: Dict):
    os.makedirs(os.path.dirname(CONTEXT_FILE), exist_ok=True)
    with open(CONTEXT_FILE, 'w') as f:
        json.dump(context, f)

def analyze_content(text: str, context_type: str) -> str:
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    if context_type == 'man':
        prompt = """Analyze this man page and generate top 5-10 commands/examples.
        Format as: Command: [command]\nExample: [example]\nKeep concise."""
    else:
        prompt = """Analyze this command output. Explain its purpose, 
        highlight key information, and suggest potential next steps."""

    response = model.generate_content([prompt, text])
    return response.text

def man_explain(text: str):
    context_type = detect_input_type(text)
    cmd = get_command_name(text)
    
    # Save context for potential chat
    context = {
        'type': context_type,
        'content': text,
        'analysis': analyze_content(text, context_type),
        'timestamp': datetime.datetime.now().isoformat()
    }
    save_context(context)

    console.print(Text("\n🔍 Analysis Results:", style="bold cyan"))
    console.print(Markdown(context['analysis']))
