import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from datetime import datetime
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.markdown import Markdown
from typing import List, Dict

load_dotenv()
console = Console()

CONTEXT_FILE = os.path.join(os.path.dirname(__file__), '..', 'cache', 'context', 'last_context.json')

class ChatManager:
    def __init__(self):
        self._configure_gemini()
        self.chat_session = None
        self.history: List[Dict] = []
        
    def _configure_gemini(self):
        GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
        if not GEMINI_API_KEY:
            console.print("[bold red]Error:[/] Missing GEMINI_API_KEY in .env file")
            exit(1)
        genai.configure(api_key=GEMINI_API_KEY)
        
    def start_chat(self):
        """Initialize a new chat session"""
        self.chat_session = genai.GenerativeModel('gemini-1.5-flash').start_chat()
        self.history = []
        
    def send_message(self, message: str) -> Markdown:
        """Send message to AI and return formatted response"""
        if not self.chat_session:
            self.start_chat()
            
        response = self.chat_session.send_message(message)
        self._update_history(prompt=message, response=response.text)
        return Markdown(response.text)

    def contextual_chat(self, question: str) -> Markdown:  # Fixed parameter definition
        """Chat with context from previous analysis"""
        try:
            os.makedirs(os.path.dirname(CONTEXT_FILE), exist_ok=True)
            if not os.path.exists(CONTEXT_FILE):
                return Markdown("No analysis context found. First analyze some content using pipe input.")
            
            with open(CONTEXT_FILE, 'r') as f:
                context = json.load(f)
            
            prompt = f"Context:\n{context['analysis']}\n\nQuestion: {question}"
            return self.send_message(prompt)  # Properly using self
        except Exception as e:
            return Markdown(f"Error loading context: {str(e)}")

    def _update_history(self, prompt: str, response: str):
        """Store conversation context"""
        self.history.append({
            'user': prompt,
            'ai': response,
            'timestamp': datetime.now().isoformat()
        })