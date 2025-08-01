#!/usr/bin/env python3
"""
Chatbot Launcher
Author: Dippu Kumar
Choose between different chatbot versions
"""

import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import IntPrompt
from rich import box

console = Console()

def show_welcome():
    """Show welcome message and options"""
    
    # Welcome panel
    welcome_text = """
🤖 Welcome to the AI Chatbot Suite!

Choose from different chatbot implementations:
"""
    
    welcome_panel = Panel(
        welcome_text.strip(),
        title="[bold blue]AI Chatbot Launcher[/bold blue]",
        box=box.DOUBLE,
        style="blue"
    )
    
    console.print("\n")
    console.print(welcome_panel)
    
    # Options table
    options_table = Table(title="[bold cyan]Available Chatbots[/bold cyan]", box=box.ROUNDED)
    options_table.add_column("Option", style="cyan", width=8)
    options_table.add_column("Chatbot", style="white", width=25)
    options_table.add_column("Description", style="green", width=40)
    options_table.add_column("Best For", style="yellow")
    
    options_table.add_row(
        "1", 
        "Simple Chat (g.py)", 
        "Basic Gemini chatbot, single interaction",
        "Quick testing"
    )
    
    options_table.add_row(
        "2",
        "Enhanced Chat",
        "Rich UI, conversation history, commands",
        "Extended conversations"
    )
    
    options_table.add_row(
        "3",
        "Universal Chat",
        "Multi-provider, factory pattern, modular",
        "Production use, flexibility"
    )
    
    console.print(options_table)
    
    # Features comparison
    features_table = Table(title="[bold yellow]Feature Comparison[/bold yellow]", box=box.ROUNDED)
    features_table.add_column("Feature", style="cyan")
    features_table.add_column("Simple", style="white", justify="center")
    features_table.add_column("Enhanced", style="white", justify="center")
    features_table.add_column("Universal", style="white", justify="center")
    
    features_table.add_row("Basic Chat", "✅", "✅", "✅")
    features_table.add_row("Rich UI", "❌", "✅", "✅")
    features_table.add_row("Conversation History", "❌", "✅", "✅")
    features_table.add_row("Commands", "❌", "✅", "✅")
    features_table.add_row("Auto-save", "❌", "✅", "✅")
    features_table.add_row("Multiple Providers", "❌", "❌", "✅")
    features_table.add_row("Provider Switching", "❌", "❌", "✅")
    features_table.add_row("Factory Pattern", "❌", "❌", "✅")
    features_table.add_row("Modular Design", "❌", "❌", "✅")
    
    console.print("\n")
    console.print(features_table)

def run_chatbot(choice: int):
    """Run the selected chatbot"""
    
    if choice == 1:
        console.print("\n[green]🚀 Starting Simple Chatbot...[/green]")
        try:
            import subprocess
            subprocess.run([sys.executable, "g.py"])
        except Exception as e:
            console.print(f"[red]❌ Error running simple chatbot: {e}[/red]")
    
    elif choice == 2:
        console.print("\n[green]🚀 Starting Enhanced Chatbot...[/green]")
        try:
            import subprocess
            subprocess.run([sys.executable, "enhanced_chat.py"])
        except Exception as e:
            console.print(f"[red]❌ Error running enhanced chatbot: {e}[/red]")
    
    elif choice == 3:
        console.print("\n[green]🚀 Starting Universal Chatbot...[/green]")
        try:
            import subprocess
            subprocess.run([sys.executable, "universal_chatbot.py"])
        except Exception as e:
            console.print(f"[red]❌ Error running universal chatbot: {e}[/red]")
            console.print("[yellow]💡 Make sure you have all required dependencies installed[/yellow]")

def check_dependencies():
    """Check if required dependencies are available"""
    missing_deps = []
    
    try:
        import rich
    except ImportError:
        missing_deps.append("rich")
    
    try:
        import yaml
    except ImportError:
        missing_deps.append("pyyaml")
    
    try:
        import langchain
    except ImportError:
        missing_deps.append("langchain")
    
    if missing_deps:
        console.print(f"[red]⚠️  Missing dependencies: {', '.join(missing_deps)}[/red]")
        console.print("[yellow]💡 Run: pip install -r requirements.txt[/yellow]")
        return False
    
    return True

def main():
    """Main launcher function"""
    
    if not check_dependencies():
        return
    
    show_welcome()
    
    try:
        choice = IntPrompt.ask(
            "\n[cyan]Select chatbot (1-3)[/cyan]",
            choices=["1", "2", "3"]
        )
        
        run_chatbot(int(choice))
        
    except KeyboardInterrupt:
        console.print("\n[yellow]👋 Goodbye![/yellow]")
    except Exception as e:
        console.print(f"\n[red]❌ Error: {e}[/red]")

if __name__ == "__main__":
    main()