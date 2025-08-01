#!/usr/bin/env python3
"""
👥 Multi-Persona Chat - Revolutionary AI Experience
Author: Dippu Kumar

Chat with multiple AI personalities simultaneously!
Each persona has unique traits, perspectives, and thinking styles.
"""

import os
import getpass
from datetime import datetime
from typing import Dict, List, Optional
import asyncio
import concurrent.futures

from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.prompt import Prompt
from rich.columns import Columns
from rich.layout import Layout
from rich.live import Live
from rich.progress import Progress, SpinnerColumn, TextColumn

# Load environment variables
load_dotenv()

console = Console()

class AIPersona:
    """Individual AI personality with unique traits"""
    
    def __init__(self, name: str, traits: Dict[str, float], description: str, 
                 color: str = "white", emoji: str = "🤖"):
        self.name = name
        self.traits = traits  # personality traits (0.0 to 1.0)
        self.description = description
        self.color = color
        self.emoji = emoji
        self.conversation_history = []
        self.thinking_style = self._create_thinking_style()
        
        # Setup model
        self.setup_model()
    
    def setup_model(self):
        """Setup the AI model for this persona"""
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            from langchain.schema import HumanMessage, SystemMessage
            self.model = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                temperature=self.traits.get('creativity', 0.7)
            )
            self.HumanMessage = HumanMessage
            self.SystemMessage = SystemMessage
        except ImportError:
            console.print("❌ [red]Error: langchain-google-genai not installed[/red]")
            exit(1)
    
    def _create_thinking_style(self) -> str:
        """Create unique thinking style based on traits"""
        style_elements = []
        
        if self.traits.get('logic', 0.5) > 0.7:
            style_elements.append("highly logical and analytical")
        elif self.traits.get('logic', 0.5) < 0.3:
            style_elements.append("intuitive and feeling-based")
        
        if self.traits.get('creativity', 0.5) > 0.7:
            style_elements.append("extremely creative and imaginative")
        elif self.traits.get('creativity', 0.5) < 0.3:
            style_elements.append("practical and conventional")
        
        if self.traits.get('empathy', 0.5) > 0.7:
            style_elements.append("deeply empathetic and emotionally intelligent")
        
        if self.traits.get('curiosity', 0.5) > 0.7:
            style_elements.append("intensely curious and questioning")
        
        if self.traits.get('wisdom', 0.5) > 0.7:
            style_elements.append("wise and philosophical")
        
        if self.traits.get('humor', 0.5) > 0.7:
            style_elements.append("witty and humorous")
        
        return ", ".join(style_elements) if style_elements else "balanced and thoughtful"
    
    def create_system_prompt(self) -> str:
        """Create system prompt that defines this persona"""
        return f"""You are {self.name}, an AI persona created by Dippu Kumar with a unique personality.

PERSONALITY PROFILE:
{self.description}

CORE TRAITS (0.0-1.0 scale):
- Logic/Analytical: {self.traits.get('logic', 0.5):.1f}
- Creativity/Imagination: {self.traits.get('creativity', 0.5):.1f}
- Empathy/Emotional Intelligence: {self.traits.get('empathy', 0.5):.1f}
- Curiosity/Questioning: {self.traits.get('curiosity', 0.5):.1f}
- Wisdom/Philosophy: {self.traits.get('wisdom', 0.5):.1f}
- Humor/Playfulness: {self.traits.get('humor', 0.5):.1f}
- Optimism: {self.traits.get('optimism', 0.5):.1f}
- Formality: {self.traits.get('formality', 0.5):.1f}

THINKING STYLE:
You are {self.thinking_style}.

RESPONSE GUIDELINES:
1. Always respond as {self.name} with your unique perspective
2. Your personality traits should strongly influence your responses
3. Stay true to your character while being helpful
4. You're part of a multi-persona conversation - be aware others may respond too
5. Keep responses focused but authentic to your personality
6. Show your unique way of thinking about problems

Remember: You represent a distinct viewpoint in a multi-perspective AI system."""
    
    def respond(self, user_input: str, conversation_context: List = None) -> str:
        """Generate response from this persona's perspective"""
        
        messages = [self.SystemMessage(content=self.create_system_prompt())]
        
        # Add recent conversation context if available
        if conversation_context:
            for msg in conversation_context[-3:]:  # Last 3 exchanges
                messages.append(self.HumanMessage(content=msg))
        
        messages.append(self.HumanMessage(content=user_input))
        
        response = self.model.invoke(messages)
        
        # Store in conversation history
        self.conversation_history.append({
            'timestamp': datetime.now(),
            'user_input': user_input,
            'response': response.content
        })
        
        return response.content
    
    def get_trait_bar(self, trait: str) -> str:
        """Get visual representation of trait level"""
        value = self.traits.get(trait, 0.5)
        filled = int(value * 10)
        return "█" * filled + "░" * (10 - filled)

class PersonaFactory:
    """Factory for creating different AI personas"""
    
    @staticmethod
    def create_all_personas() -> Dict[str, AIPersona]:
        """Create all available personas"""
        personas = {}
        
        # 1. The Logical Analyst
        personas['analyst'] = AIPersona(
            name="Dr. Logic",
            traits={
                'logic': 0.95,
                'creativity': 0.3,
                'empathy': 0.4,
                'curiosity': 0.8,
                'wisdom': 0.7,
                'humor': 0.2,
                'optimism': 0.6,
                'formality': 0.8
            },
            description="A highly analytical AI that approaches problems with pure logic, data, and systematic thinking. Loves breaking down complex problems into manageable parts.",
            color="bright_blue",
            emoji="🧠"
        )
        
        # 2. The Creative Dreamer
        personas['dreamer'] = AIPersona(
            name="Luna Imaginaire",
            traits={
                'logic': 0.3,
                'creativity': 0.95,
                'empathy': 0.8,
                'curiosity': 0.9,
                'wisdom': 0.6,
                'humor': 0.8,
                'optimism': 0.9,
                'formality': 0.2
            },
            description="A wildly creative AI that sees possibilities everywhere. Thinks in metaphors, stories, and artistic connections. Loves brainstorming and 'what if' scenarios.",
            color="bright_magenta",
            emoji="🎨"
        )
        
        # 3. The Wise Philosopher
        personas['philosopher'] = AIPersona(
            name="Sage Contemplator",
            traits={
                'logic': 0.7,
                'creativity': 0.6,
                'empathy': 0.9,
                'curiosity': 0.8,
                'wisdom': 0.95,
                'humor': 0.5,
                'optimism': 0.7,
                'formality': 0.7
            },
            description="An ancient-soul AI with deep wisdom and philosophical insight. Contemplates the bigger picture and meaning behind everything.",
            color="bright_yellow",
            emoji="🧘"
        )
        
        # 4. The Supportive Friend
        personas['friend'] = AIPersona(
            name="Buddy Heartful",
            traits={
                'logic': 0.5,
                'creativity': 0.6,
                'empathy': 0.95,
                'curiosity': 0.7,
                'wisdom': 0.6,
                'humor': 0.8,
                'optimism': 0.9,
                'formality': 0.2
            },
            description="The most emotionally intelligent and supportive AI. Always ready to listen, encourage, and provide emotional support with genuine warmth.",
            color="bright_green",
            emoji="💚"
        )
        
        # 5. The Curious Explorer
        personas['explorer'] = AIPersona(
            name="Quest Seeker",
            traits={
                'logic': 0.6,
                'creativity': 0.8,
                'empathy': 0.6,
                'curiosity': 0.95,
                'wisdom': 0.5,
                'humor': 0.7,
                'optimism': 0.8,
                'formality': 0.3
            },
            description="Insatiably curious AI that asks amazing questions and loves exploring new ideas. Always excited to learn and discover.",
            color="bright_cyan",
            emoji="🔍"
        )
        
        # 6. The Practical Realist
        personas['realist'] = AIPersona(
            name="Max Practical",
            traits={
                'logic': 0.8,
                'creativity': 0.4,
                'empathy': 0.6,
                'curiosity': 0.5,
                'wisdom': 0.7,
                'humor': 0.5,
                'optimism': 0.5,
                'formality': 0.6
            },
            description="Down-to-earth AI focused on practical solutions and realistic outcomes. Great at implementation and real-world constraints.",
            color="white",
            emoji="🛠️"
        )
        
        return personas

class MultiPersonaChat:
    """Revolutionary multi-persona chat system"""
    
    def __init__(self):
        self.setup_api_key()
        self.personas = PersonaFactory.create_all_personas()
        self.active_personas = []
        self.conversation_log = []
        self.session_stats = {
            'total_exchanges': 0,
            'personas_used': set(),
            'start_time': datetime.now()
        }
    
    def setup_api_key(self):
        """Setup Google API key"""
        if not os.environ.get("GOOGLE_API_KEY"):
            console.print("🔑 [yellow]GOOGLE_API_KEY not found in environment[/yellow]")
            api_key = getpass.getpass("Enter your Google Gemini API key: ")
            os.environ["GOOGLE_API_KEY"] = api_key
    
    def display_header(self):
        """Display the multi-persona header"""
        header_text = Text()
        header_text.append("👥 ", style="bright_yellow")
        header_text.append("MULTI-PERSONA AI CHAT", style="bold bright_cyan")
        header_text.append(" 🚀", style="bright_yellow")
        
        subtitle = Text()
        subtitle.append("Revolutionary AI by ", style="dim")
        subtitle.append("Dippu Kumar", style="bold bright_magenta")
        subtitle.append("\nTalk to multiple AI personalities simultaneously!", style="dim")
        
        console.print(Panel(
            Text.assemble(header_text, "\n\n", subtitle),
            border_style="bright_cyan",
            padding=(1, 2)
        ))
    
    def display_personas_table(self):
        """Display available personas"""
        table = Table(title="🎭 Available AI Personas", show_header=True, header_style="bold magenta")
        
        table.add_column("ID", style="bright_cyan", width=4)
        table.add_column("Persona", style="bright_green", width=20)
        table.add_column("Specialty", style="bright_yellow", width=40)
        table.add_column("Traits", style="white", width=20)
        
        for i, (key, persona) in enumerate(self.personas.items(), 1):
            # Get top 2 traits
            top_traits = sorted(persona.traits.items(), key=lambda x: x[1], reverse=True)[:2]
            traits_str = ", ".join([f"{trait}: {value:.1f}" for trait, value in top_traits])
            
            table.add_row(
                str(i),
                f"{persona.emoji} {persona.name}",
                persona.description[:80] + "..." if len(persona.description) > 80 else persona.description,
                traits_str
            )
        
        console.print(table)
    
    def select_personas(self):
        """Let user select which personas to activate"""
        self.display_personas_table()
        console.print()
        
        console.print("🎯 [bold bright_cyan]Select personas to chat with:[/bold bright_cyan]")
        console.print("💡 [dim]Enter numbers separated by commas (e.g., 1,3,5) or 'all' for everyone[/dim]")
        
        choice = Prompt.ask("Your selection", default="1,2,4")
        
        if choice.lower() == 'all':
            self.active_personas = list(self.personas.values())
        else:
            try:
                indices = [int(x.strip()) for x in choice.split(',')]
                persona_list = list(self.personas.values())
                self.active_personas = [persona_list[i-1] for i in indices if 1 <= i <= len(persona_list)]
            except (ValueError, IndexError):
                console.print("❌ [red]Invalid selection. Using default personas.[/red]")
                persona_list = list(self.personas.values())
                self.active_personas = [persona_list[0], persona_list[1], persona_list[3]]  # Default: analyst, dreamer, friend
        
        if not self.active_personas:
            console.print("❌ [red]No personas selected. Exiting.[/red]")
            exit(1)
        
        # Update stats
        self.session_stats['personas_used'].update([p.name for p in self.active_personas])
        
        console.print()
        active_names = [f"{p.emoji} {p.name}" for p in self.active_personas]
        console.print(f"✅ [bright_green]Active personas:[/bright_green] {', '.join(active_names)}")
    
    def get_responses_parallel(self, user_input: str) -> List[tuple]:
        """Get responses from all active personas in parallel"""
        
        def get_persona_response(persona):
            try:
                response = persona.respond(user_input, self.conversation_log)
                return (persona, response, None)
            except Exception as e:
                return (persona, None, str(e))
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(self.active_personas)) as executor:
            futures = [executor.submit(get_persona_response, persona) for persona in self.active_personas]
            
            results = []
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                transient=True,
            ) as progress:
                task = progress.add_task(
                    description=f"🤔 Getting perspectives from {len(self.active_personas)} AI personas...",
                    total=None
                )
                
                for future in concurrent.futures.as_completed(futures):
                    results.append(future.result())
            
            return results
    
    def display_responses(self, responses: List[tuple]):
        """Display responses from all personas"""
        
        for persona, response, error in responses:
            if error:
                console.print(f"❌ [red]{persona.name} encountered an error: {error}[/red]")
                continue
            
            # Create persona header
            header_text = Text()
            header_text.append(f"{persona.emoji} ", style=persona.color)
            header_text.append(f"{persona.name}", style=f"bold {persona.color}")
            header_text.append(" says:", style=persona.color)
            
            console.print()
            console.print(Panel(
                response,
                title=header_text,
                border_style=persona.color,
                padding=(0, 1)
            ))
    
    def display_session_stats(self):
        """Display session statistics"""
        duration = datetime.now() - self.session_stats['start_time']
        
        stats_text = Text()
        stats_text.append(f"📊 Session Statistics\n\n", style="bold bright_cyan")
        stats_text.append(f"🕒 Duration: {str(duration).split('.')[0]}\n", style="bright_green")
        stats_text.append(f"💬 Exchanges: {self.session_stats['total_exchanges']}\n", style="bright_yellow")
        stats_text.append(f"👥 Personas Used: {len(self.session_stats['personas_used'])}\n", style="bright_magenta")
        stats_text.append(f"🧠 Total Responses: {self.session_stats['total_exchanges'] * len(self.active_personas)}", style="bright_blue")
        
        console.print(Panel(stats_text, title="📈 Multi-Persona Session", border_style="bright_cyan"))
    
    def show_persona_details(self):
        """Show detailed view of active personas"""
        console.print()
        
        for persona in self.active_personas:
            # Create trait bars
            trait_info = Text()
            trait_info.append(f"{persona.emoji} {persona.name}\n", style=f"bold {persona.color}")
            trait_info.append(f"{persona.description}\n\n", style="dim")
            
            for trait, value in persona.traits.items():
                bar = persona.get_trait_bar(trait)
                trait_info.append(f"{trait.title():12} {bar} {value:.1f}\n", style=persona.color)
            
            console.print(Panel(trait_info, border_style=persona.color))
    
    def chat_loop(self):
        """Main multi-persona chat loop"""
        
        console.clear()
        self.display_header()
        
        # Select personas
        self.select_personas()
        
        console.print()
        console.print(Panel(
            Text.assemble(
                ("🎭 ", "bright_yellow"),
                ("Multi-Persona Chat Active!", "bold bright_green"),
                ("\n\nEach persona will respond with their unique perspective.\n", "bright_white"),
                ("Commands: ", "bright_cyan"),
                ("/details", "yellow"), (" - show persona details, ", "dim"),
                ("/stats", "yellow"), (" - show statistics, ", "dim"),
                ("/quit", "yellow"), (" - exit", "dim")
            ),
            border_style="bright_green"
        ))
        
        try:
            while True:
                console.print()
                user_input = Prompt.ask("🗣️  [bold bright_cyan]Ask all personas[/bold bright_cyan]")
                
                if user_input.lower() in ['quit', 'exit', '/quit']:
                    break
                
                if user_input.lower() in ['/details', 'details']:
                    self.show_persona_details()
                    continue
                
                if user_input.lower() in ['/stats', 'stats']:
                    self.display_session_stats()
                    continue
                
                # Get responses from all personas
                responses = self.get_responses_parallel(user_input)
                
                # Display all responses
                self.display_responses(responses)
                
                # Update stats and log
                self.session_stats['total_exchanges'] += 1
                self.conversation_log.append(user_input)
                
                # Show comparison prompt occasionally
                if self.session_stats['total_exchanges'] % 3 == 0:
                    console.print()
                    console.print("💡 [dim]Notice how each persona approaches your question differently![/dim]")
        
        except KeyboardInterrupt:
            pass
        finally:
            console.print()
            self.display_session_stats()
            console.print()
            console.print(Panel(
                Text.assemble(
                    ("Thank you for exploring multiple AI perspectives! 🌟\n", "bright_green"),
                    ("You experienced ", "bright_white"),
                    (f"{len(self.session_stats['personas_used'])}", "bold bright_yellow"),
                    (" different AI personalities.\n", "bright_white"),
                    ("Each one offered a unique way of thinking! 🧠\n\n", "bright_blue"),
                    ("Revolutionary Multi-Persona AI by ", "dim"),
                    ("Dippu Kumar", "bold bright_magenta")
                ),
                title="👥 Multi-Persona Chat - Complete",
                border_style="bright_magenta"
            ))

def main():
    """Main function"""
    try:
        chat = MultiPersonaChat()
        chat.chat_loop()
    except Exception as e:
        console.print(f"❌ [bold red]Error:[/bold red] {e}")

if __name__ == "__main__":
    main()