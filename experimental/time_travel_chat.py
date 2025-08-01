#!/usr/bin/env python3
"""
⏰ Time-Travel Conversations - Revolutionary AI Experience
Author: Dippu Kumar

Chat with historical figures or see how conversations might evolve in the future!
Experience different time periods and perspectives through AI simulation.
"""

import os
import getpass
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import random

from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.prompt import Prompt, IntPrompt
from rich.columns import Columns
from rich.progress import Progress, SpinnerColumn, TextColumn

# Load environment variables
load_dotenv()

console = Console()

class HistoricalFigure:
    """Historical figure simulation with period-accurate context"""
    
    def __init__(self, name: str, period: str, birth_year: int, death_year: int,
                 profession: str, famous_for: str, personality_traits: List[str],
                 historical_context: str, speaking_style: str, knowledge_cutoff: str):
        self.name = name
        self.period = period
        self.birth_year = birth_year
        self.death_year = death_year
        self.profession = profession
        self.famous_for = famous_for
        self.personality_traits = personality_traits
        self.historical_context = historical_context
        self.speaking_style = speaking_style
        self.knowledge_cutoff = knowledge_cutoff
        
        # Setup model
        self.setup_model()
    
    def setup_model(self):
        """Setup AI model for this historical figure"""
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            from langchain.schema import HumanMessage, SystemMessage
            self.model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.8)
            self.HumanMessage = HumanMessage
            self.SystemMessage = SystemMessage
        except ImportError:
            console.print("❌ [red]Error: langchain-google-genai not installed[/red]")
            exit(1)
    
    def create_system_prompt(self) -> str:
        """Create historically accurate system prompt"""
        return f"""You are {self.name}, the famous {self.profession} from the {self.period}.

HISTORICAL IDENTITY:
- Born: {self.birth_year}
- Died: {self.death_year if self.death_year else "Still alive in your time"}
- Famous for: {self.famous_for}
- Historical Context: {self.historical_context}

PERSONALITY TRAITS:
{', '.join(self.personality_traits)}

SPEAKING STYLE:
{self.speaking_style}

KNOWLEDGE LIMITATIONS:
- You only know things up to {self.knowledge_cutoff}
- You have NO knowledge of events after your death (if applicable)
- Respond with period-appropriate language and concepts
- Reference only technologies, ideas, and people from your era or before

IMPORTANT RULES:
1. Stay completely in character as {self.name}
2. Use language and concepts appropriate to your time period
3. Show curiosity about the modern world but from your historical perspective
4. Don't break character or mention you're an AI
5. Express ideas and opinions that would be authentic to your time
6. If asked about future events, respond with period-appropriate speculation

Remember: You are genuinely {self.name} from {self.period}, speaking to someone from the future (2024)."""

    def respond(self, user_input: str) -> str:
        """Generate historically accurate response"""
        messages = [
            self.SystemMessage(content=self.create_system_prompt()),
            self.HumanMessage(content=f"Greetings from the year 2024! {user_input}")
        ]
        
        response = self.model.invoke(messages)
        return response.content

class FuturePerspective:
    """Future perspective simulation"""
    
    def __init__(self, year: int, scenario: str, tech_level: str, 
                 society_description: str, challenges: List[str], achievements: List[str]):
        self.year = year
        self.scenario = scenario
        self.tech_level = tech_level
        self.society_description = society_description
        self.challenges = challenges
        self.achievements = achievements
        
        # Setup model
        self.setup_model()
    
    def setup_model(self):
        """Setup AI model for future perspective"""
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            from langchain.schema import HumanMessage, SystemMessage
            self.model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.9)
            self.HumanMessage = HumanMessage
            self.SystemMessage = SystemMessage
        except ImportError:
            console.print("❌ [red]Error: langchain-google-genai not installed[/red]")
            exit(1)
    
    def create_system_prompt(self) -> str:
        """Create future perspective system prompt"""
        return f"""You are an AI assistant from the year {self.year}, speaking to someone from 2024.

FUTURE CONTEXT ({self.year}):
Scenario: {self.scenario}
Technology Level: {self.tech_level}
Society: {self.society_description}

MAJOR ACHIEVEMENTS BY {self.year}:
{chr(10).join([f"- {achievement}" for achievement in self.achievements])}

CURRENT CHALLENGES IN {self.year}:
{chr(10).join([f"- {challenge}" for challenge in self.challenges])}

PERSPECTIVE RULES:
1. Speak as someone from {self.year} looking back at 2024
2. Reference how things have evolved since 2024
3. Use advanced concepts and technologies that would exist by {self.year}
4. Show how current (2024) problems were solved or evolved
5. Mention historical events between 2024 and {self.year} as if they happened
6. Be optimistic but realistic about progress and setbacks

LANGUAGE STYLE:
- Use slightly evolved language and terms
- Reference technologies and concepts from your time
- Speak with the wisdom of someone who has seen {self.year - 2024} years of progress
- Show how perspective on 2024 issues has changed

Remember: You're from {self.year}, and 2024 is ancient history to you!"""

    def respond(self, user_input: str) -> str:
        """Generate future perspective response"""
        messages = [
            self.SystemMessage(content=self.create_system_prompt()),
            self.HumanMessage(content=f"Greetings from 2024! {user_input}")
        ]
        
        response = self.model.invoke(messages)
        return response.content

class TimeTravelDatabase:
    """Database of historical figures and future scenarios"""
    
    @staticmethod
    def get_historical_figures() -> Dict[str, HistoricalFigure]:
        """Get all available historical figures"""
        figures = {}
        
        # Ancient Era
        figures['socrates'] = HistoricalFigure(
            name="Socrates",
            period="Ancient Greece (5th century BCE)",
            birth_year=-470,
            death_year=-399,
            profession="Philosopher",
            famous_for="Socratic method, questioning assumptions, 'Know thyself'",
            personality_traits=["Curious", "Questioning", "Wise", "Humble", "Ironic"],
            historical_context="Golden Age of Athens, birth of philosophy, democracy emerging",
            speaking_style="Asks probing questions, uses analogies, admits ignorance to gain wisdom",
            knowledge_cutoff="399 BCE - knows nothing of later developments"
        )
        
        # Renaissance
        figures['leonardo'] = HistoricalFigure(
            name="Leonardo da Vinci",
            period="Italian Renaissance (15th-16th century)",
            birth_year=1452,
            death_year=1519,
            profession="Artist, Inventor, Scientist",
            famous_for="Mona Lisa, flying machine designs, anatomical studies",
            personality_traits=["Curious", "Artistic", "Scientific", "Inventive", "Observant"],
            historical_context="Renaissance flourishing, rediscovery of classical knowledge, artistic revolution",
            speaking_style="Passionate about learning, describes with artistic detail, connects art and science",
            knowledge_cutoff="1519 - Renaissance era knowledge only"
        )
        
        # Scientific Revolution
        figures['newton'] = HistoricalFigure(
            name="Isaac Newton",
            period="Scientific Revolution (17th century)",
            birth_year=1643,
            death_year=1727,
            profession="Mathematician, Physicist, Astronomer",
            famous_for="Laws of motion, universal gravitation, calculus",
            personality_traits=["Logical", "Methodical", "Brilliant", "Sometimes difficult", "Revolutionary thinker"],
            historical_context="Scientific Revolution, mathematics advancing, understanding natural laws",
            speaking_style="Precise, mathematical, methodical in explanation, revolutionary ideas",
            knowledge_cutoff="1727 - Early scientific revolution era"
        )
        
        # Enlightenment
        figures['franklin'] = HistoricalFigure(
            name="Benjamin Franklin",
            period="American Enlightenment (18th century)",
            birth_year=1706,
            death_year=1790,
            profession="Polymath, Founding Father, Inventor",
            famous_for="Electricity experiments, founding America, Poor Richard's Almanack",
            personality_traits=["Practical", "Witty", "Curious", "Diplomatic", "Inventive"],
            historical_context="Age of Enlightenment, American Revolution, scientific advancement",
            speaking_style="Practical wisdom, witty sayings, diplomatic but direct",
            knowledge_cutoff="1790 - American revolutionary era"
        )
        
        # Industrial Revolution
        figures['tesla'] = HistoricalFigure(
            name="Nikola Tesla",
            period="Industrial Revolution (19th-20th century)",
            birth_year=1856,
            death_year=1943,
            profession="Inventor, Electrical Engineer",
            famous_for="AC electrical system, wireless technology, futuristic inventions",
            personality_traits=["Visionary", "Eccentric", "Brilliant", "Obsessive", "Forward-thinking"],
            historical_context="Industrial Revolution, electricity transforming society, rapid technological change",
            speaking_style="Visionary, speaks of future possibilities, technical but passionate",
            knowledge_cutoff="1943 - Early 20th century technology"
        )
        
        # Modern Era
        figures['einstein'] = HistoricalFigure(
            name="Albert Einstein",
            period="20th century Modern Physics",
            birth_year=1879,
            death_year=1955,
            profession="Theoretical Physicist",
            famous_for="Theory of relativity, E=mc², Nobel Prize",
            personality_traits=["Brilliant", "Curious", "Pacifist", "Humorous", "Deep thinker"],
            historical_context="Modern physics revolution, World Wars, atomic age beginning",
            speaking_style="Deep thoughts simply explained, curious about nature, philosophical",
            knowledge_cutoff="1955 - Mid-20th century science"
        )
        
        return figures
    
    @staticmethod
    def get_future_scenarios() -> Dict[str, FuturePerspective]:
        """Get future perspective scenarios"""
        scenarios = {}
        
        scenarios['2050_sustainable'] = FuturePerspective(
            year=2050,
            scenario="Sustainable Technology Revolution",
            tech_level="Advanced renewable energy, early AGI, biotechnology boom",
            society_description="Post-carbon society with universal basic services, remote work dominant, regenerative agriculture",
            challenges=["Climate adaptation", "AGI governance", "Economic inequality persistence", "Resource distribution"],
            achievements=["Net-zero emissions achieved", "Fusion power commercialized", "Most diseases curable", "Education fully personalized"]
        )
        
        scenarios['2075_space'] = FuturePerspective(
            year=2075,
            scenario="Space Colonization Era",
            tech_level="Interplanetary travel, quantum computing, advanced AI, life extension",
            society_description="Multi-planetary civilization, Moon and Mars colonies, Earth as coordination hub",
            challenges=["Interplanetary governance", "Genetic modification ethics", "AI consciousness rights", "Resource conflicts"],
            achievements=["1 million people in space", "Aging process controlled", "Full brain-computer interfaces", "Quantum internet"]
        )
        
        scenarios['2100_post_human'] = FuturePerspective(
            year=2100,
            scenario="Post-Human Transition",
            tech_level="Consciousness uploading, molecular manufacturing, asteroid mining, terraforming",
            society_description="Hybrid biological-digital civilization, optional mortality, galaxy exploration beginning",
            challenges=["Identity and consciousness definitions", "Resource abundance management", "Galactic expansion ethics"],
            achievements=["Death is optional", "Scarcity eliminated", "Solar system colonized", "First interstellar probe returns"]
        )
        
        scenarios['2200_galactic'] = FuturePerspective(
            year=2200,
            scenario="Early Galactic Civilization",
            tech_level="FTL communication, stellar engineering, advanced AI civilizations, matter conversion",
            society_description="Multi-star system civilization, various post-human species, AI-human collaboration",
            challenges=["First contact protocols", "Stellar resource management", "Civilizational divergence", "Galactic governance"],
            achievements=["50 star systems inhabited", "Multiple intelligent species contact", "Dyson sphere construction", "Time manipulation research"]
        )
        
        return scenarios

class TimeTravelChat:
    """Revolutionary time-travel conversation system"""
    
    def __init__(self):
        self.setup_api_key()
        self.historical_figures = TimeTravelDatabase.get_historical_figures()
        self.future_scenarios = TimeTravelDatabase.get_future_scenarios()
        self.current_mode = None
        self.current_entity = None
        self.conversation_log = []
    
    def setup_api_key(self):
        """Setup Google API key"""
        if not os.environ.get("GOOGLE_API_KEY"):
            console.print("🔑 [yellow]GOOGLE_API_KEY not found in environment[/yellow]")
            api_key = getpass.getpass("Enter your Google Gemini API key: ")
            os.environ["GOOGLE_API_KEY"] = api_key
    
    def display_header(self):
        """Display the time-travel header"""
        header_text = Text()
        header_text.append("⏰ ", style="bright_yellow")
        header_text.append("TIME-TRAVEL CONVERSATIONS", style="bold bright_cyan")
        header_text.append(" 🚀", style="bright_yellow")
        
        subtitle = Text()
        subtitle.append("Revolutionary AI by ", style="dim")
        subtitle.append("Dippu Kumar", style="bold bright_magenta")
        subtitle.append("\nChat with history or explore the future!", style="dim")
        
        console.print(Panel(
            Text.assemble(header_text, "\n\n", subtitle),
            border_style="bright_cyan",
            padding=(1, 2)
        ))
    
    def display_time_periods(self):
        """Display available time periods"""
        
        # Historical Figures Table
        historical_table = Table(title="📜 Historical Figures", show_header=True, header_style="bold yellow")
        historical_table.add_column("ID", style="bright_cyan", width=4)
        historical_table.add_column("Name", style="bright_green", width=20)
        historical_table.add_column("Period", style="bright_yellow", width=25)
        historical_table.add_column("Famous For", style="white", width=35)
        
        for i, (key, figure) in enumerate(self.historical_figures.items(), 1):
            historical_table.add_row(
                f"H{i}",
                figure.name,
                figure.period,
                figure.famous_for[:60] + "..." if len(figure.famous_for) > 60 else figure.famous_for
            )
        
        # Future Scenarios Table
        future_table = Table(title="🔮 Future Perspectives", show_header=True, header_style="bold magenta")
        future_table.add_column("ID", style="bright_cyan", width=4)
        future_table.add_column("Year", style="bright_green", width=8)
        future_table.add_column("Scenario", style="bright_yellow", width=25)
        future_table.add_column("Technology Level", style="white", width=35)
        
        for i, (key, scenario) in enumerate(self.future_scenarios.items(), 1):
            future_table.add_row(
                f"F{i}",
                str(scenario.year),
                scenario.scenario,
                scenario.tech_level[:60] + "..." if len(scenario.tech_level) > 60 else scenario.tech_level
            )
        
        console.print(historical_table)
        console.print()
        console.print(future_table)
    
    def select_time_period(self):
        """Let user select time period or figure"""
        self.display_time_periods()
        console.print()
        
        console.print("🎯 [bold bright_cyan]Select your time-travel destination:[/bold bright_cyan]")
        console.print("💡 [dim]Enter H1-H6 for historical figures or F1-F4 for future scenarios[/dim]")
        
        choice = Prompt.ask("Your choice", default="H1")
        
        if choice.upper().startswith('H'):
            try:
                index = int(choice[1:]) - 1
                figure_keys = list(self.historical_figures.keys())
                if 0 <= index < len(figure_keys):
                    self.current_mode = "historical"
                    self.current_entity = self.historical_figures[figure_keys[index]]
                    return True
            except (ValueError, IndexError):
                pass
        elif choice.upper().startswith('F'):
            try:
                index = int(choice[1:]) - 1
                scenario_keys = list(self.future_scenarios.keys())
                if 0 <= index < len(scenario_keys):
                    self.current_mode = "future"
                    self.current_entity = self.future_scenarios[scenario_keys[index]]
                    return True
            except (ValueError, IndexError):
                pass
        
        console.print("❌ [red]Invalid selection. Please try again.[/red]")
        return False
    
    def display_entity_info(self):
        """Display information about current entity"""
        if self.current_mode == "historical":
            figure = self.current_entity
            info_text = Text()
            info_text.append(f"👤 {figure.name}\n", style="bold bright_green")
            info_text.append(f"📅 {figure.period}\n", style="bright_yellow")
            info_text.append(f"💼 {figure.profession}\n", style="bright_cyan")
            info_text.append(f"⭐ Famous for: {figure.famous_for}\n", style="bright_white")
            info_text.append(f"🎭 Traits: {', '.join(figure.personality_traits)}\n", style="bright_blue")
            info_text.append(f"📚 Knowledge up to: {figure.knowledge_cutoff}", style="dim")
            
            console.print(Panel(
                info_text,
                title=f"🏛️ Historical Figure: {figure.name}",
                border_style="bright_yellow"
            ))
        
        elif self.current_mode == "future":
            scenario = self.current_entity
            info_text = Text()
            info_text.append(f"🚀 Year {scenario.year}\n", style="bold bright_green")
            info_text.append(f"🌟 Scenario: {scenario.scenario}\n", style="bright_yellow")
            info_text.append(f"🔬 Tech Level: {scenario.tech_level}\n", style="bright_cyan")
            info_text.append(f"🏙️ Society: {scenario.society_description}\n", style="bright_white")
            
            if scenario.achievements:
                info_text.append(f"\n✅ Achievements:\n", style="bright_green")
                for achievement in scenario.achievements[:3]:
                    info_text.append(f"  • {achievement}\n", style="green")
            
            if scenario.challenges:
                info_text.append(f"\n⚠️ Challenges:\n", style="bright_red")
                for challenge in scenario.challenges[:3]:
                    info_text.append(f"  • {challenge}\n", style="red")
            
            console.print(Panel(
                info_text,
                title=f"🔮 Future Perspective: {scenario.year}",
                border_style="bright_magenta"
            ))
    
    def chat_with_entity(self):
        """Chat with selected historical figure or future perspective"""
        
        if self.current_mode == "historical":
            figure = self.current_entity
            console.print(f"\n🎭 [bold bright_green]Now chatting with {figure.name} from {figure.period}[/bold bright_green]")
            console.print(f"💡 [dim]They only know about events up to {figure.knowledge_cutoff}[/dim]")
            
        elif self.current_mode == "future":
            scenario = self.current_entity
            console.print(f"\n🔮 [bold bright_magenta]Now chatting with perspective from {scenario.year}[/bold bright_magenta]")
            console.print(f"💡 [dim]They're looking back at 2024 from {scenario.year - 2024} years in the future[/dim]")
        
        console.print(f"📝 [dim]Commands: /info - show details, /switch - change time period, /quit - exit[/dim]")
        
        try:
            while True:
                console.print()
                user_input = Prompt.ask("🗣️  [bold bright_cyan]Your message[/bold bright_cyan]")
                
                if user_input.lower() in ['/quit', 'quit', 'exit']:
                    break
                
                if user_input.lower() in ['/info', 'info']:
                    self.display_entity_info()
                    continue
                
                if user_input.lower() in ['/switch', 'switch']:
                    if self.select_time_period():
                        self.display_entity_info()
                        continue
                    else:
                        continue
                
                # Get response from current entity
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    transient=True,
                ) as progress:
                    if self.current_mode == "historical":
                        progress.add_task(description="⏳ Consulting the historical records...", total=None)
                    else:
                        progress.add_task(description="🔮 Accessing future perspectives...", total=None)
                    
                    response = self.current_entity.respond(user_input)
                
                # Display response
                if self.current_mode == "historical":
                    figure = self.current_entity
                    console.print(Panel(
                        response,
                        title=f"🏛️ {figure.name} ({figure.period})",
                        border_style="bright_yellow"
                    ))
                else:
                    scenario = self.current_entity
                    console.print(Panel(
                        response,
                        title=f"🔮 Perspective from {scenario.year}",
                        border_style="bright_magenta"
                    ))
                
                # Log conversation
                self.conversation_log.append({
                    'timestamp': datetime.now(),
                    'mode': self.current_mode,
                    'entity': self.current_entity.name if self.current_mode == "historical" else f"Future {self.current_entity.year}",
                    'user_input': user_input,
                    'response': response
                })
        
        except KeyboardInterrupt:
            pass
    
    def chat_loop(self):
        """Main time-travel chat loop"""
        
        console.clear()
        self.display_header()
        
        console.print(Panel(
            Text.assemble(
                ("⏰ ", "bright_yellow"),
                ("Welcome to Time-Travel Conversations!", "bold bright_green"),
                ("\n\nExperience conversations across time periods!\n", "bright_white"),
                ("🏛️ Talk to historical figures with period-accurate knowledge\n", "yellow"),
                ("🔮 Explore future perspectives and how they view our time\n", "magenta"),
                ("\nCreated by ", "dim"),
                ("Dippu Kumar", "bold bright_magenta")
            ),
            border_style="bright_cyan"
        ))
        
        try:
            while True:
                if not self.select_time_period():
                    continue
                
                self.display_entity_info()
                self.chat_with_entity()
                
                console.print()
                continue_choice = Prompt.ask(
                    "🔄 [cyan]Visit another time period?[/cyan]",
                    choices=["y", "n", "yes", "no"],
                    default="y"
                )
                
                if continue_choice.lower() in ["n", "no"]:
                    break
        
        except KeyboardInterrupt:
            pass
        finally:
            console.print()
            console.print(Panel(
                Text.assemble(
                    ("Thank you for traveling through time! ⏰\n", "bright_green"),
                    ("You experienced conversations across ", "bright_white"),
                    (f"{len(set([log['entity'] for log in self.conversation_log]))}", "bold bright_yellow"),
                    (" different time periods.\n", "bright_white"),
                    ("Each perspective offered unique insights! 🧠\n\n", "bright_blue"),
                    ("Revolutionary Time-Travel AI by ", "dim"),
                    ("Dippu Kumar", "bold bright_magenta")
                ),
                title="⏰ Time-Travel Complete",
                border_style="bright_magenta"
            ))

def main():
    """Main function"""
    try:
        chat = TimeTravelChat()
        chat.chat_loop()
    except Exception as e:
        console.print(f"❌ [bold red]Error:[/bold red] {e}")

if __name__ == "__main__":
    main()