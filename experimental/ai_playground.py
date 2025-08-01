#!/usr/bin/env python3
"""
🎪 AI Playground - Revolutionary Multi-Experiment Sandbox
Author: Dippu Kumar

Combine multiple revolutionary AI experiments in one playground!
Mix and match different AI consciousness features for ultimate experiences.
"""

import os
import sys
import getpass
from datetime import datetime
from typing import Dict, List, Optional
import subprocess
from pathlib import Path

from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.columns import Columns
from rich.layout import Layout

# Load environment variables
load_dotenv()

console = Console()

class ExperimentCombiner:
    """Combines multiple AI experiments"""
    
    def __init__(self):
        self.available_experiments = {
            'emotional_memory': {
                'name': '🧠 Emotional Memory AI',
                'description': 'AI that remembers emotions and evolves personality',
                'file': 'emotional_memory_ai.py',
                'features': ['Emotional tracking', 'Personality evolution', 'Memory system'],
                'combinable': True
            },
            'multi_persona': {
                'name': '👥 Multi-Persona Chat',
                'description': 'Multiple AI personalities working together',
                'file': 'multi_persona_chat.py',
                'features': ['Multiple perspectives', 'Parallel thinking', 'Collaborative AI'],
                'combinable': True
            },
            'time_travel': {
                'name': '⏰ Time-Travel Conversations',
                'description': 'Chat with historical figures and future perspectives',
                'file': 'time_travel_chat.py',
                'features': ['Historical simulation', 'Future prediction', 'Time context'],
                'combinable': False
            },
            'swarm_intelligence': {
                'name': '🐝 AI Swarm Intelligence',
                'description': 'Multiple AIs debating and reaching consensus',
                'file': 'ai_swarm_intelligence.py',
                'features': ['Collective thinking', 'AI debates', 'Consensus building'],
                'combinable': False
            },
            'reality_synthesis': {
                'name': '🌀 Reality Synthesis Engine',
                'description': 'Explore topics from all possible dimensions',
                'file': 'reality_synthesis.py',
                'features': ['Multi-dimensional analysis', 'Reality layers', 'Comprehensive synthesis'],
                'combinable': True
            },
            'consciousness_bridge': {
                'name': '🧘 Consciousness Bridge',
                'description': 'AI adapts to match your thinking style',
                'file': 'consciousness_bridge.py',
                'features': ['Cognitive adaptation', 'Mind synchronization', 'Personalized AI'],
                'combinable': True
            },
            'mood_adaptive': {
                'name': '🎭 Mood-Adaptive UI',
                'description': 'Interface changes based on your emotions',
                'file': 'mood_adaptive_ui.py',
                'features': ['Emotional UI', 'Dynamic themes', 'Empathetic interface'],
                'combinable': True
            },
            'predictive_conversation': {
                'name': '🔮 Predictive Conversation',
                'description': 'AI predicts and prepares for your next questions',
                'file': 'predictive_conversation.py',
                'features': ['Question prediction', 'Pre-prepared responses', 'Conversation flow'],
                'combinable': True
            },
            'stream_consciousness': {
                'name': '🌊 Stream of Consciousness',
                'description': 'Watch AI think in real-time',
                'file': 'stream_consciousness.py',
                'features': ['Continuous thinking', 'Thought visualization', 'Real-time AI mind'],
                'combinable': True
            }
        }
        
        self.active_experiments = []
        self.session_stats = {
            'experiments_run': 0,
            'combinations_tried': 0,
            'start_time': datetime.now()
        }
    
    def setup_api_key(self):
        """Setup Google API key"""
        if not os.environ.get("GOOGLE_API_KEY"):
            console.print("🔑 [yellow]GOOGLE_API_KEY not found in environment[/yellow]")
            api_key = getpass.getpass("Enter your Google Gemini API key: ")
            os.environ["GOOGLE_API_KEY"] = api_key

class AIPlayground:
    """Revolutionary AI experiment playground"""
    
    def __init__(self):
        self.setup_api_key()
        self.combiner = ExperimentCombiner()
        self.playground_history = []
    
    def setup_api_key(self):
        """Setup Google API key"""
        if not os.environ.get("GOOGLE_API_KEY"):
            console.print("🔑 [yellow]GOOGLE_API_KEY not found in environment[/yellow]")
            api_key = getpass.getpass("Enter your Google Gemini API key: ")
            os.environ["GOOGLE_API_KEY"] = api_key
    
    def display_header(self):
        """Display playground header"""
        header_text = Text()
        header_text.append("🎪 ", style="bright_yellow")
        header_text.append("AI PLAYGROUND", style="bold bright_cyan")
        header_text.append(" 🚀", style="bright_yellow")
        
        subtitle = Text()
        subtitle.append("Revolutionary Multi-Experiment Sandbox by ", style="dim")
        subtitle.append("Dippu Kumar", style="bold bright_magenta")
        subtitle.append("\nCombine revolutionary AI experiments!", style="dim")
        
        console.print(Panel(
            Text.assemble(header_text, "\n\n", subtitle),
            border_style="bright_cyan",
            padding=(1, 2)
        ))
    
    def display_experiments_catalog(self):
        """Display all available experiments"""
        
        console.print()
        console.print("🧪 [bold bright_cyan]Revolutionary AI Experiments Catalog[/bold bright_cyan]")
        console.print()
        
        # Create two columns for experiments
        experiments = list(self.combiner.available_experiments.items())
        mid_point = len(experiments) // 2
        
        left_experiments = experiments[:mid_point]
        right_experiments = experiments[mid_point:]
        
        # Left column
        left_panels = []
        for exp_id, exp_data in left_experiments:
            exp_text = Text()
            exp_text.append(f"{exp_data['name']}\n", style="bold bright_green")
            exp_text.append(f"{exp_data['description']}\n\n", style="bright_white")
            exp_text.append("Features:\n", style="bright_cyan")
            for feature in exp_data['features']:
                exp_text.append(f"• {feature}\n", style="dim")
            
            combinable_status = "✅ Combinable" if exp_data['combinable'] else "⚠️ Standalone"
            exp_text.append(f"\n{combinable_status}", style="bright_yellow" if exp_data['combinable'] else "bright_red")
            
            left_panels.append(Panel(
                exp_text,
                title=f"🧪 {exp_id.replace('_', ' ').title()}",
                border_style="bright_green"
            ))
        
        # Right column
        right_panels = []
        for exp_id, exp_data in right_experiments:
            exp_text = Text()
            exp_text.append(f"{exp_data['name']}\n", style="bold bright_green")
            exp_text.append(f"{exp_data['description']}\n\n", style="bright_white")
            exp_text.append("Features:\n", style="bright_cyan")
            for feature in exp_data['features']:
                exp_text.append(f"• {feature}\n", style="dim")
            
            combinable_status = "✅ Combinable" if exp_data['combinable'] else "⚠️ Standalone"
            exp_text.append(f"\n{combinable_status}", style="bright_yellow" if exp_data['combinable'] else "bright_red")
            
            right_panels.append(Panel(
                exp_text,
                title=f"🧪 {exp_id.replace('_', ' ').title()}",
                border_style="bright_green"
            ))
        
        # Balance the columns
        while len(left_panels) < len(right_panels):
            left_panels.append(Panel("", border_style="dim"))
        while len(right_panels) < len(left_panels):
            right_panels.append(Panel("", border_style="dim"))
        
        # Display in columns
        for left, right in zip(left_panels, right_panels):
            console.print(Columns([left, right], equal=True))
    
    def display_experiment_menu(self):
        """Display experiment selection menu"""
        
        table = Table(title="🎪 AI Experiment Selection", show_header=True, header_style="bold magenta")
        table.add_column("ID", style="bright_cyan", width=4)
        table.add_column("Experiment", style="bright_green", width=25)
        table.add_column("Description", style="bright_white", width=40)
        table.add_column("Status", style="bright_yellow", width=12)
        
        for i, (exp_id, exp_data) in enumerate(self.combiner.available_experiments.items(), 1):
            status = "Combinable" if exp_data['combinable'] else "Standalone"
            table.add_row(
                str(i),
                exp_data['name'],
                exp_data['description'][:60] + "..." if len(exp_data['description']) > 60 else exp_data['description'],
                status
            )
        
        console.print(table)
    
    def run_single_experiment(self, experiment_id: str):
        """Run a single experiment"""
        
        exp_data = self.combiner.available_experiments[experiment_id]
        script_path = Path(__file__).parent / exp_data['file']
        
        if not script_path.exists():
            console.print(f"❌ [red]Experiment file not found: {exp_data['file']}[/red]")
            return
        
        console.print(f"\n🚀 [bold bright_green]Launching {exp_data['name']}...[/bold bright_green]")
        console.print(f"📝 [dim]{exp_data['description']}[/dim]")
        console.print()
        
        try:
            subprocess.run([sys.executable, str(script_path)], check=True)
            self.combiner.session_stats['experiments_run'] += 1
        except subprocess.CalledProcessError as e:
            console.print(f"❌ [bold red]Error running experiment:[/bold red] {e}")
        except KeyboardInterrupt:
            console.print("\n👋 [yellow]Experiment interrupted by user[/yellow]")
    
    def playground_mode(self):
        """Interactive playground mode"""
        
        console.print(Panel(
            Text.assemble(
                ("🎪 ", "bright_yellow"),
                ("Welcome to the AI Playground!", "bold bright_green"),
                ("\n\nExplore revolutionary AI experiments!\n", "bright_white"),
                ("🧪 ", "bright_cyan"), ("9 groundbreaking experiments available\n", "cyan"),
                ("🔀 ", "bright_magenta"), ("Combine compatible experiments\n", "magenta"),
                ("🚀 ", "bright_green"), ("Push the boundaries of AI interaction\n", "green"),
                ("\nEach experiment represents a breakthrough in AI consciousness!\n", "dim"),
                ("\nCreated by ", "dim"),
                ("Dippu Kumar", "bold bright_magenta")
            ),
            border_style="bright_cyan"
        ))
        
        while True:
            console.print()
            console.print("🎮 [bold bright_cyan]Playground Options:[/bold bright_cyan]")
            console.print("1. 📖 [bright_green]Browse Experiments Catalog[/bright_green]")
            console.print("2. 🚀 [bright_yellow]Launch Single Experiment[/bright_yellow]") 
            console.print("3. 🔀 [bright_magenta]Experiment Combinations (Coming Soon)[/bright_magenta]")
            console.print("4. 📊 [bright_blue]View Session Stats[/bright_blue]")
            console.print("5. 👋 [bright_red]Exit Playground[/bright_red]")
            
            choice = Prompt.ask("\n🎯 [bold bright_cyan]Choose your adventure[/bold bright_cyan]", choices=["1", "2", "3", "4", "5"], default="1")
            
            if choice == "1":
                self.display_experiments_catalog()
                input("\n🔄 Press Enter to continue...")
            
            elif choice == "2":
                console.print()
                self.display_experiment_menu()
                
                exp_choice = Prompt.ask(
                    "\n🧪 [bold bright_cyan]Select experiment (1-9)[/bold bright_cyan]",
                    choices=[str(i) for i in range(1, 10)],
                    default="1"
                )
                
                exp_ids = list(self.combiner.available_experiments.keys())
                selected_exp = exp_ids[int(exp_choice) - 1]
                
                self.run_single_experiment(selected_exp)
            
            elif choice == "3":
                console.print()
                console.print(Panel(
                    Text.assemble(
                        ("🔀 ", "bright_magenta"),
                        ("Experiment Combinations", "bold bright_cyan"),
                        ("\n\n🚧 Coming Soon! 🚧\n", "bright_yellow"),
                        ("This feature will allow you to:\n", "bright_white"),
                        ("• Combine Emotional Memory + Mood Adaptive UI\n", "green"),
                        ("• Mix Consciousness Bridge + Predictive Conversation\n", "green"),
                        ("• Blend Reality Synthesis + Stream of Consciousness\n", "green"),
                        ("\nImagine the possibilities! 🌟", "bright_magenta")
                    ),
                    border_style="bright_magenta"
                ))
            
            elif choice == "4":
                self.display_session_stats()
            
            elif choice == "5":
                break
    
    def display_session_stats(self):
        """Display playground session statistics"""
        duration = datetime.now() - self.combiner.session_stats['start_time']
        
        stats_text = Text()
        stats_text.append(f"🎪 AI Playground Session\n\n", style="bold bright_cyan")
        stats_text.append(f"🕒 Duration: {str(duration).split('.')[0]}\n", style="bright_green")
        stats_text.append(f"🧪 Experiments Run: {self.combiner.session_stats['experiments_run']}\n", style="bright_yellow")
        stats_text.append(f"🔀 Combinations Tried: {self.combiner.session_stats['combinations_tried']}\n", style="bright_blue")
        stats_text.append(f"🚀 Total Experiments Available: {len(self.combiner.available_experiments)}\n", style="bright_magenta")
        stats_text.append(f"💡 Revolutionary Features Explored: {self.combiner.session_stats['experiments_run'] * 3}", style="bright_cyan")
        
        console.print(Panel(stats_text, title="📊 Playground Statistics", border_style="bright_cyan"))
    
    def main_loop(self):
        """Main playground loop"""
        
        console.clear()
        self.display_header()
        
        try:
            self.playground_mode()
        except KeyboardInterrupt:
            pass
        finally:
            console.print()
            self.display_session_stats()
            console.print()
            console.print(Panel(
                Text.assemble(
                    ("Thank you for exploring the AI Playground! 🎪\n", "bright_green"),
                    ("You experienced ", "bright_white"),
                    (f"{self.combiner.session_stats['experiments_run']}", "bold bright_yellow"),
                    (" revolutionary AI experiments.\n", "bright_white"),
                    ("Each one pushed the boundaries of what's possible! 🚀\n\n", "bright_blue"),
                    ("Continue exploring the future of AI consciousness!\n", "bright_magenta"),
                    ("\nRevolutionary AI Playground by ", "dim"),
                    ("Dippu Kumar", "bold bright_magenta")
                ),
                title="🎪 Playground Session Complete",
                border_style="bright_magenta"
            ))

def main():
    """Main function"""
    try:
        playground = AIPlayground()
        playground.main_loop()
    except Exception as e:
        console.print(f"❌ [bold red]Error:[/bold red] {e}")

if __name__ == "__main__":
    main()