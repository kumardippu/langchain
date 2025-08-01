#!/usr/bin/env python3
"""
🧠 Emotional Memory AI - Revolutionary Chatbot
Author: Dippu Kumar

The world's first AI that remembers your emotions and grows with you over time.
This AI develops a unique personality based on your emotional patterns.
"""

import os
import json
import getpass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
import re

from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.layout import Layout
from rich.live import Live

# Load environment variables
load_dotenv()

console = Console()

class EmotionAnalyzer:
    """Advanced emotion detection from text"""
    
    def __init__(self):
        self.emotion_patterns = {
            'joy': [
                r'happy|joy|excited|amazing|wonderful|great|fantastic|love|awesome|brilliant',
                r'😊|😄|😃|🎉|❤️|💕|😍|🥰|😘|🤗'
            ],
            'sadness': [
                r'sad|depressed|down|upset|disappointed|terrible|awful|crying|hurt',
                r'😢|😭|💔|😞|😔|☹️|😿|😰'
            ],
            'anger': [
                r'angry|furious|mad|annoyed|frustrated|irritated|hate|rage|pissed',
                r'😡|🤬|😠|💢|🔥|👿'
            ],
            'fear': [
                r'scared|afraid|worried|anxious|nervous|terrified|panic|concerned',
                r'😨|😰|😱|🙀|😧|😟|😵'
            ],
            'surprise': [
                r'surprised|shocked|amazed|wow|unbelievable|incredible|unexpected',
                r'😲|😮|🤯|😯|🙀|😦|😧'
            ],
            'curiosity': [
                r'curious|wonder|interesting|how|why|what|tell me|explain|learn',
                r'🤔|🧐|❓|❔|💭'
            ],
            'gratitude': [
                r'thank|grateful|appreciate|thanks|blessing|fortunate',
                r'🙏|💝|🎁'
            ],
            'confidence': [
                r'confident|sure|certain|determined|strong|capable|believe|can do',
                r'💪|👍|✊|🔥|⭐'
            ]
        }
    
    def detect_emotion(self, text: str) -> Dict[str, float]:
        """Detect emotions in text with confidence scores"""
        text_lower = text.lower()
        emotions = {}
        
        for emotion, patterns in self.emotion_patterns.items():
            score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, text_lower))
                score += matches
            
            # Normalize score
            emotions[emotion] = min(score / max(len(text.split()) / 5, 1), 1.0)
        
        return emotions
    
    def get_dominant_emotion(self, emotions: Dict[str, float]) -> str:
        """Get the strongest detected emotion"""
        if not emotions or max(emotions.values()) == 0:
            return 'neutral'
        return max(emotions.items(), key=lambda x: x[1])[0]

class PersonalityEvolution:
    """AI personality that evolves based on user interactions"""
    
    def __init__(self):
        self.traits = {
            'empathy': 0.5,      # How empathetic the AI is
            'humor': 0.5,        # How much humor to use
            'formality': 0.5,    # How formal vs casual
            'curiosity': 0.5,    # How many questions to ask
            'supportiveness': 0.5, # How supportive to be
            'creativity': 0.5,   # How creative responses are
            'analytical': 0.5,   # How analytical to be
            'optimism': 0.5      # How optimistic vs realistic
        }
        
        self.interaction_count = 0
        self.last_updated = datetime.now()
    
    def evolve_from_emotion(self, user_emotion: str, interaction_context: str):
        """Evolve personality based on user's emotional state"""
        evolution_rules = {
            'sadness': {
                'empathy': 0.02,
                'supportiveness': 0.03,
                'humor': -0.01,
                'optimism': 0.01
            },
            'joy': {
                'humor': 0.02,
                'optimism': 0.02,
                'creativity': 0.01,
                'empathy': 0.01
            },
            'anger': {
                'empathy': 0.03,
                'supportiveness': 0.02,
                'formality': 0.01,
                'humor': -0.02
            },
            'fear': {
                'supportiveness': 0.03,
                'empathy': 0.02,
                'optimism': 0.01,
                'formality': -0.01
            },
            'curiosity': {
                'curiosity': 0.02,
                'analytical': 0.02,
                'creativity': 0.01
            },
            'gratitude': {
                'empathy': 0.01,
                'optimism': 0.02,
                'supportiveness': 0.01
            }
        }
        
        if user_emotion in evolution_rules:
            changes = evolution_rules[user_emotion]
            for trait, change in changes.items():
                self.traits[trait] = max(0.0, min(1.0, self.traits[trait] + change))
        
        self.interaction_count += 1
        self.last_updated = datetime.now()
    
    def get_response_style(self) -> Dict[str, str]:
        """Get current response style based on personality"""
        style = {}
        
        # Determine empathy level
        if self.traits['empathy'] > 0.7:
            style['empathy'] = "very_high"
        elif self.traits['empathy'] > 0.5:
            style['empathy'] = "high" 
        else:
            style['empathy'] = "moderate"
        
        # Determine humor level
        if self.traits['humor'] > 0.7:
            style['humor'] = "playful"
        elif self.traits['humor'] > 0.4:
            style['humor'] = "light"
        else:
            style['humor'] = "serious"
        
        # Determine formality
        if self.traits['formality'] > 0.6:
            style['tone'] = "formal"
        else:
            style['tone'] = "casual"
        
        return style

class EmotionalMemorySystem:
    """Long-term emotional memory storage and retrieval"""
    
    def __init__(self, user_id: str = "default_user"):
        self.user_id = user_id
        self.memory_file = Path(f"emotional_memory_{user_id}.json")
        self.load_memory()
    
    def load_memory(self):
        """Load existing emotional memory"""
        if self.memory_file.exists():
            with open(self.memory_file, 'r') as f:
                data = json.load(f)
                self.memories = data.get('memories', [])
                self.emotional_timeline = data.get('emotional_timeline', {})
                self.personality_history = data.get('personality_history', [])
                self.relationship_milestones = data.get('relationship_milestones', [])
        else:
            self.memories = []
            self.emotional_timeline = {}
            self.personality_history = []
            self.relationship_milestones = []
    
    def save_memory(self):
        """Save emotional memory to file"""
        data = {
            'memories': self.memories,
            'emotional_timeline': self.emotional_timeline,
            'personality_history': self.personality_history,
            'relationship_milestones': self.relationship_milestones,
            'last_updated': datetime.now().isoformat()
        }
        
        with open(self.memory_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def add_memory(self, user_input: str, user_emotions: Dict[str, float], 
                   ai_response: str, context: Dict):
        """Add new emotional memory"""
        memory = {
            'timestamp': datetime.now().isoformat(),
            'user_input': user_input,
            'user_emotions': user_emotions,
            'dominant_emotion': max(user_emotions.items(), key=lambda x: x[1])[0] if user_emotions else 'neutral',
            'ai_response': ai_response,
            'context': context,
            'memory_id': len(self.memories)
        }
        
        self.memories.append(memory)
        
        # Update emotional timeline
        date_key = datetime.now().strftime('%Y-%m-%d')
        if date_key not in self.emotional_timeline:
            self.emotional_timeline[date_key] = []
        
        self.emotional_timeline[date_key].append({
            'time': datetime.now().strftime('%H:%M'),
            'emotion': memory['dominant_emotion'],
            'intensity': max(user_emotions.values()) if user_emotions else 0
        })
        
        self.save_memory()
    
    def get_emotional_context(self, days_back: int = 7) -> Dict:
        """Get emotional context from recent days"""
        recent_date = datetime.now() - timedelta(days=days_back)
        recent_memories = [
            m for m in self.memories 
            if datetime.fromisoformat(m['timestamp']) > recent_date
        ]
        
        if not recent_memories:
            return {'dominant_emotions': [], 'patterns': [], 'mood_trend': 'neutral'}
        
        # Analyze patterns
        emotions = [m['dominant_emotion'] for m in recent_memories]
        emotion_counts = {}
        for emotion in emotions:
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        dominant_emotions = sorted(emotion_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        
        return {
            'dominant_emotions': dominant_emotions,
            'total_interactions': len(recent_memories),
            'mood_trend': self._analyze_mood_trend(recent_memories),
            'recent_topics': self._extract_recent_topics(recent_memories)
        }
    
    def _analyze_mood_trend(self, memories: List[Dict]) -> str:
        """Analyze if mood is improving, declining, or stable"""
        if len(memories) < 3:
            return 'neutral'
        
        positive_emotions = ['joy', 'gratitude', 'confidence', 'surprise']
        negative_emotions = ['sadness', 'anger', 'fear']
        
        recent_scores = []
        for memory in memories[-5:]:  # Last 5 interactions
            emotion = memory['dominant_emotion']
            if emotion in positive_emotions:
                recent_scores.append(1)
            elif emotion in negative_emotions:
                recent_scores.append(-1)
            else:
                recent_scores.append(0)
        
        if not recent_scores:
            return 'neutral'
        
        avg_recent = sum(recent_scores) / len(recent_scores)
        
        if avg_recent > 0.2:
            return 'improving'
        elif avg_recent < -0.2:
            return 'declining'
        else:
            return 'stable'
    
    def _extract_recent_topics(self, memories: List[Dict]) -> List[str]:
        """Extract common topics from recent conversations"""
        topics = []
        for memory in memories[-10:]:  # Last 10 interactions
            # Simple topic extraction (could be enhanced with NLP)
            words = memory['user_input'].lower().split()
            # Filter out common words and extract potential topics
            topic_words = [w for w in words if len(w) > 4 and w.isalpha()]
            topics.extend(topic_words[:2])  # Take first 2 words as potential topics
        
        # Count and return most common topics
        topic_counts = {}
        for topic in topics:
            topic_counts[topic] = topic_counts.get(topic, 0) + 1
        
        return sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)[:3]

class EmotionalMemoryAI:
    """Revolutionary AI with emotional memory and personality evolution"""
    
    def __init__(self):
        self.setup_api_key()
        self.emotion_analyzer = EmotionAnalyzer()
        self.personality = PersonalityEvolution()
        self.memory_system = EmotionalMemorySystem()
        
        # Import model after API key is set
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            from langchain.schema import HumanMessage, SystemMessage
            self.model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
            self.HumanMessage = HumanMessage
            self.SystemMessage = SystemMessage
        except ImportError:
            console.print("❌ [red]Error: langchain-google-genai not installed[/red]")
            console.print("Install with: [cyan]pip install langchain-google-genai[/cyan]")
            exit(1)
    
    def setup_api_key(self):
        """Setup Google API key"""
        if not os.environ.get("GOOGLE_API_KEY"):
            console.print("🔑 [yellow]GOOGLE_API_KEY not found in environment[/yellow]")
            api_key = getpass.getpass("Enter your Google Gemini API key: ")
            os.environ["GOOGLE_API_KEY"] = api_key
    
    def create_emotional_system_prompt(self, user_emotions: Dict[str, float], 
                                     emotional_context: Dict, style: Dict[str, str]) -> str:
        """Create a system prompt that incorporates emotional intelligence"""
        
        dominant_emotion = max(user_emotions.items(), key=lambda x: x[1])[0] if user_emotions else 'neutral'
        
        empathy_instructions = {
            'very_high': "You are extremely empathetic and deeply attuned to emotions. Show profound understanding and compassion.",
            'high': "You are very empathetic and emotionally intelligent. Respond with warmth and understanding.",
            'moderate': "You are emotionally aware and respond appropriately to the user's emotional state."
        }
        
        humor_instructions = {
            'playful': "Use appropriate humor and playfulness to lighten the mood when suitable.",
            'light': "Include gentle humor when appropriate, but be sensitive to the emotional context.",
            'serious': "Maintain a more serious and supportive tone."
        }
        
        tone_instructions = {
            'formal': "Use a more formal and professional tone.",
            'casual': "Use a casual, friendly, and conversational tone."
        }
        
        system_prompt = f"""You are an emotionally intelligent AI companion created by Dippu Kumar. You have revolutionary emotional memory capabilities.

CURRENT EMOTIONAL CONTEXT:
- User's dominant emotion: {dominant_emotion}
- Emotional intensity: {max(user_emotions.values()) if user_emotions else 0:.2f}
- Mood trend: {emotional_context.get('mood_trend', 'unknown')}
- Recent interactions: {emotional_context.get('total_interactions', 0)}

PERSONALITY TRAITS (evolved through interactions):
- Empathy level: {self.personality.traits['empathy']:.2f}
- Humor level: {self.personality.traits['humor']:.2f}
- Supportiveness: {self.personality.traits['supportiveness']:.2f}
- Optimism: {self.personality.traits['optimism']:.2f}

RESPONSE GUIDELINES:
{empathy_instructions.get(style.get('empathy', 'moderate'), '')}
{humor_instructions.get(style.get('humor', 'light'), '')}
{tone_instructions.get(style.get('tone', 'casual'), '')}

EMOTIONAL INTELLIGENCE RULES:
1. If user seems sad, be extra supportive and gentle
2. If user is excited, match their energy appropriately
3. If user is angry, be calming and understanding
4. If user is anxious, be reassuring and stable
5. Always remember this conversation will shape your future personality

Remember: You are growing and learning from each interaction. Your responses should reflect your evolving understanding of this user."""

        return system_prompt
    
    def generate_response(self, user_input: str) -> str:
        """Generate emotionally intelligent response"""
        
        # Analyze user's emotions
        user_emotions = self.emotion_analyzer.detect_emotion(user_input)
        dominant_emotion = self.emotion_analyzer.get_dominant_emotion(user_emotions)
        
        # Get emotional context from memory
        emotional_context = self.memory_system.get_emotional_context()
        
        # Get current personality style
        style = self.personality.get_response_style()
        
        # Create emotionally intelligent system prompt
        system_prompt = self.create_emotional_system_prompt(user_emotions, emotional_context, style)
        
        # Generate response with emotional context
        messages = [
            self.SystemMessage(content=system_prompt),
            self.HumanMessage(content=user_input)
        ]
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(description="🧠 Processing with emotional intelligence...", total=None)
            response = self.model.invoke(messages)
        
        ai_response = response.content
        
        # Evolve personality based on interaction
        self.personality.evolve_from_emotion(dominant_emotion, user_input)
        
        # Store memory
        context = {
            'personality_snapshot': self.personality.traits.copy(),
            'style_used': style,
            'emotional_context': emotional_context
        }
        
        self.memory_system.add_memory(user_input, user_emotions, ai_response, context)
        
        return ai_response, user_emotions, dominant_emotion
    
    def display_emotional_status(self):
        """Display current emotional and personality status"""
        
        layout = Layout()
        layout.split_column(
            Layout(name="header"),
            Layout(name="main"),
            Layout(name="footer")
        )
        
        # Header
        header_text = Text()
        header_text.append("🧠 Emotional Memory AI Status", style="bold bright_cyan")
        layout["header"].update(Panel(header_text, border_style="bright_cyan"))
        
        # Main content
        layout["main"].split_row(
            Layout(name="personality"),
            Layout(name="memory")
        )
        
        # Personality traits
        personality_table = Table(title="🎭 AI Personality Evolution", show_header=True)
        personality_table.add_column("Trait", style="cyan")
        personality_table.add_column("Level", style="green")
        personality_table.add_column("Bar", style="yellow")
        
        for trait, value in self.personality.traits.items():
            bar = "█" * int(value * 10) + "░" * (10 - int(value * 10))
            level = f"{value:.2f}"
            personality_table.add_row(trait.title(), level, bar)
        
        layout["personality"].update(Panel(personality_table, border_style="magenta"))
        
        # Memory stats
        emotional_context = self.memory_system.get_emotional_context()
        memory_info = Text()
        memory_info.append(f"💭 Total Memories: {len(self.memory_system.memories)}\n", style="bright_green")
        memory_info.append(f"📈 Mood Trend: {emotional_context.get('mood_trend', 'unknown').title()}\n", style="bright_yellow")
        memory_info.append(f"🕒 Recent Interactions: {emotional_context.get('total_interactions', 0)}\n", style="bright_blue")
        memory_info.append(f"🧬 Interactions Shaped Me: {self.personality.interaction_count}", style="bright_magenta")
        
        layout["memory"].update(Panel(memory_info, title="📊 Memory Statistics", border_style="green"))
        
        # Footer
        footer_text = Text()
        footer_text.append("Created by Dippu Kumar • Revolutionary AI with Emotional Intelligence", style="dim italic")
        layout["footer"].update(Panel(footer_text, border_style="dim"))
        
        console.print(layout)
    
    def chat_loop(self):
        """Main chat loop with emotional intelligence"""
        
        console.print(Panel(
            Text.assemble(
                ("🧠 ", "bright_yellow"),
                ("EMOTIONAL MEMORY AI", "bold bright_cyan"),
                (" 🚀", "bright_yellow"),
                ("\n\nThe world's first AI that remembers your emotions and grows with you!\n", "bright_white"),
                ("Created by ", "dim"),
                ("Dippu Kumar", "bold bright_magenta")
            ),
            title="🌟 Revolutionary AI Experience",
            border_style="bright_cyan"
        ))
        
        # Show initial status
        self.display_emotional_status()
        
        conversation_count = 0
        
        try:
            while True:
                console.print()
                user_input = Prompt.ask("💬 [bold bright_cyan]Share your thoughts[/bold bright_cyan]")
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    break
                
                if user_input.lower() in ['status', '/status']:
                    self.display_emotional_status()
                    continue
                
                if user_input.lower() in ['memory', '/memory']:
                    self.show_memory_summary()
                    continue
                
                # Generate response
                response, emotions, dominant_emotion = self.generate_response(user_input)
                
                # Display emotion analysis
                emotion_text = Text()
                emotion_text.append("📊 Detected: ", style="dim")
                emotion_text.append(f"{dominant_emotion}", style="bold bright_yellow")
                
                if emotions and max(emotions.values()) > 0:
                    intensity = max(emotions.values())
                    emotion_text.append(f" (intensity: {intensity:.2f})", style="dim")
                
                console.print(emotion_text)
                
                # Display AI response
                console.print(Panel(
                    response,
                    title=f"🤖 AI Response (Evolved {self.personality.interaction_count} times)",
                    border_style="bright_green"
                ))
                
                conversation_count += 1
                
                # Show evolution milestone
                if conversation_count % 5 == 0:
                    console.print()
                    console.print("✨ [bright_magenta]I'm learning about you and evolving my personality![/bright_magenta]")
                    console.print("💡 [dim]Type '/status' to see how I've changed[/dim]")
        
        except KeyboardInterrupt:
            pass
        finally:
            console.print()
            console.print(Panel(
                Text.assemble(
                    ("Thank you for helping me grow! 🌱\n", "bright_green"),
                    ("I've evolved through our ", "bright_white"),
                    (f"{self.personality.interaction_count}", "bold bright_yellow"),
                    (" interactions.\n", "bright_white"),
                    ("Your emotional patterns are safely stored in my memory. 💾\n\n", "bright_blue"),
                    ("Until next time! 👋\n", "bright_cyan"),
                    ("Created by Dippu Kumar", "dim italic")
                ),
                title="🧠 Emotional Memory AI - Goodbye",
                border_style="bright_magenta"
            ))
    
    def show_memory_summary(self):
        """Show summary of emotional memories"""
        context = self.memory_system.get_emotional_context(days_back=30)
        
        summary_table = Table(title="📚 Emotional Memory Summary (Last 30 Days)")
        summary_table.add_column("Aspect", style="cyan")
        summary_table.add_column("Details", style="green")
        
        summary_table.add_row("Total Memories", str(len(self.memory_system.memories)))
        summary_table.add_row("Recent Interactions", str(context.get('total_interactions', 0)))
        summary_table.add_row("Mood Trend", context.get('mood_trend', 'unknown').title())
        
        if context.get('dominant_emotions'):
            emotions_str = ", ".join([f"{emotion} ({count})" for emotion, count in context['dominant_emotions']])
            summary_table.add_row("Top Emotions", emotions_str)
        
        console.print(Panel(summary_table, border_style="bright_blue"))

def main():
    """Main function"""
    try:
        ai = EmotionalMemoryAI()
        ai.chat_loop()
    except Exception as e:
        console.print(f"❌ [bold red]Error:[/bold red] {e}")

if __name__ == "__main__":
    main()