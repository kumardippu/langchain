#!/usr/bin/env python3
"""
Enhanced LangChain Google Gemini Chatbot
Author: Dippu Kumar
Features: Conversation history, streaming, commands, rich UI and more!
"""

import getpass
import os
import json
import yaml
from datetime import datetime
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, AIMessage

# Rich imports for beautiful console output
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.markdown import Markdown
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt, Confirm
from rich import box
import time

# Load environment variables
load_dotenv()

class GeminiChatBot:
    def __init__(self):
        self.console = Console()
        self.config = self.load_config()
        self.setup_api_key()
        
        # Initialize model with config settings
        self.model = ChatGoogleGenerativeAI(
            model=self.config.get('model', {}).get('name', 'gemini-1.5-flash'),
            temperature=self.config.get('model', {}).get('temperature', 0.7)
        )
        
        self.conversation_history = []
        self.session_start = datetime.now()
        self.message_count = 0
    
    def load_config(self):
        """Load configuration from YAML file"""
        try:
            with open('config.yaml', 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            # Default configuration if file doesn't exist
            return {
                'model': {'name': 'gemini-1.5-flash', 'temperature': 0.7},
                'interface': {'show_timestamp': True, 'auto_save': True, 'max_history': 20},
                'features': {'streaming': False}
            }
        
    def setup_api_key(self):
        """Set up Google API key"""
        if not os.environ.get("GOOGLE_API_KEY"):
            self.console.print("\n[yellow]🔑 GOOGLE_API_KEY not found in .env file[/yellow]")
            os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter API key for Google Gemini: ")
        
        api_key = os.environ.get("GOOGLE_API_KEY")
        if api_key:
            self.console.print(f"[green]✅ API Key loaded: {api_key[:10]}...[/green]")
        
    def display_header(self):
        """Display beautiful chat header with Rich"""
        
        # Create a beautiful title panel
        title = Text("🤖 Enhanced Gemini AI Chat", style="bold blue")
        title_panel = Panel(
            title,
            box=box.DOUBLE,
            padding=(1, 2),
            style="blue"
        )
        
        # Create info table
        info_table = Table(show_header=False, box=None, padding=0)
        info_table.add_column(style="cyan", width=15)
        info_table.add_column(style="white")
        
        model_name = self.config.get('model', {}).get('name', 'gemini-1.5-flash')
        temperature = self.config.get('model', {}).get('temperature', 0.7)
        
        info_table.add_row("🧠 Model:", f"{model_name}")
        info_table.add_row("🌡️ Temperature:", f"{temperature}")
        info_table.add_row("💬 Commands:", "/help, /clear, /save, /history, /config, /quit")
        info_table.add_row("🎯 Ready:", "Type your message or use a command")
        
        info_panel = Panel(
            info_table,
            title="[bold cyan]Session Info[/bold cyan]",
            box=box.ROUNDED,
            padding=(0, 1),
            style="cyan"
        )
        
        self.console.print("\n")
        self.console.print(title_panel)
        self.console.print(info_panel)
        
    def handle_command(self, user_input):
        """Handle special commands"""
        command = user_input.lower().strip()
        
        if command == '/help':
            help_table = Table(title="[bold blue]Available Commands[/bold blue]", box=box.ROUNDED)
            help_table.add_column("Command", style="cyan", width=12)
            help_table.add_column("Description", style="white")
            
            help_table.add_row("/help", "Show this help message")
            help_table.add_row("/clear", "Clear conversation history")
            help_table.add_row("/save", "Save conversation to file")
            help_table.add_row("/history", "Show conversation summary")
            help_table.add_row("/config", "Show current configuration")
            help_table.add_row("/models", "Show available models")
            help_table.add_row("/quit", "Exit the chat")
            
            self.console.print("\n")
            self.console.print(help_table)
            return True
            
        elif command == '/clear':
            if self.conversation_history:
                if Confirm.ask("[yellow]Are you sure you want to clear conversation history?[/yellow]"):
                    self.conversation_history.clear()
                    self.message_count = 0
                    self.console.print("[green]🗑️ Conversation history cleared![/green]")
            else:
                self.console.print("[yellow]📝 No conversation history to clear![/yellow]")
            return True
            
        elif command == '/save':
            self.save_conversation()
            return True
            
        elif command == '/history':
            self.show_history()
            return True
            
        elif command == '/config':
            self.show_config()
            return True
            
        elif command == '/models':
            self.show_available_models()
            return True
            
        elif command in ['/quit', '/exit']:
            self.console.print("[bold yellow]👋 Thanks for chatting! Goodbye![/bold yellow]")
            return False
            
        return None  # Not a command
    
    def show_config(self):
        """Display current configuration"""
        config_table = Table(title="[bold blue]Current Configuration[/bold blue]", box=box.ROUNDED)
        config_table.add_column("Setting", style="cyan", width=20)
        config_table.add_column("Value", style="white")
        
        # Model settings
        model_config = self.config.get('model', {})
        config_table.add_row("Model Name", model_config.get('name', 'gemini-1.5-flash'))
        config_table.add_row("Temperature", str(model_config.get('temperature', 0.7)))
        config_table.add_row("Max Tokens", str(model_config.get('max_tokens', 1000)))
        
        # Interface settings
        interface_config = self.config.get('interface', {})
        config_table.add_row("Auto Save", str(interface_config.get('auto_save', True)))
        config_table.add_row("Max History", str(interface_config.get('max_history', 20)))
        config_table.add_row("Show Timestamp", str(interface_config.get('show_timestamp', True)))
        
        # Features
        features_config = self.config.get('features', {})
        config_table.add_row("Streaming", str(features_config.get('streaming', False)))
        
        self.console.print("\n")
        self.console.print(config_table)
    
    def show_available_models(self):
        """Show available Gemini models"""
        models_table = Table(title="[bold blue]Available Gemini Models[/bold blue]", box=box.ROUNDED)
        models_table.add_column("Model", style="cyan", width=25)
        models_table.add_column("Description", style="white")
        models_table.add_column("Best For", style="green")
        
        models_table.add_row(
            "gemini-1.5-flash", 
            "Fast, efficient model", 
            "Quick responses, chat"
        )
        models_table.add_row(
            "gemini-1.5-pro", 
            "More capable, slower", 
            "Complex reasoning, analysis"
        )
        models_table.add_row(
            "gemini-2.0-flash-exp", 
            "Latest experimental", 
            "Cutting-edge features"
        )
        
        self.console.print("\n")
        self.console.print(models_table)
        self.console.print("\n[dim]💡 To change model, edit the config.yaml file[/dim]")
        
    def save_conversation(self):
        """Save conversation to JSON file"""
        if not self.conversation_history:
            self.console.print("[yellow]📝 No conversation to save![/yellow]")
            return
            
        timestamp = self.session_start.strftime("%Y%m%d_%H%M%S")
        filename = f"chat_session_{timestamp}.json"
        
        # Convert messages to serializable format
        chat_data = {
            "session_start": self.session_start.isoformat(),
            "message_count": len(self.conversation_history),
            "messages": []
        }
        
        for msg in self.conversation_history:
            chat_data["messages"].append({
                "role": "human" if isinstance(msg, HumanMessage) else "ai",
                "content": msg.content,
                "timestamp": datetime.now().isoformat()
            })
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(chat_data, f, indent=2, ensure_ascii=False)
            
        self.console.print(f"[green]💾 Conversation saved to: {filename}[/green]")
        
    def show_history(self):
        """Show conversation summary"""
        if not self.conversation_history:
            self.console.print("[yellow]📝 No conversation history![/yellow]")
            return
        
        # Create summary table
        duration = datetime.now() - self.session_start
        
        summary_table = Table(title="[bold blue]📊 Conversation Summary[/bold blue]", box=box.ROUNDED)
        summary_table.add_column("Metric", style="cyan", width=20)
        summary_table.add_column("Value", style="white")
        
        summary_table.add_row("Session Started", self.session_start.strftime('%Y-%m-%d %H:%M:%S'))
        summary_table.add_row("Total Messages", str(len(self.conversation_history)))
        summary_table.add_row("Your Messages", str(len([m for m in self.conversation_history if isinstance(m, HumanMessage)])))
        summary_table.add_row("AI Responses", str(len([m for m in self.conversation_history if isinstance(m, AIMessage)])))
        summary_table.add_row("Duration", str(duration).split('.')[0])  # Remove microseconds
        
        self.console.print("\n")
        self.console.print(summary_table)
        
        # Show recent messages
        if len(self.conversation_history) > 0:
            recent_messages = self.conversation_history[-6:]  # Last 3 exchanges
            
            messages_panel = Panel(
                self._format_recent_messages(recent_messages),
                title="[bold cyan]💬 Recent Messages[/bold cyan]",
                box=box.ROUNDED
            )
            self.console.print(messages_panel)
    
    def _format_recent_messages(self, messages):
        """Format recent messages for display"""
        formatted = []
        for msg in messages:
            if isinstance(msg, HumanMessage):
                role = "[bold green]👤 You[/bold green]"
                content = msg.content[:100] + "..." if len(msg.content) > 100 else msg.content
            else:
                role = "[bold blue]🤖 Gemini[/bold blue]"
                content = msg.content[:100] + "..." if len(msg.content) > 100 else msg.content
            
            formatted.append(f"{role}: {content}")
        
        return "\n".join(formatted)
            
    def chat_loop(self):
        """Main chat loop with Rich UI"""
        self.display_header()
        
        while True:
            try:
                # Get user input with Rich prompt
                user_input = Prompt.ask("\n[bold green]💬 You[/bold green]").strip()
                
                if not user_input:
                    continue
                
                # Increment message count
                self.message_count += 1
                    
                # Handle commands
                command_result = self.handle_command(user_input)
                if command_result is False:  # Quit command
                    break
                elif command_result is True:  # Other commands
                    continue
                
                # Process as regular message with progress indicator
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    transient=True,
                    console=self.console
                ) as progress:
                    task = progress.add_task("🤔 Thinking...", total=None)
                    
                    # Add user message to history
                    user_message = HumanMessage(content=user_input)
                    self.conversation_history.append(user_message)
                    
                    # Get AI response with full conversation history
                    response = self.model.invoke(self.conversation_history)
                    
                    # Add AI response to history
                    self.conversation_history.append(response)
                
                # Display response in a beautiful panel
                if self.config.get('features', {}).get('streaming', False):
                    # Streaming response (simulate typing effect)
                    self.console.print("\n[bold blue]🤖 Gemini:[/bold blue]", end=" ")
                    for char in response.content:
                        self.console.print(char, end="", style="white")
                        time.sleep(0.01)  # Typing effect
                    self.console.print()  # New line
                else:
                    # Regular response in a panel
                    response_panel = Panel(
                        Markdown(response.content),
                        title="[bold blue]🤖 Gemini[/bold blue]",
                        title_align="left",
                        box=box.ROUNDED,
                        border_style="blue"
                    )
                    self.console.print("\n")
                    self.console.print(response_panel)
                
                # Show timestamp if enabled
                if self.config.get('interface', {}).get('show_timestamp', True):
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    self.console.print(f"[dim]⏰ {timestamp}[/dim]")
                
                # Auto-save if enabled
                if self.config.get('interface', {}).get('auto_save', True) and self.message_count % 10 == 0:
                    self.console.print("[dim]💾 Auto-saving conversation...[/dim]")
                    self.save_conversation()
                
                # Keep conversation history manageable
                max_history = self.config.get('interface', {}).get('max_history', 20)
                if len(self.conversation_history) > max_history:
                    self.conversation_history = self.conversation_history[-max_history:]
                    
            except KeyboardInterrupt:
                self.console.print("\n\n[yellow]👋 Chat interrupted. Goodbye![/yellow]")
                break
            except Exception as e:
                error_panel = Panel(
                    f"[red]❌ Error: {str(e)}[/red]\n\n[yellow]Please try again or type /quit to exit[/yellow]",
                    title="[bold red]Error[/bold red]",
                    box=box.ROUNDED,
                    border_style="red"
                )
                self.console.print("\n")
                self.console.print(error_panel)

def main():
    """Main function"""
    try:
        chatbot = GeminiChatBot()
        chatbot.chat_loop()
    except Exception as e:
        print(f"❌ Failed to start chatbot: {e}")

if __name__ == "__main__":
    main()