#!/usr/bin/env python3
"""
🎭 Mood-Adaptive UI - Revolutionary Emotional Interface
Author: Dippu Kumar

UI that changes colors, themes, and interaction style based on your emotional state!
The first truly empathetic user interface.
"""

import os
import getpass
from datetime import datetime
from typing import Dict, List, Optional
import re
import random

from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.theme import Theme
from rich.style import Style

# Load environment variables
load_dotenv()


class MoodThemes:
    """Different UI themes for different moods"""

    @staticmethod
    def get_themes():
        return {
            "joy": {
                "colors": {
                    "primary": "bright_yellow",
                    "secondary": "bright_green",
                    "accent": "bright_magenta",
                    "text": "bright_white",
                    "border": "bright_cyan",
                },
                "emoji": "😊",
                "style_desc": "Bright, energetic, celebratory",
                "animations": ["✨", "🌟", "💫", "🎉"],
                "greeting": "What a wonderful day to chat!",
            },
            "sadness": {
                "colors": {
                    "primary": "blue",
                    "secondary": "cyan",
                    "accent": "white",
                    "text": "bright_white",
                    "border": "blue",
                },
                "emoji": "🤗",
                "style_desc": "Calm, supportive, gentle",
                "animations": ["💙", "🌙", "☁️", "🕊️"],
                "greeting": "I'm here to listen and support you.",
            },
            "anger": {
                "colors": {
                    "primary": "red",
                    "secondary": "bright_red",
                    "accent": "yellow",
                    "text": "bright_white",
                    "border": "red",
                },
                "emoji": "🔥",
                "style_desc": "Strong, bold, understanding",
                "animations": ["🔥", "⚡", "💪", "🌋"],
                "greeting": "Let's work through this together.",
            },
            "anxiety": {
                "colors": {
                    "primary": "magenta",
                    "secondary": "bright_blue",
                    "accent": "cyan",
                    "text": "bright_white",
                    "border": "magenta",
                },
                "emoji": "🌸",
                "style_desc": "Calming, peaceful, reassuring",
                "animations": ["🌸", "🦋", "🌿", "💆"],
                "greeting": "Take a deep breath. Everything will be okay.",
            },
            "excitement": {
                "colors": {
                    "primary": "bright_magenta",
                    "secondary": "bright_yellow",
                    "accent": "bright_green",
                    "text": "bright_white",
                    "border": "bright_magenta",
                },
                "emoji": "🚀",
                "style_desc": "Dynamic, energetic, vibrant",
                "animations": ["🚀", "⚡", "🎆", "🌈"],
                "greeting": "I can feel your energy! Let's explore!",
            },
            "curiosity": {
                "colors": {
                    "primary": "bright_green",
                    "secondary": "bright_cyan",
                    "accent": "bright_yellow",
                    "text": "bright_white",
                    "border": "bright_green",
                },
                "emoji": "🔍",
                "style_desc": "Inquisitive, bright, exploratory",
                "animations": ["🔍", "💡", "🧩", "🗝️"],
                "greeting": "What fascinating questions shall we explore?",
            },
            "peaceful": {
                "colors": {
                    "primary": "green",
                    "secondary": "cyan",
                    "accent": "white",
                    "text": "bright_white",
                    "border": "green",
                },
                "emoji": "🧘",
                "style_desc": "Serene, balanced, harmonious",
                "animations": ["🧘", "🌊", "🍃", "☮️"],
                "greeting": "Welcome to this peaceful moment together.",
            },
            "neutral": {
                "colors": {
                    "primary": "white",
                    "secondary": "bright_white",
                    "accent": "cyan",
                    "text": "bright_white",
                    "border": "white",
                },
                "emoji": "🤖",
                "style_desc": "Clean, professional, balanced",
                "animations": ["🤖", "💭", "📝", "⚖️"],
                "greeting": "Hello! How can I help you today?",
            },
        }


class EmotionDetector:
    """Detect emotions from text input"""

    def __init__(self):
        self.emotion_patterns = {
            "joy": [
                r"happy|joy|excited|amazing|wonderful|great|fantastic|love|awesome|brilliant|thrilled|delighted",
                r"😊|😄|😃|🎉|❤️|💕|😍|🥰|😘|🤗|🎊|🥳",
            ],
            "sadness": [
                r"sad|depressed|down|upset|disappointed|terrible|awful|crying|hurt|lonely|miserable",
                r"😢|😭|💔|😞|😔|☹️|😿|😰|😩|😫",
            ],
            "anger": [
                r"angry|furious|mad|annoyed|frustrated|irritated|hate|rage|pissed|outraged|livid",
                r"😡|🤬|😠|💢|🔥|👿|😤|🗯️",
            ],
            "anxiety": [
                r"worried|anxious|nervous|scared|afraid|stressed|overwhelmed|panic|concerned|tense",
                r"😰|😟|😨|😧|😵|🙀|😬|😓",
            ],
            "excitement": [
                r"excited|thrilled|pumped|energized|hyped|amazing|incredible|fantastic|wow",
                r"🤩|😍|🤯|🎉|🚀|⚡|🔥|💥|🎆",
            ],
            "curiosity": [
                r"curious|wonder|interesting|how|why|what|tell me|explain|learn|explore|discover",
                r"🤔|🧐|❓|❔|💭|🔍|💡",
            ],
            "peaceful": [
                r"calm|peaceful|relaxed|serene|content|zen|tranquil|balanced|centered",
                r"🧘|😌|☮️|🌸|🌿|🕊️|🌊",
            ],
        }

    def detect_emotion(self, text: str) -> Dict[str, float]:
        """Detect emotions with confidence scores"""
        text_lower = text.lower()
        emotions = {}

        for emotion, patterns in self.emotion_patterns.items():
            score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, text_lower))
                score += matches

            # Normalize score based on text length
            emotions[emotion] = min(score / max(len(text.split()) / 5, 1), 1.0)

        return emotions

    def get_primary_emotion(self, emotions: Dict[str, float]) -> str:
        """Get the strongest emotion or neutral if none detected"""
        if not emotions or max(emotions.values()) < 0.1:
            return "neutral"
        return max(emotions.items(), key=lambda x: x[1])[0]


class AdaptiveUI:
    """Mood-adaptive user interface"""

    def __init__(self):
        self.setup_api_key()
        self.emotion_detector = EmotionDetector()
        self.themes = MoodThemes.get_themes()
        self.current_theme = "neutral"
        self.mood_history = []
        self.adaptation_count = 0

        # Setup model
        self.setup_model()

    def setup_api_key(self):
        """Setup Google API key"""
        if not os.environ.get("GOOGLE_API_KEY"):
            console = Console()
            console.print("🔑 [yellow]GOOGLE_API_KEY not found in environment[/yellow]")
            api_key = getpass.getpass("Enter your Google Gemini API key: ")
            os.environ["GOOGLE_API_KEY"] = api_key

    def setup_model(self):
        """Setup AI model"""
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            from langchain.schema import HumanMessage, SystemMessage

            self.model = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash", temperature=0.7
            )
            self.HumanMessage = HumanMessage
            self.SystemMessage = SystemMessage
        except ImportError:
            console = Console()
            console.print("❌ [red]Error: langchain-google-genai not installed[/red]")
            exit(1)

    def adapt_to_mood(self, emotions: Dict[str, float]) -> str:
        """Adapt UI theme based on detected emotions"""
        primary_emotion = self.emotion_detector.get_primary_emotion(emotions)

        if primary_emotion != self.current_theme:
            self.current_theme = primary_emotion
            self.adaptation_count += 1
            return f"🎭 UI adapted to {primary_emotion} mood"

        return ""

    def get_console_with_theme(self) -> Console:
        """Get console with current mood theme"""
        theme_colors = self.themes[self.current_theme]["colors"]

        # Create custom theme
        theme = Theme(
            {
                "primary": theme_colors["primary"],
                "secondary": theme_colors["secondary"],
                "accent": theme_colors["accent"],
                "text": theme_colors["text"],
                "border": theme_colors["border"],
            }
        )

        return Console(theme=theme)

    def create_mood_system_prompt(self) -> str:
        """Create system prompt that matches current mood"""
        theme = self.themes[self.current_theme]

        return f"""You are a Mood-Adaptive AI created by Dippu Kumar that responds empathetically to the user's emotional state.

CURRENT USER MOOD: {self.current_theme}
UI THEME: {theme['style_desc']}
MOOD EMOJI: {theme['emoji']}

EMOTIONAL RESPONSE GUIDELINES FOR {self.current_theme.upper()}:

{self._get_mood_specific_guidelines()}

GENERAL RULES:
1. Match the emotional tone of your response to the user's mood
2. Use language that feels appropriate for their emotional state
3. Be genuinely empathetic and supportive
4. Adjust your communication style to what they need right now
5. Remember that the UI has also adapted to their mood

RESPONSE STYLE:
- Tone: Match the {theme['style_desc']} theme
- Approach: Emotionally appropriate for {self.current_theme}
- Goal: Provide exactly what they need in this emotional moment

Remember: You're not just answering questions - you're providing emotional support through adaptive interaction!"""

    def _get_mood_specific_guidelines(self) -> str:
        """Get mood-specific response guidelines"""
        guidelines = {
            "joy": "Be celebratory and energetic! Share in their happiness. Use exclamation points and positive language. Encourage their good mood and build on their excitement.",
            "sadness": "Be gentle, compassionate, and supportive. Use softer language. Offer comfort and understanding. Don't try to immediately cheer them up - acknowledge their feelings first.",
            "anger": "Be understanding but not inflammatory. Help them process their feelings constructively. Stay calm and supportive. Offer perspective when appropriate.",
            "anxiety": "Be calming and reassuring. Use simple, clear language. Offer practical support. Help them feel grounded and safe. Avoid overwhelming information.",
            "excitement": "Match their energy! Be enthusiastic and dynamic. Help them explore their excitement. Use energetic language and build on their momentum.",
            "curiosity": "Be engaging and informative! Feed their curiosity with interesting details. Ask follow-up questions. Encourage their desire to learn and explore.",
            "peaceful": "Maintain a calm, balanced tone. Be thoughtful and measured in your responses. Respect the tranquil mood and don't disrupt it unnecessarily.",
            "neutral": "Be professional but warm. Maintain a balanced approach. Adapt to cues from their input about what they might need.",
        }
        return guidelines.get(self.current_theme, guidelines["neutral"])

    def display_adaptive_header(self, console: Console):
        """Display header adapted to current mood"""
        theme = self.themes[self.current_theme]

        header_text = Text()
        header_text.append(f"{theme['emoji']} ", style="primary")
        header_text.append("MOOD-ADAPTIVE AI", style="bold primary")
        header_text.append(f" {random.choice(theme['animations'])}", style="accent")

        subtitle = Text()
        subtitle.append("Revolutionary Emotional UI by ", style="dim")
        subtitle.append("Dippu Kumar", style="bold accent")
        subtitle.append(f"\n{theme['greeting']}", style="secondary")

        console.print(
            Panel(
                Text.assemble(header_text, "\n\n", subtitle),
                border_style="border",
                padding=(1, 2),
            )
        )

    def display_mood_status(self, console: Console, emotions: Dict[str, float]):
        """Display current mood and UI adaptation status"""
        theme = self.themes[self.current_theme]

        # Mood detection results
        mood_table = Table(
            title=f"{theme['emoji']} Emotional State Analysis", show_header=True
        )
        mood_table.add_column("Emotion", style="accent")
        mood_table.add_column("Level", style="secondary")
        mood_table.add_column("Indicator", style="primary")

        for emotion, level in sorted(
            emotions.items(), key=lambda x: x[1], reverse=True
        ):
            if level > 0:
                indicator = "█" * int(level * 10) if level > 0 else "░"
                mood_table.add_row(emotion.title(), f"{level:.2f}", indicator)

        # Theme info
        theme_info = Text()
        theme_info.append(
            f"🎭 Current Theme: {self.current_theme.title()}\n", style="primary"
        )
        theme_info.append(f"🎨 Style: {theme['style_desc']}\n", style="secondary")
        theme_info.append(f"🔄 Adaptations: {self.adaptation_count}\n", style="accent")
        theme_info.append(
            f"📊 Mood History: {len(self.mood_history)} entries", style="text"
        )

        console.print(mood_table)
        console.print()
        console.print(
            Panel(theme_info, title="🎭 UI Adaptation Status", border_style="border")
        )

    def get_mood_response(self, user_input: str, emotions: Dict[str, float]) -> str:
        """Get AI response adapted to current mood"""

        # Create mood-adapted system prompt
        system_prompt = self.create_mood_system_prompt()

        messages = [
            self.SystemMessage(content=system_prompt),
            self.HumanMessage(content=user_input),
        ]

        response = self.model.invoke(messages)
        return response.content

    def main_loop(self):
        """Main mood-adaptive chat loop"""

        # Start with neutral console
        console = Console()
        console.clear()

        # Initial header
        console.print(
            Panel(
                Text.assemble(
                    ("🎭 ", "bright_yellow"),
                    ("MOOD-ADAPTIVE UI", "bold bright_cyan"),
                    (" 🌈", "bright_magenta"),
                    ("\n\nRevolutionary Emotional Interface by ", "dim"),
                    ("Dippu Kumar", "bold bright_magenta"),
                    ("\n\nThe UI that adapts to YOUR emotions!", "bright_white"),
                    (
                        "\n\n💡 Start chatting and watch the interface transform based on your mood!",
                        "dim",
                    ),
                ),
                border_style="bright_cyan",
                padding=(1, 2),
            )
        )

        session_stats = {
            "interactions": 0,
            "mood_changes": 0,
            "start_time": datetime.now(),
        }

        try:
            while True:
                # Get themed console
                console = self.get_console_with_theme()

                console.print()
                user_input = Prompt.ask(
                    "💭 [text]Share your thoughts[/text]", console=console
                )

                if user_input.lower() in ["quit", "exit", "/quit"]:
                    break

                if user_input.lower() in ["/mood", "mood", "/status"]:
                    emotions = self.emotion_detector.detect_emotion(user_input)
                    self.display_mood_status(console, emotions)
                    continue

                # Detect emotions and adapt
                emotions = self.emotion_detector.detect_emotion(user_input)
                previous_theme = self.current_theme
                adaptation_msg = self.adapt_to_mood(emotions)

                # Track mood change
                if previous_theme != self.current_theme:
                    session_stats["mood_changes"] += 1
                    console = self.get_console_with_theme()  # Get new themed console
                    self.display_adaptive_header(console)
                    if adaptation_msg:
                        console.print(f"[accent]{adaptation_msg}[/accent]")

                # Generate mood-adapted response
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    transient=True,
                    console=console,
                ) as progress:
                    theme = self.themes[self.current_theme]
                    progress.add_task(
                        description=f"{theme['emoji']} Crafting response for your {self.current_theme} mood...",
                        total=None,
                    )
                    response = self.get_mood_response(user_input, emotions)

                # Display response with current theme
                theme = self.themes[self.current_theme]
                console.print(
                    Panel(
                        response,
                        title=f"{theme['emoji']} Response (Mood: {self.current_theme.title()})",
                        border_style="border",
                    )
                )

                # Store mood history
                self.mood_history.append(
                    {
                        "timestamp": datetime.now(),
                        "input": user_input,
                        "emotions": emotions,
                        "primary_emotion": self.current_theme,
                        "response": response,
                    }
                )

                session_stats["interactions"] += 1

                # Show periodic mood insights
                if session_stats["interactions"] % 5 == 0:
                    console.print()
                    console.print(
                        f"[accent]✨ UI has adapted {session_stats['mood_changes']} times to match your emotions![/accent]"
                    )

        except KeyboardInterrupt:
            pass
        finally:
            # Final summary with themed console
            console = self.get_console_with_theme()
            duration = datetime.now() - session_stats["start_time"]

            console.print()
            console.print(
                Panel(
                    Text.assemble(
                        (
                            f"Thank you for experiencing adaptive emotions! {self.themes[self.current_theme]['emoji']}\n",
                            "primary",
                        ),
                        ("Session Summary:\n", "accent"),
                        (f"🕒 Duration: {str(duration).split('.')[0]}\n", "secondary"),
                        (
                            f"💬 Interactions: {session_stats['interactions']}\n",
                            "secondary",
                        ),
                        (
                            f"🎭 Mood Changes: {session_stats['mood_changes']}\n",
                            "secondary",
                        ),
                        (f"🎨 Final Mood: {self.current_theme.title()}\n", "secondary"),
                        (
                            f"🔄 Total Adaptations: {self.adaptation_count}\n\n",
                            "secondary",
                        ),
                        ("Revolutionary Mood-Adaptive UI by ", "dim"),
                        ("Dippu Kumar", "accent"),
                    ),
                    title="🎭 Adaptive Session Complete",
                    border_style="border",
                )
            )


def main():
    """Main function"""
    try:
        ui = AdaptiveUI()
        ui.main_loop()
    except Exception as e:
        console = Console()
        console.print(f"❌ [bold red]Error:[/bold red] {e}")


if __name__ == "__main__":
    main()
