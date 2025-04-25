import json
import os
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from typing import List, Dict

load_dotenv()
console = Console()

class ChatManager:
    PERSONA_PATH = Path(__file__).parent.parent / "config" / "persona.json"
    
    def __init__(self, use_persona=False):
        self._configure_gemini()
        self.use_persona = use_persona
        self.persona_context = None
        self.chat_session = None
        self.history: List[Dict] = []
        
        if self.use_persona:
            self._load_persona()

    def _configure_gemini(self):
        GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
        if not GEMINI_API_KEY:
            console.print("[bold red]Error:[/] Missing API key")
            exit(1)
        genai.configure(api_key=GEMINI_API_KEY)

    def _load_persona(self):
        try:
            with open(self.PERSONA_PATH) as f:
                data = json.load(f)
            self.persona_context = (
                f"My name is {data['my_name']}. "
                f"Youre role is{data['role']}. "
                f"Your name is {data['name']}. "
                f"Your gender is {data['gender']}. "
                f"Your relationship status is {data['relationship']}. "
                f"{data['traits'][0]} assistant. "
                f"Style: {data['response_style']}"
            )
        except Exception as e:
            self.persona_context = "You are a helpful assistant."

    def _apply_persona(self, prompt: str) -> str:
        if self.use_persona and self.persona_context:
            if not hasattr(self, "_persona_applied"):
                prompt = f"{self.persona_context}\n{prompt}"
                self._persona_applied = True
        return prompt

    def start_chat(self):
        self.chat_session = genai.GenerativeModel('gemini-1.5-flash').start_chat()
        self.history = []

    def send_message(self, message: str) -> Markdown:
        if not self.chat_session:
            self.start_chat()
            
        message = self._apply_persona(message)
        response = self.chat_session.send_message(message)
        return Markdown(response.text)

    def single_query(self, question: str) -> Panel:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(question)
        return Panel(
            Markdown(response.text),
            title="[bold green]🤖 Response[/]",
            border_style="green",
            padding=(1, 2)
        )

