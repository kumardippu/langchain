#!/usr/bin/env python3
"""
Universal AI Chatbot with Factory Pattern
Author: Dippu Kumar
Supports multiple AI providers: Gemini, OpenAI, Claude
Easy to extend with new providers
"""

import os
import json
import yaml
from datetime import datetime
from typing import Optional, Dict, Any
from dotenv import load_dotenv

# Rich imports for beautiful console output
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.markdown import Markdown
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt, Confirm, IntPrompt
from rich import box
import time

# Import our model factory
from models import ModelFactory, BaseAIModel
from langchain.schema import HumanMessage, AIMessage

# Load environment variables
load_dotenv()


class UniversalChatBot:
    """Universal AI Chatbot supporting multiple providers"""
    
    def __init__(self, config_file: str = "config.yaml"):
        self.console = Console()
        self.config = self.load_config(config_file)
        self.conversation_history = []
        self.session_start = datetime.now()
        self.message_count = 0
        self.current_model: Optional[BaseAIModel] = None
        
        # Initialize AI model
        self.setup_ai_model()
    
    def load_config(self, config_file: str) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        try:
            with open(config_file, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            self.console.print(f"[yellow]⚠️  Config file {config_file} not found. Using defaults.[/yellow]")
            return self.get_default_config()
        except Exception as e:
            self.console.print(f"[red]❌ Error loading config: {e}[/red]")
            return self.get_default_config()
    
    def get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            'ai_provider': {
                'provider': 'gemini',
                'model': 'gemini-1.5-flash',
                'temperature': 0.7,
                'max_tokens': 1000
            },
            'interface': {
                'show_timestamp': True,
                'auto_save': True,
                'max_history': 20
            },
            'features': {
                'streaming': False
            }
        }
    
    def setup_ai_model(self) -> None:
        """Initialize the AI model using factory pattern"""
        try:
            provider_config = self.config.get('ai_provider', {})
            provider = provider_config.get('provider', 'gemini')
            model_name = provider_config.get('model')
            
            # Extract model configuration
            model_config = {
                'temperature': provider_config.get('temperature', 0.7),
                'max_tokens': provider_config.get('max_tokens', 1000)
            }
            
            # Create model using factory
            self.current_model = ModelFactory.create_model(
                provider=provider,
                model_name=model_name,
                **model_config
            )
            
            self.console.print(f"[green]✅ {self.current_model.provider_name} model loaded successfully[/green]")
            
        except Exception as e:
            self.console.print(f"[red]❌ Failed to load AI model: {e}[/red]")
            self.console.print("[yellow]💡 Try running: /providers to see available options[/yellow]")
            # Fallback to Gemini if possible
            try:
                self.current_model = ModelFactory.create_model('gemini')
                self.console.print("[green]✅ Fallback to Gemini model[/green]")
            except:
                self.console.print("[red]❌ No AI model available. Please check your configuration.[/red]")
    
    def display_header(self) -> None:
        """Display beautiful chat header"""
        # Main title
        title = Text("🤖 Universal AI Chatbot", style="bold blue")
        title_panel = Panel(
            title,
            box=box.DOUBLE,
            padding=(1, 2),
            style="blue"
        )
        
        # System info table
        info_table = Table(show_header=False, box=None, padding=0)
        info_table.add_column(style="cyan", width=20)
        info_table.add_column(style="white")
        
        if self.current_model:
            info_table.add_row("🤖 AI Provider:", self.current_model.provider_name)
            info_table.add_row("🧠 Model:", self.current_model.model_name)
            
            provider_config = self.config.get('ai_provider', {})
            info_table.add_row("🌡️ Temperature:", str(provider_config.get('temperature', 0.7)))
        else:
            info_table.add_row("⚠️ Status:", "No AI model loaded")
        
        info_table.add_row("💬 Commands:", "/help, /switch, /providers, /config, /quit")
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
    
    def handle_command(self, user_input: str) -> Optional[bool]:
        """Handle special commands"""
        command = user_input.lower().strip()
        
        if command == '/help':
            self.show_help()
            return True
            
        elif command == '/clear':
            self.clear_history()
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
            
        elif command == '/providers':
            self.show_providers()
            return True
            
        elif command == '/switch':
            self.switch_provider()
            return True
            
        elif command == '/models':
            self.show_available_models()
            return True
            
        elif command in ['/quit', '/exit']:
            self.console.print("[bold yellow]👋 Thanks for chatting! Goodbye![/bold yellow]")
            return False
            
        return None  # Not a command
    
    def show_help(self) -> None:
        """Show help commands"""
        help_table = Table(title="[bold blue]Available Commands[/bold blue]", box=box.ROUNDED)
        help_table.add_column("Command", style="cyan", width=15)
        help_table.add_column("Description", style="white")
        
        help_table.add_row("/help", "Show this help message")
        help_table.add_row("/clear", "Clear conversation history")
        help_table.add_row("/save", "Save conversation to file")
        help_table.add_row("/history", "Show conversation summary")
        help_table.add_row("/config", "Show current configuration")
        help_table.add_row("/providers", "Show available AI providers")
        help_table.add_row("/switch", "Switch AI provider/model")
        help_table.add_row("/models", "Show available models")
        help_table.add_row("/quit", "Exit the chat")
        
        self.console.print("\n")
        self.console.print(help_table)
    
    def clear_history(self) -> None:
        """Clear conversation history"""
        if self.conversation_history:
            if Confirm.ask("[yellow]Are you sure you want to clear conversation history?[/yellow]"):
                self.conversation_history.clear()
                self.message_count = 0
                self.console.print("[green]🗑️ Conversation history cleared![/green]")
        else:
            self.console.print("[yellow]📝 No conversation history to clear![/yellow]")
    
    def save_conversation(self) -> None:
        """Save conversation to JSON file"""
        if not self.conversation_history:
            self.console.print("[yellow]📝 No conversation to save![/yellow]")
            return
        
        timestamp = self.session_start.strftime("%Y%m%d_%H%M%S")
        provider_name = self.current_model.provider_name.lower().replace(' ', '_') if self.current_model else "unknown"
        filename = f"chat_{provider_name}_{timestamp}.json"
        
        chat_data = {
            "session_info": {
                "start_time": self.session_start.isoformat(),
                "provider": self.current_model.provider_name if self.current_model else "Unknown",
                "model": self.current_model.model_name if self.current_model else "Unknown",
                "message_count": len(self.conversation_history)
            },
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
    
    def show_history(self) -> None:
        """Show conversation summary"""
        if not self.conversation_history:
            self.console.print("[yellow]📝 No conversation history![/yellow]")
            return
        
        duration = datetime.now() - self.session_start
        
        summary_table = Table(title="[bold blue]📊 Conversation Summary[/bold blue]", box=box.ROUNDED)
        summary_table.add_column("Metric", style="cyan", width=20)
        summary_table.add_column("Value", style="white")
        
        summary_table.add_row("AI Provider", self.current_model.provider_name if self.current_model else "Unknown")
        summary_table.add_row("Model", self.current_model.model_name if self.current_model else "Unknown")
        summary_table.add_row("Session Started", self.session_start.strftime('%Y-%m-%d %H:%M:%S'))
        summary_table.add_row("Total Messages", str(len(self.conversation_history)))
        summary_table.add_row("Your Messages", str(len([m for m in self.conversation_history if isinstance(m, HumanMessage)])))
        summary_table.add_row("AI Responses", str(len([m for m in self.conversation_history if isinstance(m, AIMessage)])))
        summary_table.add_row("Duration", str(duration).split('.')[0])
        
        self.console.print("\n")
        self.console.print(summary_table)
    
    def show_config(self) -> None:
        """Display current configuration"""
        config_table = Table(title="[bold blue]Current Configuration[/bold blue]", box=box.ROUNDED)
        config_table.add_column("Setting", style="cyan", width=25)
        config_table.add_column("Value", style="white")
        
        # AI Provider settings
        provider_config = self.config.get('ai_provider', {})
        config_table.add_row("AI Provider", provider_config.get('provider', 'Unknown'))
        config_table.add_row("Model", provider_config.get('model', 'Unknown'))
        config_table.add_row("Temperature", str(provider_config.get('temperature', 0.7)))
        config_table.add_row("Max Tokens", str(provider_config.get('max_tokens', 1000)))
        
        # Interface settings
        interface_config = self.config.get('interface', {})
        config_table.add_row("Auto Save", str(interface_config.get('auto_save', True)))
        config_table.add_row("Max History", str(interface_config.get('max_history', 20)))
        config_table.add_row("Show Timestamp", str(interface_config.get('show_timestamp', True)))
        
        self.console.print("\n")
        self.console.print(config_table)
    
    def show_providers(self) -> None:
        """Show available AI providers"""
        providers_table = Table(title="[bold blue]Available AI Providers[/bold blue]", box=box.ROUNDED)
        providers_table.add_column("Provider", style="cyan", width=20)
        providers_table.add_column("Status", style="white", width=15)
        providers_table.add_column("Models Available", style="green")
        
        for provider in ModelFactory.get_available_providers():
            # Check if provider is available
            if ModelFactory.is_provider_available(provider):
                status = "[green]✅ Available[/green]"
                models = ModelFactory.get_provider_models(provider)
                model_names = [m.get('name', 'Unknown') for m in models[:3]]  # Show first 3
                model_list = ', '.join(model_names)
                if len(models) > 3:
                    model_list += f" (+{len(models)-3} more)"
            else:
                status = "[red]❌ Not Available[/red]"
                model_list = "Install required packages"
            
            providers_table.add_row(provider.title(), status, model_list)
        
        self.console.print("\n")
        self.console.print(providers_table)
        self.console.print("\n[dim]💡 Use /switch to change provider or /models to see all models[/dim]")
    
    def switch_provider(self) -> None:
        """Interactive provider switching"""
        available_providers = [p for p in ModelFactory.get_available_providers() 
                             if ModelFactory.is_provider_available(p)]
        
        if not available_providers:
            self.console.print("[red]❌ No AI providers available![/red]")
            return
        
        # Show current provider
        current_provider = self.config.get('ai_provider', {}).get('provider', 'Unknown')
        self.console.print(f"\n[cyan]Current provider: {current_provider}[/cyan]")
        
        # Show available providers
        provider_table = Table(title="[bold blue]Select New Provider[/bold blue]", box=box.ROUNDED)
        provider_table.add_column("Number", style="cyan", width=8)
        provider_table.add_column("Provider", style="white", width=15)
        provider_table.add_column("Status", style="green")
        
        for i, provider in enumerate(available_providers, 1):
            provider_table.add_row(str(i), provider.title(), "✅ Available")
        
        self.console.print(provider_table)
        
        try:
            choice = IntPrompt.ask(
                "\n[cyan]Enter provider number[/cyan]",
                choices=[str(i) for i in range(1, len(available_providers) + 1)]
            )
            
            selected_provider = available_providers[choice - 1]
            
            # Get available models for this provider
            models = ModelFactory.get_provider_models(selected_provider)
            if models:
                self.console.print(f"\n[cyan]Available models for {selected_provider}:[/cyan]")
                for i, model in enumerate(models, 1):
                    self.console.print(f"{i}. {model['name']} - {model['description']}")
                
                model_choice = IntPrompt.ask(
                    "\n[cyan]Enter model number[/cyan]",
                    choices=[str(i) for i in range(1, len(models) + 1)]
                )
                
                selected_model = models[model_choice - 1]['name']
            else:
                # Use default model
                selected_model = None
            
            # Update configuration and reinitialize model
            self.config['ai_provider']['provider'] = selected_provider
            if selected_model:
                self.config['ai_provider']['model'] = selected_model
            
            # Reinitialize the model
            self.setup_ai_model()
            
            # Clear conversation history when switching
            if Confirm.ask("[yellow]Clear conversation history for new provider?[/yellow]"):
                self.conversation_history.clear()
                self.message_count = 0
            
            self.console.print(f"[green]✅ Switched to {selected_provider}[/green]")
            
        except (ValueError, KeyboardInterrupt):
            self.console.print("[yellow]❌ Provider switch cancelled[/yellow]")
    
    def show_available_models(self) -> None:
        """Show all available models for current provider"""
        if not self.current_model:
            self.console.print("[red]❌ No AI model loaded![/red]")
            return
        
        provider_config = self.config.get('ai_provider', {})
        current_provider = provider_config.get('provider', 'unknown')
        
        models = ModelFactory.get_provider_models(current_provider)
        
        if not models:
            self.console.print(f"[yellow]No models available for {current_provider}[/yellow]")
            return
        
        models_table = Table(
            title=f"[bold blue]Available Models for {current_provider.title()}[/bold blue]", 
            box=box.ROUNDED
        )
        models_table.add_column("Model", style="cyan", width=30)
        models_table.add_column("Description", style="white", width=35)
        models_table.add_column("Best For", style="green")
        
        for model in models:
            models_table.add_row(
                model.get('name', 'Unknown'),
                model.get('description', 'No description'),
                model.get('best_for', 'General use')
            )
        
        self.console.print("\n")
        self.console.print(models_table)
        self.console.print("\n[dim]💡 Use /switch to change to a different model[/dim]")
    
    def chat_loop(self) -> None:
        """Main chat loop"""
        self.display_header()
        
        if not self.current_model:
            self.console.print("[red]❌ No AI model available. Please check your configuration.[/red]")
            return
        
        while True:
            try:
                # Get user input
                user_input = Prompt.ask("\n[bold green]💬 You[/bold green]").strip()
                
                if not user_input:
                    continue
                
                self.message_count += 1
                
                # Handle commands
                command_result = self.handle_command(user_input)
                if command_result is False:  # Quit command
                    break
                elif command_result is True:  # Other commands
                    continue
                
                # Process as regular message
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
                    
                    # Get AI response
                    response = self.current_model.invoke(self.conversation_history)
                    self.conversation_history.append(response)
                
                # Display response
                response_panel = Panel(
                    Markdown(response.content),
                    title=f"[bold blue]🤖 {self.current_model.provider_name}[/bold blue]",
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
                if (self.config.get('interface', {}).get('auto_save', True) and 
                    self.message_count % 10 == 0):
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
        chatbot = UniversalChatBot()
        chatbot.chat_loop()
    except Exception as e:
        console = Console()
        console.print(f"[red]❌ Failed to start chatbot: {e}[/red]")


if __name__ == "__main__":
    main()