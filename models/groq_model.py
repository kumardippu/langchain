"""
Groq Model Implementation
Author: Dippu Kumar
Fast and free AI model using Groq's inference engine
"""

import getpass
import os
from typing import Any, Dict, List

from langchain.schema import AIMessage, BaseMessage

from .base_model import BaseAIModel

try:
    from langchain_groq import ChatGroq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False


class GroqModel(BaseAIModel):
    """Groq Model implementation - Fast and Free AI"""

    def __init__(self, model_name: str = "llama3-8b-8192", **kwargs):
        if not GROQ_AVAILABLE:
            raise ImportError(
                "Groq package not installed. Run: pip install langchain-groq"
            )
        super().__init__(model_name, **kwargs)

    def _setup_model(self) -> None:
        """Initialize Groq model"""
        self._ensure_api_key()

        self.model = ChatGroq(
            model=self.model_name,
            temperature=self.config.get("temperature", 0.7),
            max_tokens=self.config.get("max_tokens", 1000),
            api_key=os.environ.get("GROQ_API_KEY"),
        )

    def _ensure_api_key(self) -> None:
        """Ensure Groq API key is available"""
        if not os.environ.get("GROQ_API_KEY"):
            print("🔑 Get your free Groq API key from: https://console.groq.com/keys")
            api_key = getpass.getpass("Enter Groq API Key: ")
            os.environ["GROQ_API_KEY"] = api_key

    def invoke(self, messages: List[BaseMessage]) -> BaseMessage:
        """Send messages to Groq and get response"""
        try:
            response = self.model.invoke(messages)
            return response
        except Exception as e:
            # Re-raise the exception so it can be handled by the automatic switching logic
            raise e

    def stream(self, messages: List[BaseMessage]) -> Any:
        """Stream response from Groq"""
        try:
            return self.model.stream(messages)
        except Exception as e:
            yield AIMessage(content=f"Error: {str(e)}")

    def get_available_models(self) -> List[Dict[str, str]]:
        """Get available Groq models"""
        return [
            {
                "name": "llama3-8b-8192",
                "description": "Meta Llama 3 8B - Fast and lightweight",
                "best_for": "Quick responses, general chat, coding help",
            },
            {
                "name": "llama3-70b-8192", 
                "description": "Meta Llama 3 70B - More capable and powerful",
                "best_for": "Complex reasoning, detailed analysis",
            },
            {
                "name": "gemma-7b-it",
                "description": "Google Gemma 7B Instruct - Good for instructions",
                "best_for": "Following instructions, structured tasks",
            },
            {
                "name": "llama3-groq-70b-8192-tool-use-preview",
                "description": "Llama 3 70B with tool use capabilities (preview)",
                "best_for": "Function calling, tool integration",
            },
        ]

    def validate_api_key(self) -> bool:
        """Validate Groq API key"""
        try:
            # Try a simple request to validate the key
            from langchain.schema import HumanMessage
            
            test_messages = [HumanMessage(content="Hello")]
            response = self.model.invoke(test_messages)
            return True
        except:
            return False

    @property
    def provider_name(self) -> str:
        return "Groq"

    @property
    def requires_api_key(self) -> bool:
        return True

    @property
    def is_free_tier_available(self) -> bool:
        """Groq offers generous free tier"""
        return True

    @property  
    def free_tier_details(self) -> Dict[str, Any]:
        """Details about Groq's free tier"""
        return {
            "requests_per_day": 6000,
            "tokens_per_minute": 30000,
            "concurrent_requests": 30,
            "cost": "Free",
            "signup_required": True,
            "credit_card_required": False,
        }
