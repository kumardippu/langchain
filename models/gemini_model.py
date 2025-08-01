"""
Google Gemini AI Model Implementation
"""

import os
import getpass
from typing import List, Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import BaseMessage, AIMessage
from .base_model import BaseAIModel


class GeminiModel(BaseAIModel):
    """Google Gemini AI Model implementation"""
    
    def __init__(self, model_name: str = "gemini-1.5-flash", **kwargs):
        super().__init__(model_name, **kwargs)
    
    def _setup_model(self) -> None:
        """Initialize Gemini model"""
        self._ensure_api_key()
        
        self.model = ChatGoogleGenerativeAI(
            model=self.model_name,
            temperature=self.config.get('temperature', 0.7),
            max_tokens=self.config.get('max_tokens', 1000)
        )
    
    def _ensure_api_key(self) -> None:
        """Ensure Google API key is available"""
        if not os.environ.get("GOOGLE_API_KEY"):
            api_key = getpass.getpass("Enter Google API Key: ")
            os.environ["GOOGLE_API_KEY"] = api_key
    
    def invoke(self, messages: List[BaseMessage]) -> BaseMessage:
        """Send messages to Gemini and get response"""
        try:
            response = self.model.invoke(messages)
            return response
        except Exception as e:
            return AIMessage(content=f"Error: {str(e)}")
    
    def stream(self, messages: List[BaseMessage]) -> Any:
        """Stream response from Gemini"""
        try:
            return self.model.stream(messages)
        except Exception as e:
            yield AIMessage(content=f"Error: {str(e)}")
    
    def get_available_models(self) -> List[Dict[str, str]]:
        """Get available Gemini models"""
        return [
            {
                "name": "gemini-1.5-flash",
                "description": "Fast, efficient model for quick responses",
                "best_for": "Chat, quick questions"
            },
            {
                "name": "gemini-1.5-pro", 
                "description": "More capable model for complex tasks",
                "best_for": "Complex reasoning, analysis"
            },
            {
                "name": "gemini-2.0-flash-exp",
                "description": "Latest experimental model", 
                "best_for": "Cutting-edge features"
            }
        ]
    
    def validate_api_key(self) -> bool:
        """Validate Google API key"""
        try:
            # Try a simple request to validate the key
            test_messages = [BaseMessage(content="Hello", type="human")]
            response = self.model.invoke(test_messages)
            return True
        except:
            return False
    
    @property
    def provider_name(self) -> str:
        return "Google Gemini"
    
    @property 
    def requires_api_key(self) -> bool:
        return True