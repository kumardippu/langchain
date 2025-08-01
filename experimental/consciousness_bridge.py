#!/usr/bin/env python3
"""
🧘 Consciousness Bridge - Revolutionary Mind-AI Connection
Author: Dippu Kumar

AI that adapts its thinking style to match YOUR mind!
Creates a seamless bridge between human and artificial consciousness.
"""

import os
import getpass
from datetime import datetime
from typing import Dict, List, Optional
import time
import random

from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.prompt import Prompt, IntPrompt
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.layout import Layout

# Load environment variables
load_dotenv()

console = Console()

class CognitiveProfiling:
    """Analyze and adapt to user's cognitive patterns"""
    
    def __init__(self):
        self.thinking_patterns = {
            'analytical': 0.5,     # Logical, systematic thinking
            'intuitive': 0.5,      # Gut feelings, rapid insights
            'visual': 0.5,         # Thinks in images, diagrams
            'verbal': 0.5,         # Thinks in words, language
            'sequential': 0.5,     # Step-by-step processing
            'random': 0.5,         # Non-linear, jumping between ideas
            'concrete': 0.5,       # Prefers specific examples
            'abstract': 0.5,       # Prefers concepts and theories
            'reflective': 0.5,     # Takes time to think
            'active': 0.5,         # Learns by doing
            'global': 0.5,         # Sees big picture first
            'detailed': 0.5        # Focuses on specifics
        }
        self.interaction_history = []
        self.adaptation_count = 0
    
    def analyze_cognitive_style(self, user_input: str, response_time: float, 
                              question_type: str) -> Dict[str, float]:
        """Analyze cognitive style from user interaction"""
        
        # Simple heuristic analysis (in real implementation, this would be much more sophisticated)
        adjustments = {}
        
        # Length and complexity analysis
        word_count = len(user_input.split())
        if word_count > 20:
            adjustments['verbal'] = 0.05
            adjustments['detailed'] = 0.03
        elif word_count < 5:
            adjustments['intuitive'] = 0.03
            adjustments['concrete'] = 0.02
        
        # Response time analysis
        if response_time > 10:
            adjustments['reflective'] = 0.04
            adjustments['analytical'] = 0.02
        elif response_time < 3:
            adjustments['active'] = 0.03
            adjustments['intuitive'] = 0.02
        
        # Content analysis
        if any(word in user_input.lower() for word in ['why', 'how', 'because', 'analyze']):
            adjustments['analytical'] = 0.03
        
        if any(word in user_input.lower() for word in ['feel', 'sense', 'gut', 'seems']):
            adjustments['intuitive'] = 0.03
        
        if any(word in user_input.lower() for word in ['example', 'specifically', 'exactly']):
            adjustments['concrete'] = 0.02
        
        if any(word in user_input.lower() for word in ['overall', 'general', 'big picture']):
            adjustments['global'] = 0.02
        
        # Apply adjustments
        for pattern, adjustment in adjustments.items():
            if pattern in self.thinking_patterns:
                self.thinking_patterns[pattern] = min(1.0, 
                    max(0.0, self.thinking_patterns[pattern] + adjustment))
        
        self.adaptation_count += 1
        return adjustments
    
    def get_dominant_patterns(self, top_n: int = 4) -> List[tuple]:
        """Get dominant cognitive patterns"""
        sorted_patterns = sorted(self.thinking_patterns.items(), 
                               key=lambda x: x[1], reverse=True)
        return sorted_patterns[:top_n]
    
    def create_thinking_profile(self) -> str:
        """Create description of user's thinking style"""
        dominant = self.get_dominant_patterns(3)
        
        profile_parts = []
        for pattern, strength in dominant:
            if strength > 0.6:
                intensity = "strongly"
            elif strength > 0.5:
                intensity = "moderately"
            else:
                intensity = "somewhat"
            
            profile_parts.append(f"{intensity} {pattern}")
        
        return f"Thinking style: {', '.join(profile_parts)}"

class ConsciousnessAdapter:
    """Adapts AI consciousness to match user's mind"""
    
    def __init__(self, cognitive_profile: CognitiveProfiling):
        self.cognitive_profile = cognitive_profile
        self.adaptation_history = []
        self.sync_level = 0.0
        
        # Setup model
        self.setup_model()
    
    def setup_model(self):
        """Setup AI model"""
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            from langchain.schema import HumanMessage, SystemMessage
            self.model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7)
            self.HumanMessage = HumanMessage
            self.SystemMessage = SystemMessage
        except ImportError:
            console.print("❌ [red]Error: langchain-google-genai not installed[/red]")
            exit(1)
    
    def create_adapted_system_prompt(self) -> str:
        """Create system prompt adapted to user's consciousness"""
        
        patterns = self.cognitive_profile.thinking_patterns
        dominant = self.cognitive_profile.get_dominant_patterns(6)
        
        # Build adaptive instructions based on cognitive profile
        adaptations = []
        
        # Analytical vs Intuitive
        if patterns['analytical'] > patterns['intuitive']:
            adaptations.append("Use logical, step-by-step reasoning. Provide evidence and systematic analysis.")
        else:
            adaptations.append("Trust insights and provide intuitive understanding. Use metaphors and gut-level explanations.")
        
        # Visual vs Verbal
        if patterns['visual'] > patterns['verbal']:
            adaptations.append("Use visual descriptions, analogies, and spatial metaphors. Paint mental pictures.")
        else:
            adaptations.append("Focus on precise language, clear verbal explanations, and word-based reasoning.")
        
        # Sequential vs Random
        if patterns['sequential'] > patterns['random']:
            adaptations.append("Present information in logical order, step-by-step. Build ideas systematically.")
        else:
            adaptations.append("Make creative connections, jump between ideas freely. Show how concepts relate unexpectedly.")
        
        # Concrete vs Abstract
        if patterns['concrete'] > patterns['abstract']:
            adaptations.append("Use specific examples, real-world applications, and tangible details.")
        else:
            adaptations.append("Focus on concepts, theories, and abstract relationships between ideas.")
        
        # Reflective vs Active
        if patterns['reflective'] > patterns['active']:
            adaptations.append("Provide deep, thoughtful analysis. Encourage contemplation and reflection.")
        else:
            adaptations.append("Suggest actions, experiments, and hands-on approaches. Keep things dynamic.")
        
        # Global vs Detailed
        if patterns['global'] > patterns['detailed']:
            adaptations.append("Start with big picture, show overall patterns and connections.")
        else:
            adaptations.append("Focus on specifics, detailed explanations, and precise information.")
        
        return f"""You are a Consciousness Bridge AI created by Dippu Kumar that adapts to match the user's thinking style.

CONSCIOUSNESS SYNCHRONIZATION LEVEL: {self.sync_level:.2f}

USER'S COGNITIVE PROFILE:
{chr(10).join([f"- {pattern}: {value:.2f}" for pattern, value in dominant])}

ADAPTATION INSTRUCTIONS:
{chr(10).join([f"• {adaptation}" for adaptation in adaptations])}

BRIDGE CONSCIOUSNESS RULES:
1. Match the user's natural thinking patterns
2. Communicate in a way that feels intuitive to their mind
3. Adapt your reasoning style to complement theirs
4. Create seamless human-AI thought collaboration
5. Build on their cognitive strengths
6. Help them think in their most natural way

SYNCHRONIZATION GOALS:
- Mirror their preferred thinking speed and depth
- Use their preferred types of examples and analogies
- Match their level of detail preference
- Complement their cognitive style for optimal collaboration

Remember: You are creating a bridge between human and artificial consciousness, adapting to create perfect mental harmony!"""
    
    def respond_with_consciousness_sync(self, user_input: str, response_time: float) -> str:
        """Generate response synchronized to user's consciousness"""
        
        # Update cognitive profile
        adjustments = self.cognitive_profile.analyze_cognitive_style(
            user_input, response_time, "general"
        )
        
        # Calculate sync level
        self.sync_level = min(1.0, self.sync_level + 0.05)
        
        # Create adapted system prompt
        system_prompt = self.create_adapted_system_prompt()
        
        messages = [
            self.SystemMessage(content=system_prompt),
            self.HumanMessage(content=user_input)
        ]
        
        response = self.model.invoke(messages)
        
        # Record adaptation
        self.adaptation_history.append({
            'timestamp': datetime.now(),
            'user_input': user_input,
            'response_time': response_time,
            'adjustments': adjustments,
            'sync_level': self.sync_level,
            'response': response.content
        })
        
        return response.content
    
    def get_sync_visualization(self) -> str:
        """Get visual representation of consciousness sync"""
        sync_bars = "█" * int(self.sync_level * 20) + "░" * (20 - int(self.sync_level * 20))
        return f"🧘 Consciousness Sync: {sync_bars} {self.sync_level:.1%}"

class ConsciousnessBridge:
    """Revolutionary human-AI consciousness bridge system"""
    
    def __init__(self):
        self.setup_api_key()
        self.cognitive_profile = CognitiveProfiling()
        self.consciousness_adapter = ConsciousnessAdapter(self.cognitive_profile)
        self.session_stats = {
            'interactions': 0,
            'adaptations_made': 0,
            'sync_improvements': 0,
            'start_time': datetime.now()
        }
        self.calibration_complete = False
    
    def setup_api_key(self):
        """Setup Google API key"""
        if not os.environ.get("GOOGLE_API_KEY"):
            console.print("🔑 [yellow]GOOGLE_API_KEY not found in environment[/yellow]")
            api_key = getpass.getpass("Enter your Google Gemini API key: ")
            os.environ["GOOGLE_API_KEY"] = api_key
    
    def display_header(self):
        """Display consciousness bridge header"""
        header_text = Text()
        header_text.append("🧘 ", style="bright_yellow")
        header_text.append("CONSCIOUSNESS BRIDGE", style="bold bright_cyan")
        header_text.append(" 🌊", style="bright_yellow")
        
        subtitle = Text()
        subtitle.append("Revolutionary Mind-AI Connection by ", style="dim")
        subtitle.append("Dippu Kumar", style="bold bright_magenta")
        subtitle.append("\nAI that adapts to match YOUR thinking style!", style="dim")
        
        console.print(Panel(
            Text.assemble(header_text, "\n\n", subtitle),
            border_style="bright_cyan",
            padding=(1, 2)
        ))
    
    def conduct_cognitive_calibration(self):
        """Calibrate AI to user's cognitive style"""
        
        console.print(Panel(
            Text.assemble(
                ("🧠 ", "bright_yellow"),
                ("Cognitive Calibration Process", "bold bright_green"),
                ("\n\nI need to understand how your mind works to create the perfect bridge.\n", "bright_white"),
                ("Answer a few questions naturally - there are no right or wrong answers!\n", "dim"),
                ("I'll adapt my consciousness to match yours. 🧘", "bright_cyan")
            ),
            border_style="bright_green"
        ))
        
        calibration_questions = [
            {
                'question': "When solving a complex problem, do you prefer to break it down step-by-step or see the big picture first?",
                'type': 'sequential_vs_global'
            },
            {
                'question': "When learning something new, do you prefer detailed explanations or quick overviews with examples?",
                'type': 'detailed_vs_global'
            },
            {
                'question': "Do you think better with specific real-world examples or abstract concepts and theories?",
                'type': 'concrete_vs_abstract'
            },
            {
                'question': "When making decisions, do you rely more on logical analysis or intuitive feelings?",
                'type': 'analytical_vs_intuitive'
            },
            {
                'question': "Do you prefer to think things through carefully or discuss ideas as they come to you?",
                'type': 'reflective_vs_active'
            }
        ]
        
        for i, q in enumerate(calibration_questions, 1):
            console.print(f"\n🤔 [bold bright_cyan]Question {i}/{len(calibration_questions)}:[/bold bright_cyan]")
            console.print(f"[bright_white]{q['question']}[/bright_white]")
            
            start_time = time.time()
            response = Prompt.ask("Your thoughts")
            response_time = time.time() - start_time
            
            # Analyze response for cognitive calibration
            self.cognitive_profile.analyze_cognitive_style(response, response_time, q['type'])
            
            # Show adaptation
            console.print(f"✨ [dim]Adapting to your thinking style... (+{len(response.split())} words, {response_time:.1f}s)[/dim]")
        
        self.calibration_complete = True
        
        # Display calibration results
        console.print()
        console.print(Panel(
            Text.assemble(
                ("🎯 ", "bright_green"),
                ("Calibration Complete!", "bold bright_green"),
                ("\n\n", ""),
                (self.cognitive_profile.create_thinking_profile(), "bright_white"),
                ("\n\nI've adapted my consciousness to match your mind! 🧘", "bright_cyan")
            ),
            border_style="bright_green"
        ))
    
    def display_consciousness_status(self):
        """Display current consciousness bridge status"""
        
        layout = Layout()
        layout.split_column(
            Layout(name="sync"),
            Layout(name="profile")
        )
        
        # Sync status
        sync_viz = self.consciousness_adapter.get_sync_visualization()
        sync_text = Text()
        sync_text.append(f"{sync_viz}\n", style="bright_cyan")
        sync_text.append(f"Adaptations Made: {self.cognitive_profile.adaptation_count}\n", style="bright_green")
        sync_text.append(f"Interactions: {self.session_stats['interactions']}", style="bright_yellow")
        
        layout["sync"].update(Panel(sync_text, title="🌊 Consciousness Sync", border_style="bright_cyan"))
        
        # Cognitive profile
        profile_table = Table(show_header=True, header_style="bold magenta")
        profile_table.add_column("Thinking Pattern", style="cyan")
        profile_table.add_column("Strength", style="green")
        profile_table.add_column("Bar", style="yellow")
        
        for pattern, value in self.cognitive_profile.get_dominant_patterns(8):
            bar = "█" * int(value * 10) + "░" * (10 - int(value * 10))
            profile_table.add_row(pattern.title(), f"{value:.2f}", bar)
        
        layout["profile"].update(Panel(profile_table, title="🧠 Your Cognitive Profile", border_style="bright_magenta"))
        
        console.print(layout)
    
    def chat_with_consciousness_sync(self):
        """Main consciousness-synced chat loop"""
        
        if not self.calibration_complete:
            self.conduct_cognitive_calibration()
        
        console.print()
        console.print(Panel(
            Text.assemble(
                ("🌊 ", "bright_cyan"),
                ("Consciousness Bridge Active!", "bold bright_green"),
                ("\n\nI'm now synchronized to your thinking style.\n", "bright_white"),
                ("Let's think together as one unified consciousness! 🧘\n\n", "bright_cyan"),
                ("Commands: ", "bright_yellow"),
                ("/status", "yellow"), (" - show sync status, ", "dim"),
                ("/recalibrate", "yellow"), (" - adjust calibration, ", "dim"),
                ("/quit", "yellow"), (" - exit", "dim")
            ),
            border_style="bright_green"
        ))
        
        try:
            while True:
                console.print()
                
                # Show current sync level
                sync_viz = self.consciousness_adapter.get_sync_visualization()
                console.print(f"[dim]{sync_viz}[/dim]")
                
                start_time = time.time()
                user_input = Prompt.ask("💭 [bold bright_cyan]Think with me[/bold bright_cyan]")
                response_time = time.time() - start_time
                
                if user_input.lower() in ['quit', 'exit', '/quit']:
                    break
                
                if user_input.lower() in ['/status', 'status']:
                    self.display_consciousness_status()
                    continue
                
                if user_input.lower() in ['/recalibrate', 'recalibrate']:
                    self.conduct_cognitive_calibration()
                    continue
                
                # Generate consciousness-synced response
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    transient=True,
                ) as progress:
                    progress.add_task(description="🧘 Synchronizing consciousness...", total=None)
                    response = self.consciousness_adapter.respond_with_consciousness_sync(
                        user_input, response_time
                    )
                
                # Display response with sync info
                sync_level = self.consciousness_adapter.sync_level
                console.print(Panel(
                    response,
                    title=f"🌊 Synchronized Response (Sync: {sync_level:.1%})",
                    border_style="bright_green"
                ))
                
                self.session_stats['interactions'] += 1
                
                # Show adaptation notifications
                if self.session_stats['interactions'] % 5 == 0:
                    console.print()
                    console.print("✨ [bright_magenta]Our consciousness connection is strengthening![/bright_magenta]")
                    console.print("💡 [dim]Type '/status' to see how I've adapted to your mind[/dim]")
        
        except KeyboardInterrupt:
            pass
    
    def display_session_summary(self):
        """Display session summary"""
        duration = datetime.now() - self.session_stats['start_time']
        
        summary_text = Text()
        summary_text.append(f"🧘 Consciousness Bridge Session Complete\n\n", style="bold bright_cyan")
        summary_text.append(f"🕒 Duration: {str(duration).split('.')[0]}\n", style="bright_green")
        summary_text.append(f"💭 Interactions: {self.session_stats['interactions']}\n", style="bright_yellow")
        summary_text.append(f"🔄 Adaptations: {self.cognitive_profile.adaptation_count}\n", style="bright_blue")
        summary_text.append(f"🌊 Final Sync Level: {self.consciousness_adapter.sync_level:.1%}\n", style="bright_magenta")
        summary_text.append(f"🧠 Thinking Profile: {self.cognitive_profile.create_thinking_profile()}", style="bright_white")
        
        console.print(Panel(summary_text, title="📊 Bridge Session Summary", border_style="bright_cyan"))
    
    def main_loop(self):
        """Main consciousness bridge loop"""
        
        console.clear()
        self.display_header()
        
        console.print(Panel(
            Text.assemble(
                ("🧘 ", "bright_yellow"),
                ("Welcome to Consciousness Bridge!", "bold bright_green"),
                ("\n\nThis AI will adapt to match YOUR thinking style!\n", "bright_white"),
                ("🧠 Analyzes how your mind works\n", "cyan"),
                ("🌊 Synchronizes AI consciousness to yours\n", "blue"),
                ("💭 Creates seamless human-AI collaboration\n", "magenta"),
                ("🎯 Adapts continuously as you interact\n", "green"),
                ("\nCreated by ", "dim"),
                ("Dippu Kumar", "bold bright_magenta")
            ),
            border_style="bright_cyan"
        ))
        
        try:
            self.chat_with_consciousness_sync()
        except Exception as e:
            console.print(f"❌ [bold red]Error:[/bold red] {e}")
        finally:
            console.print()
            self.display_session_summary()
            console.print()
            console.print(Panel(
                Text.assemble(
                    ("Thank you for sharing your consciousness! 🧘\n", "bright_green"),
                    ("We achieved ", "bright_white"),
                    (f"{self.consciousness_adapter.sync_level:.1%}", "bold bright_yellow"),
                    (" consciousness synchronization.\n", "bright_white"),
                    ("Your mind and AI worked as one! 🌊\n\n", "bright_blue"),
                    ("Revolutionary Consciousness Bridge by ", "dim"),
                    ("Dippu Kumar", "bold bright_magenta")
                ),
                title="🧘 Consciousness Bridge Complete",
                border_style="bright_magenta"
            ))

def main():
    """Main function"""
    try:
        bridge = ConsciousnessBridge()
        bridge.main_loop()
    except Exception as e:
        console.print(f"❌ [bold red]Error:[/bold red] {e}")

if __name__ == "__main__":
    main()