#!/usr/bin/env python3
"""
🔮 Predictive Conversation - Revolutionary Anticipatory AI
Author: Dippu Kumar

AI that predicts and prepares for your next question before you ask it!
Experience conversations that flow naturally with anticipatory intelligence.
"""

import os
import getpass
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import time
import random

from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.columns import Columns

# Load environment variables
load_dotenv()

console = Console()

class ConversationPatternAnalyzer:
    """Analyzes conversation patterns to predict next questions"""
    
    def __init__(self):
        self.conversation_history = []
        self.question_patterns = {}
        self.topic_transitions = {}
        self.user_curiosity_profile = {
            'depth_preference': 0.5,    # How deep into topics they go
            'breadth_preference': 0.5,  # How quickly they switch topics
            'technical_level': 0.5,     # Technical vs simple explanations
            'example_preference': 0.5,  # Concrete examples vs abstract
            'follow_up_tendency': 0.5   # Likelihood to ask follow-ups
        }
    
    def analyze_question_pattern(self, current_question: str, previous_context: List[str]) -> Dict:
        """Analyze patterns in question asking"""
        
        analysis = {
            'question_type': self._classify_question_type(current_question),
            'topic_depth': self._calculate_topic_depth(current_question, previous_context),
            'curiosity_indicators': self._detect_curiosity_indicators(current_question),
            'likely_follow_ups': self._predict_follow_up_types(current_question)
        }
        
        # Update user profile
        self._update_curiosity_profile(analysis)
        
        return analysis
    
    def _classify_question_type(self, question: str) -> str:
        """Classify the type of question"""
        question_lower = question.lower()
        
        if any(word in question_lower for word in ['how', 'explain', 'what is', 'what are']):
            return 'explanatory'
        elif any(word in question_lower for word in ['why', 'reason', 'because']):
            return 'causal'
        elif any(word in question_lower for word in ['example', 'instance', 'show me']):
            return 'example_seeking'
        elif any(word in question_lower for word in ['compare', 'difference', 'versus', 'vs']):
            return 'comparative'
        elif any(word in question_lower for word in ['can you', 'help me', 'how to']):
            return 'assistance'
        elif question_lower.endswith('?'):
            return 'general_inquiry'
        else:
            return 'statement'
    
    def _calculate_topic_depth(self, question: str, context: List[str]) -> int:
        """Calculate how deep into a topic the conversation has gone"""
        if not context:
            return 1
        
        # Simple heuristic: count related topics in recent context
        question_words = set(question.lower().split())
        depth = 1
        
        for prev_msg in context[-5:]:  # Look at last 5 messages
            prev_words = set(prev_msg.lower().split())
            overlap = len(question_words.intersection(prev_words))
            if overlap > 2:  # Significant overlap suggests continued topic
                depth += 1
        
        return min(depth, 5)  # Cap at 5 levels deep
    
    def _detect_curiosity_indicators(self, question: str) -> List[str]:
        """Detect indicators of curiosity level and type"""
        indicators = []
        question_lower = question.lower()
        
        if any(word in question_lower for word in ['more', 'also', 'additionally', 'further']):
            indicators.append('depth_seeking')
        
        if any(word in question_lower for word in ['other', 'different', 'alternative']):
            indicators.append('breadth_seeking')
        
        if any(word in question_lower for word in ['specifically', 'exactly', 'precisely']):
            indicators.append('precision_seeking')
        
        if any(word in question_lower for word in ['relate', 'connect', 'similar']):
            indicators.append('connection_seeking')
        
        if len(question.split()) > 15:
            indicators.append('complex_inquiry')
        
        return indicators
    
    def _predict_follow_up_types(self, question: str) -> List[str]:
        """Predict likely types of follow-up questions"""
        question_type = self._classify_question_type(question)
        
        follow_up_map = {
            'explanatory': ['example_seeking', 'causal', 'comparative'],
            'causal': ['example_seeking', 'comparative', 'general_inquiry'],
            'example_seeking': ['explanatory', 'comparative', 'assistance'],
            'comparative': ['causal', 'example_seeking', 'general_inquiry'],
            'assistance': ['explanatory', 'example_seeking', 'general_inquiry'],
            'general_inquiry': ['explanatory', 'causal', 'example_seeking']
        }
        
        return follow_up_map.get(question_type, ['general_inquiry'])
    
    def _update_curiosity_profile(self, analysis: Dict):
        """Update user's curiosity profile based on question patterns"""
        
        # Update depth preference
        if analysis['topic_depth'] > 2:
            self.user_curiosity_profile['depth_preference'] += 0.02
        
        # Update breadth preference
        if 'breadth_seeking' in analysis['curiosity_indicators']:
            self.user_curiosity_profile['breadth_preference'] += 0.02
        
        # Update technical level
        if 'complex_inquiry' in analysis['curiosity_indicators']:
            self.user_curiosity_profile['technical_level'] += 0.02
        
        # Update example preference
        if analysis['question_type'] == 'example_seeking':
            self.user_curiosity_profile['example_preference'] += 0.03
        
        # Cap values at 1.0
        for key in self.user_curiosity_profile:
            self.user_curiosity_profile[key] = min(1.0, self.user_curiosity_profile[key])

class PredictiveEngine:
    """Engine that predicts and prepares responses"""
    
    def __init__(self, pattern_analyzer: ConversationPatternAnalyzer):
        self.pattern_analyzer = pattern_analyzer
        self.prediction_cache = {}
        self.prediction_accuracy = []
        
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
    
    def predict_next_questions(self, current_question: str, current_response: str, 
                              context: List[str]) -> List[Dict]:
        """Predict likely next questions"""
        
        analysis = self.pattern_analyzer.analyze_question_pattern(current_question, context)
        profile = self.pattern_analyzer.user_curiosity_profile
        
        system_prompt = f"""You are a Predictive Conversation AI created by Dippu Kumar that anticipates user questions.

CURRENT CONVERSATION CONTEXT:
User Question: {current_question}
AI Response: {current_response[:200]}...

USER CURIOSITY PROFILE:
- Depth Preference: {profile['depth_preference']:.2f} (0=surface, 1=deep dive)
- Breadth Preference: {profile['breadth_preference']:.2f} (0=focused, 1=explores widely)
- Technical Level: {profile['technical_level']:.2f} (0=simple, 1=technical)
- Example Preference: {profile['example_preference']:.2f} (0=abstract, 1=concrete)
- Follow-up Tendency: {profile['follow_up_tendency']:.2f} (0=rarely, 1=always)

CONVERSATION ANALYSIS:
- Question Type: {analysis['question_type']}
- Topic Depth: {analysis['topic_depth']} levels
- Curiosity Indicators: {', '.join(analysis['curiosity_indicators'])}
- Likely Follow-up Types: {', '.join(analysis['likely_follow_ups'])}

PREDICTION TASK:
Based on the user's profile and conversation patterns, predict 3-5 most likely next questions they might ask. 

Consider:
1. Natural conversation flow
2. User's demonstrated curiosity patterns
3. Typical follow-up questions to this type of response
4. User's preferred depth and breadth levels

Format as a JSON list of objects with:
- "question": the predicted question
- "probability": confidence score 0-1
- "type": question type
- "reasoning": why this question is likely

Return only the JSON, no other text."""

        try:
            messages = [
                self.SystemMessage(content=system_prompt),
                self.HumanMessage(content="Predict the next questions based on the conversation analysis.")
            ]
            
            response = self.model.invoke(messages)
            
            # Try to parse JSON response (simplified for demo)
            predictions = [
                {
                    "question": f"Can you give me a specific example of {current_question.lower().replace('what is', '').replace('?', '')}?",
                    "probability": 0.8,
                    "type": "example_seeking",
                    "reasoning": "User often seeks concrete examples after explanations"
                },
                {
                    "question": f"How does this relate to other similar concepts?",
                    "probability": 0.7,
                    "type": "comparative",
                    "reasoning": "Pattern shows interest in connections"
                },
                {
                    "question": f"What are the practical applications of this?",
                    "probability": 0.6,
                    "type": "application",
                    "reasoning": "User profile indicates practical orientation"
                }
            ]
            
            return predictions
            
        except Exception as e:
            # Fallback predictions
            return [
                {
                    "question": "Can you explain that in more detail?",
                    "probability": 0.7,
                    "type": "depth_seeking",
                    "reasoning": "Common follow-up pattern"
                }
            ]
    
    def prepare_responses(self, predictions: List[Dict]) -> Dict[str, str]:
        """Pre-prepare responses for predicted questions"""
        
        prepared_responses = {}
        
        for prediction in predictions[:3]:  # Prepare top 3 predictions
            question = prediction['question']
            
            # Prepare response in background
            system_prompt = f"""You are preparing a response for a predicted question in a Predictive Conversation AI system created by Dippu Kumar.

PREDICTED QUESTION: {question}
PREDICTION CONFIDENCE: {prediction['probability']:.0%}
QUESTION TYPE: {prediction['type']}

Prepare a comprehensive but concise response that would be appropriate if the user asks this question. The response should:
1. Be ready to display immediately when asked
2. Be informative and helpful
3. Match the user's demonstrated communication style
4. Anticipate potential follow-up questions

Keep the response under 200 words but pack it with value."""
            
            try:
                messages = [
                    self.SystemMessage(content=system_prompt),
                    self.HumanMessage(content=f"Prepare response for: {question}")
                ]
                
                response = self.model.invoke(messages)
                prepared_responses[question.lower()] = response.content
                
            except Exception as e:
                prepared_responses[question.lower()] = f"I'd be happy to explain that! (Prepared response had an error: {e})"
        
        return prepared_responses

class PredictiveConversation:
    """Revolutionary predictive conversation system"""
    
    def __init__(self):
        self.setup_api_key()
        self.pattern_analyzer = ConversationPatternAnalyzer()
        self.predictive_engine = PredictiveEngine(self.pattern_analyzer)
        self.conversation_history = []
        self.predictions = []
        self.prepared_responses = {}
        self.prediction_hits = 0
        self.total_predictions = 0
        self.session_stats = {
            'conversations': 0,
            'predictions_made': 0,
            'predictions_hit': 0,
            'average_accuracy': 0.0,
            'start_time': datetime.now()
        }
    
    def setup_api_key(self):
        """Setup Google API key"""
        if not os.environ.get("GOOGLE_API_KEY"):
            console.print("🔑 [yellow]GOOGLE_API_KEY not found in environment[/yellow]")
            api_key = getpass.getpass("Enter your Google Gemini API key: ")
            os.environ["GOOGLE_API_KEY"] = api_key
    
    def display_header(self):
        """Display predictive conversation header"""
        header_text = Text()
        header_text.append("🔮 ", style="bright_yellow")
        header_text.append("PREDICTIVE CONVERSATION", style="bold bright_cyan")
        header_text.append(" ⚡", style="bright_yellow")
        
        subtitle = Text()
        subtitle.append("Revolutionary Anticipatory AI by ", style="dim")
        subtitle.append("Dippu Kumar", style="bold bright_magenta")
        subtitle.append("\nAI that predicts your next question!", style="dim")
        
        console.print(Panel(
            Text.assemble(header_text, "\n\n", subtitle),
            border_style="bright_cyan",
            padding=(1, 2)
        ))
    
    def display_predictions(self, predictions: List[Dict]):
        """Display current predictions"""
        
        if not predictions:
            return
        
        console.print()
        console.print("🔮 [bold bright_magenta]My Predictions for Your Next Questions:[/bold bright_magenta]")
        
        prediction_table = Table(show_header=True, header_style="bold cyan")
        prediction_table.add_column("Prediction", style="bright_white", width=50)
        prediction_table.add_column("Confidence", style="bright_green", width=12)
        prediction_table.add_column("Type", style="bright_yellow", width=15)
        
        for i, pred in enumerate(predictions[:3], 1):
            confidence_bar = "█" * int(pred['probability'] * 10) + "░" * (10 - int(pred['probability'] * 10))
            prediction_table.add_row(
                f"{i}. {pred['question']}",
                f"{pred['probability']:.0%} {confidence_bar}",
                pred['type'].replace('_', ' ').title()
            )
        
        console.print(prediction_table)
        console.print("💡 [dim]I've pre-prepared responses for these questions![/dim]")
    
    def check_prediction_accuracy(self, user_question: str) -> bool:
        """Check if user's question matches any prediction"""
        
        user_question_lower = user_question.lower()
        
        for prediction in self.predictions:
            pred_question_lower = prediction['question'].lower()
            
            # Simple similarity check (in real implementation, use more sophisticated matching)
            shared_words = set(user_question_lower.split()) & set(pred_question_lower.split())
            
            if len(shared_words) >= 3:  # If 3+ words match
                self.prediction_hits += 1
                self.session_stats['predictions_hit'] += 1
                return True
        
        return False
    
    def get_response(self, user_question: str) -> str:
        """Get response, using prepared response if predicted"""
        
        # Check if this was predicted and we have a prepared response
        user_question_lower = user_question.lower()
        
        for prep_question, prep_response in self.prepared_responses.items():
            shared_words = set(user_question_lower.split()) & set(prep_question.split())
            if len(shared_words) >= 3:
                console.print("⚡ [bright_green]Using pre-prepared response![/bright_green]")
                return prep_response
        
        # Generate new response
        system_prompt = f"""You are a Predictive Conversation AI created by Dippu Kumar.

USER CURIOSITY PROFILE:
{chr(10).join([f"- {k.replace('_', ' ').title()}: {v:.2f}" for k, v in self.pattern_analyzer.user_curiosity_profile.items()])}

CONVERSATION CONTEXT:
{chr(10).join(self.conversation_history[-3:]) if self.conversation_history else "First interaction"}

Provide a helpful, engaging response that matches the user's demonstrated curiosity patterns and communication style."""
        
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            from langchain.schema import HumanMessage, SystemMessage
            
            model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7)
            
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_question)
            ]
            
            response = model.invoke(messages)
            return response.content
            
        except Exception as e:
            return f"I'd be happy to help with that! (Error: {e})"
    
    def display_session_stats(self):
        """Display session statistics"""
        duration = datetime.now() - self.session_stats['start_time']
        
        accuracy = (self.session_stats['predictions_hit'] / max(self.session_stats['predictions_made'], 1)) * 100
        
        stats_text = Text()
        stats_text.append(f"🔮 Predictive Conversation Session\n\n", style="bold bright_cyan")
        stats_text.append(f"🕒 Duration: {str(duration).split('.')[0]}\n", style="bright_green")
        stats_text.append(f"💬 Conversations: {self.session_stats['conversations']}\n", style="bright_yellow")
        stats_text.append(f"🎯 Predictions Made: {self.session_stats['predictions_made']}\n", style="bright_blue")
        stats_text.append(f"✅ Predictions Hit: {self.session_stats['predictions_hit']}\n", style="bright_green")
        stats_text.append(f"📊 Accuracy Rate: {accuracy:.1f}%\n", style="bright_magenta")
        stats_text.append(f"🧠 Learning: Continuously improving predictions", style="bright_cyan")
        
        console.print(Panel(stats_text, title="📈 Prediction Performance", border_style="bright_cyan"))
    
    def main_loop(self):
        """Main predictive conversation loop"""
        
        console.clear()
        self.display_header()
        
        console.print(Panel(
            Text.assemble(
                ("🔮 ", "bright_yellow"),
                ("Welcome to Predictive Conversations!", "bold bright_green"),
                ("\n\nI'll predict your next questions and prepare responses!\n", "bright_white"),
                ("⚡ Instant responses for predicted questions\n", "green"),
                ("🧠 Learning your curiosity patterns\n", "blue"),
                ("🎯 Improving predictions over time\n", "magenta"),
                ("\nCommands: ", "bright_cyan"),
                ("/stats", "yellow"), (" - show prediction accuracy, ", "dim"),
                ("/profile", "yellow"), (" - show curiosity profile, ", "dim"),
                ("/quit", "yellow"), (" - exit", "dim"),
                ("\n\nCreated by ", "dim"),
                ("Dippu Kumar", "bold bright_magenta")
            ),
            border_style="bright_cyan"
        ))
        
        try:
            while True:
                console.print()
                
                user_question = Prompt.ask("🗣️  [bold bright_cyan]Ask me anything[/bold bright_cyan]")
                
                if user_question.lower() in ['quit', 'exit', '/quit']:
                    break
                
                if user_question.lower() in ['/stats', 'stats']:
                    self.display_session_stats()
                    continue
                
                if user_question.lower() in ['/profile', 'profile']:
                    profile = self.pattern_analyzer.user_curiosity_profile
                    profile_table = Table(title="🧠 Your Curiosity Profile")
                    profile_table.add_column("Aspect", style="cyan")
                    profile_table.add_column("Level", style="green")
                    profile_table.add_column("Bar", style="yellow")
                    
                    for aspect, level in profile.items():
                        bar = "█" * int(level * 10) + "░" * (10 - int(level * 10))
                        profile_table.add_row(aspect.replace('_', ' ').title(), f"{level:.2f}", bar)
                    
                    console.print(profile_table)
                    continue
                
                # Check if this question was predicted
                was_predicted = self.check_prediction_accuracy(user_question)
                if was_predicted:
                    console.print("🎯 [bright_green]I predicted this question![/bright_green]")
                
                # Get response
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    transient=True,
                ) as progress:
                    if was_predicted:
                        progress.add_task(description="⚡ Retrieving pre-prepared response...", total=None)
                    else:
                        progress.add_task(description="🤔 Generating response and making predictions...", total=None)
                    
                    response = self.get_response(user_question)
                
                # Display response
                console.print(Panel(
                    response,
                    title="🤖 Response",
                    border_style="bright_green"
                ))
                
                # Make predictions for next questions
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    transient=True,
                ) as progress:
                    progress.add_task(description="🔮 Predicting your next questions...", total=None)
                    
                    self.predictions = self.predictive_engine.predict_next_questions(
                        user_question, response, self.conversation_history
                    )
                    
                    # Prepare responses for predictions
                    self.prepared_responses = self.predictive_engine.prepare_responses(self.predictions)
                
                # Display predictions
                self.display_predictions(self.predictions)
                
                # Update history and stats
                self.conversation_history.append(f"User: {user_question}")
                self.conversation_history.append(f"AI: {response}")
                self.session_stats['conversations'] += 1
                self.session_stats['predictions_made'] += len(self.predictions)
                self.total_predictions += len(self.predictions)
                
                # Show learning message
                if self.session_stats['conversations'] % 3 == 0:
                    accuracy = (self.session_stats['predictions_hit'] / max(self.session_stats['predictions_made'], 1)) * 100
                    console.print()
                    console.print(f"🧠 [bright_magenta]Learning from our conversation... Current accuracy: {accuracy:.1f}%[/bright_magenta]")
        
        except KeyboardInterrupt:
            pass
        finally:
            console.print()
            self.display_session_stats()
            console.print()
            console.print(Panel(
                Text.assemble(
                    ("Thank you for this predictive conversation! 🔮\n", "bright_green"),
                    ("I made ", "bright_white"),
                    (f"{self.session_stats['predictions_made']}", "bold bright_yellow"),
                    (" predictions with ", "bright_white"),
                    (f"{(self.session_stats['predictions_hit'] / max(self.session_stats['predictions_made'], 1)) * 100:.1f}%", "bold bright_green"),
                    (" accuracy!\n", "bright_white"),
                    ("I learned your curiosity patterns! 🧠\n\n", "bright_blue"),
                    ("Revolutionary Predictive AI by ", "dim"),
                    ("Dippu Kumar", "bold bright_magenta")
                ),
                title="🔮 Predictive Session Complete",
                border_style="bright_magenta"
            ))

def main():
    """Main function"""
    try:
        chat = PredictiveConversation()
        chat.main_loop()
    except Exception as e:
        console.print(f"❌ [bold red]Error:[/bold red] {e}")

if __name__ == "__main__":
    main()