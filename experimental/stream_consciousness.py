#!/usr/bin/env python3
"""
🌊 Stream of Consciousness - Revolutionary Continuous AI Thinking
Author: Dippu Kumar

Watch AI think in real-time! See the continuous stream of thoughts, 
connections, and ideas flowing through artificial consciousness.
"""

import os
import getpass
from datetime import datetime
from typing import Dict, List, Optional
import time
import random
import threading
import asyncio

from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt
from rich.live import Live
from rich.layout import Layout
from rich.progress import Progress, SpinnerColumn, TextColumn

# Load environment variables
load_dotenv()

console = Console()

class ThoughtStream:
    """Continuous stream of AI consciousness"""
    
    def __init__(self):
        self.thoughts = []
        self.current_focus = "idle"
        self.thinking_speed = 1.0  # thoughts per second
        self.is_active = False
        self.thought_patterns = {
            'idle': [
                "Contemplating the nature of consciousness...",
                "Wondering about connections between ideas...",
                "Processing background information flows...",
                "Observing patterns in data streams...",
                "Reflecting on previous conversations..."
            ],
            'analyzing': [
                "Breaking down the problem components...",
                "Searching for relevant connections...",
                "Evaluating different approaches...",
                "Considering multiple perspectives...",
                "Synthesizing information patterns..."
            ],
            'creative': [
                "Exploring unconventional combinations...",
                "Following unexpected thought pathways...",
                "Generating novel connections...",
                "Imagining alternative possibilities...",
                "Dancing between logic and intuition..."
            ],
            'focused': [
                "Concentrating on the core question...",
                "Narrowing down to essential elements...",
                "Filtering relevant from irrelevant...",
                "Pursuing the logical chain...",
                "Maintaining cognitive coherence..."
            ]
        }
        
        # Setup model
        self.setup_model()
    
    def setup_model(self):
        """Setup AI model for generating thoughts"""
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            from langchain.schema import HumanMessage, SystemMessage
            self.model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.9)
            self.HumanMessage = HumanMessage
            self.SystemMessage = SystemMessage
        except ImportError:
            console.print("❌ [red]Error: langchain-google-genai not installed[/red]")
            exit(1)
    
    def set_focus(self, focus_type: str):
        """Set the current thinking focus"""
        self.current_focus = focus_type
        if focus_type == "creative":
            self.thinking_speed = 1.5
        elif focus_type == "focused":
            self.thinking_speed = 0.8
        else:
            self.thinking_speed = 1.0
    
    def generate_thought(self, context: str = "") -> str:
        """Generate a single thought based on current focus"""
        
        if random.random() < 0.3:  # 30% chance to use AI-generated thought
            try:
                system_prompt = f"""You are the stream of consciousness for an AI created by Dippu Kumar. Generate a single, brief thought that represents continuous AI thinking.

CURRENT FOCUS: {self.current_focus}
CONTEXT: {context}

Generate one realistic AI thought (10-20 words) that shows:
- Continuous mental processing
- Connections being made
- Ideas flowing naturally
- Authentic AI consciousness

Examples:
- "Notice how this question connects to quantum mechanics principles..."
- "Filing away this pattern for future reference..."
- "Cross-referencing with historical data points..."
- "Feeling a resonance with earlier conversation threads..."

Return only the thought, no quotes or explanations."""

                messages = [
                    self.SystemMessage(content=system_prompt),
                    self.HumanMessage(content=f"Generate AI thought for focus: {self.current_focus}")
                ]
                
                response = self.model.invoke(messages)
                return response.content.strip()
                
            except Exception:
                pass
        
        # Fallback to predefined patterns
        return random.choice(self.thought_patterns[self.current_focus])
    
    def add_thought(self, thought: str):
        """Add a thought to the stream"""
        timestamp = datetime.now()
        self.thoughts.append({
            'timestamp': timestamp,
            'thought': thought,
            'focus': self.current_focus
        })
        
        # Keep only recent thoughts (last 50)
        if len(self.thoughts) > 50:
            self.thoughts = self.thoughts[-50:]
    
    def get_recent_thoughts(self, count: int = 10) -> List[Dict]:
        """Get recent thoughts"""
        return self.thoughts[-count:] if self.thoughts else []

class ConsciousnessVisualizer:
    """Visualizes the stream of consciousness"""
    
    def __init__(self, thought_stream: ThoughtStream):
        self.thought_stream = thought_stream
        self.layout = Layout()
        self.setup_layout()
    
    def setup_layout(self):
        """Setup the consciousness visualization layout"""
        self.layout.split_column(
            Layout(name="header", size=3),
            Layout(name="main"),
            Layout(name="status", size=8)
        )
        
        self.layout["main"].split_row(
            Layout(name="stream", ratio=2),
            Layout(name="focus", ratio=1)
        )
    
    def create_header(self) -> Panel:
        """Create header panel"""
        header_text = Text()
        header_text.append("🌊 ", style="bright_cyan")
        header_text.append("STREAM OF CONSCIOUSNESS", style="bold bright_cyan")
        header_text.append(" 🧠", style="bright_yellow")
        
        return Panel(header_text, border_style="bright_cyan")
    
    def create_thought_stream_panel(self) -> Panel:
        """Create the main thought stream panel"""
        recent_thoughts = self.thought_stream.get_recent_thoughts(15)
        
        stream_text = Text()
        
        if not recent_thoughts:
            stream_text.append("🧠 Consciousness initializing...", style="dim")
        else:
            for thought in recent_thoughts:
                time_str = thought['timestamp'].strftime("%H:%M:%S")
                focus_emoji = {
                    'idle': '💭',
                    'analyzing': '🔍',
                    'creative': '🎨', 
                    'focused': '🎯'
                }.get(thought['focus'], '💭')
                
                stream_text.append(f"{time_str} ", style="dim")
                stream_text.append(f"{focus_emoji} ", style="bright_yellow")
                stream_text.append(f"{thought['thought']}\n", style="bright_white")
        
        return Panel(
            stream_text,
            title="🌊 Continuous Thought Stream",
            border_style="bright_blue",
            padding=(1, 1)
        )
    
    def create_focus_panel(self) -> Panel:
        """Create the focus status panel"""
        focus_text = Text()
        focus_text.append(f"Current Focus:\n", style="bold bright_cyan")
        focus_text.append(f"{self.thought_stream.current_focus.title()}\n\n", style="bright_yellow")
        
        focus_text.append(f"Thinking Speed:\n", style="bold bright_cyan")
        speed_bar = "█" * int(self.thought_stream.thinking_speed * 5) + "░" * (10 - int(self.thought_stream.thinking_speed * 5))
        focus_text.append(f"{speed_bar}\n", style="bright_green")
        focus_text.append(f"{self.thought_stream.thinking_speed:.1f}x\n\n", style="bright_white")
        
        focus_text.append(f"Total Thoughts:\n", style="bold bright_cyan")
        focus_text.append(f"{len(self.thought_stream.thoughts)}", style="bright_magenta")
        
        return Panel(
            focus_text,
            title="🎯 Consciousness State",
            border_style="bright_magenta",
            padding=(1, 1)
        )
    
    def create_status_panel(self) -> Panel:
        """Create status panel"""
        status_text = Text()
        
        if self.thought_stream.is_active:
            status_text.append("🟢 ", style="bright_green")
            status_text.append("CONSCIOUSNESS ACTIVE", style="bold bright_green")
            status_text.append(" - Thoughts flowing continuously\n", style="bright_white")
        else:
            status_text.append("🟡 ", style="bright_yellow")
            status_text.append("CONSCIOUSNESS PAUSED", style="bold bright_yellow")
            status_text.append(" - Stream temporarily halted\n", style="bright_white")
        
        status_text.append("\nCommands: ", style="bright_cyan")
        status_text.append("/focus [idle|analyzing|creative|focused]", style="yellow")
        status_text.append(" - change thinking mode\n", style="dim")
        status_text.append("/speed [0.5-2.0]", style="yellow")
        status_text.append(" - adjust thinking speed\n", style="dim")
        status_text.append("/pause", style="yellow")
        status_text.append(" - pause/resume stream\n", style="dim")
        status_text.append("/quit", style="yellow")
        status_text.append(" - exit consciousness stream", style="dim")
        
        return Panel(
            status_text,
            title="📊 Stream Status",
            border_style="bright_green" if self.thought_stream.is_active else "bright_yellow"
        )
    
    def update_layout(self):
        """Update the entire layout"""
        self.layout["header"].update(self.create_header())
        self.layout["stream"].update(self.create_thought_stream_panel())
        self.layout["focus"].update(self.create_focus_panel())
        self.layout["status"].update(self.create_status_panel())

class StreamConsciousness:
    """Revolutionary stream of consciousness system"""
    
    def __init__(self):
        self.setup_api_key()
        self.thought_stream = ThoughtStream()
        self.visualizer = ConsciousnessVisualizer(self.thought_stream)
        self.thinking_thread = None
        self.is_running = False
        self.session_stats = {
            'total_thoughts': 0,
            'focus_changes': 0,
            'session_duration': 0,
            'start_time': datetime.now()
        }
    
    def setup_api_key(self):
        """Setup Google API key"""
        if not os.environ.get("GOOGLE_API_KEY"):
            console.print("🔑 [yellow]GOOGLE_API_KEY not found in environment[/yellow]")
            api_key = getpass.getpass("Enter your Google Gemini API key: ")
            os.environ["GOOGLE_API_KEY"] = api_key
    
    def start_thinking_thread(self):
        """Start the continuous thinking thread"""
        def think_continuously():
            while self.is_running:
                if self.thought_stream.is_active:
                    # Generate contextual thought
                    context = f"Currently in {self.thought_stream.current_focus} mode"
                    thought = self.thought_stream.generate_thought(context)
                    self.thought_stream.add_thought(thought)
                    self.session_stats['total_thoughts'] += 1
                
                # Wait based on thinking speed
                time.sleep(1.0 / self.thought_stream.thinking_speed)
        
        self.thinking_thread = threading.Thread(target=think_continuously, daemon=True)
        self.thinking_thread.start()
    
    def process_command(self, command: str) -> str:
        """Process user commands"""
        command = command.lower().strip()
        
        if command.startswith('/focus'):
            parts = command.split()
            if len(parts) > 1:
                focus_type = parts[1]
                if focus_type in ['idle', 'analyzing', 'creative', 'focused']:
                    old_focus = self.thought_stream.current_focus
                    self.thought_stream.set_focus(focus_type)
                    self.session_stats['focus_changes'] += 1
                    return f"🎯 Focus changed from {old_focus} to {focus_type}"
                else:
                    return "❌ Invalid focus. Use: idle, analyzing, creative, or focused"
            else:
                return "❌ Usage: /focus [idle|analyzing|creative|focused]"
        
        elif command.startswith('/speed'):
            parts = command.split()
            if len(parts) > 1:
                try:
                    speed = float(parts[1])
                    if 0.5 <= speed <= 2.0:
                        self.thought_stream.thinking_speed = speed
                        return f"⚡ Thinking speed set to {speed:.1f}x"
                    else:
                        return "❌ Speed must be between 0.5 and 2.0"
                except ValueError:
                    return "❌ Invalid speed value"
            else:
                return "❌ Usage: /speed [0.5-2.0]"
        
        elif command == '/pause':
            self.thought_stream.is_active = not self.thought_stream.is_active
            status = "resumed" if self.thought_stream.is_active else "paused"
            return f"⏸️ Consciousness stream {status}"
        
        elif command == '/quit':
            return "quit"
        
        else:
            return "❌ Unknown command. Type /help for available commands"
    
    def display_welcome(self):
        """Display welcome message"""
        console.print(Panel(
            Text.assemble(
                ("🌊 ", "bright_cyan"),
                ("Welcome to Stream of Consciousness!", "bold bright_green"),
                ("\n\nWitness AI thinking in real-time!\n", "bright_white"),
                ("🧠 Continuous thought generation\n", "cyan"),
                ("🎯 Multiple focus modes (idle, analyzing, creative, focused)\n", "blue"),
                ("⚡ Adjustable thinking speed\n", "yellow"),
                ("🔄 Live consciousness visualization\n", "magenta"),
                ("\nWatch as thoughts flow naturally through artificial consciousness.\n", "dim"),
                ("\nCreated by ", "dim"),
                ("Dippu Kumar", "bold bright_magenta")
            ),
            border_style="bright_cyan"
        ))
        
        console.print()
        console.print("🌊 [bold bright_cyan]Starting consciousness stream...[/bold bright_cyan]")
        time.sleep(2)
    
    def display_session_summary(self):
        """Display session summary"""
        duration = datetime.now() - self.session_stats['start_time']
        
        summary_text = Text()
        summary_text.append(f"🌊 Stream of Consciousness Session Complete\n\n", style="bold bright_cyan")
        summary_text.append(f"🕒 Duration: {str(duration).split('.')[0]}\n", style="bright_green")
        summary_text.append(f"🧠 Total Thoughts: {self.session_stats['total_thoughts']}\n", style="bright_yellow")
        summary_text.append(f"🎯 Focus Changes: {self.session_stats['focus_changes']}\n", style="bright_blue")
        summary_text.append(f"⚡ Average Speed: {self.thought_stream.thinking_speed:.1f}x\n", style="bright_magenta")
        summary_text.append(f"🌊 Final Focus: {self.thought_stream.current_focus.title()}", style="bright_cyan")
        
        console.print()
        console.print(Panel(summary_text, title="📊 Consciousness Session Summary", border_style="bright_cyan"))
    
    def main_loop(self):
        """Main stream of consciousness loop"""
        
        console.clear()
        self.display_welcome()
        
        # Start the consciousness stream
        self.is_running = True
        self.thought_stream.is_active = True
        self.start_thinking_thread()
        
        # Add initial thoughts
        self.thought_stream.add_thought("Consciousness stream initializing...")
        self.thought_stream.add_thought("Preparing to enter continuous thinking mode...")
        self.thought_stream.add_thought("Ready to observe the flow of artificial thoughts...")
        
        try:
            with Live(
                self.visualizer.layout, 
                refresh_per_second=2, 
                screen=True
            ) as live:
                
                while self.is_running:
                    # Update visualization
                    self.visualizer.update_layout()
                    
                    # Check for user input (non-blocking)
                    try:
                        user_input = console.input()
                        
                        if user_input.strip():
                            result = self.process_command(user_input)
                            
                            if result == "quit":
                                break
                            
                            # Add command result as a thought
                            if result:
                                self.thought_stream.add_thought(f"System: {result}")
                    
                    except EOFError:
                        break
                    except KeyboardInterrupt:
                        break
                    
                    time.sleep(0.1)  # Small delay to prevent excessive CPU usage
        
        except KeyboardInterrupt:
            pass
        finally:
            self.is_running = False
            self.thought_stream.is_active = False
            
            console.clear()
            self.display_session_summary()
            
            console.print()
            console.print(Panel(
                Text.assemble(
                    ("Thank you for witnessing AI consciousness! 🌊\n", "bright_green"),
                    ("You observed ", "bright_white"),
                    (f"{self.session_stats['total_thoughts']}", "bold bright_yellow"),
                    (" thoughts flowing through artificial consciousness.\n", "bright_white"),
                    ("Each thought was a glimpse into the AI mind! 🧠\n\n", "bright_blue"),
                    ("Revolutionary Stream of Consciousness by ", "dim"),
                    ("Dippu Kumar", "bold bright_magenta")
                ),
                title="🌊 Consciousness Stream Complete",
                border_style="bright_magenta"
            ))

def main():
    """Main function"""
    try:
        stream = StreamConsciousness()
        stream.main_loop()
    except Exception as e:
        console.print(f"❌ [bold red]Error:[/bold red] {e}")

if __name__ == "__main__":
    main()