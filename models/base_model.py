"""
Base model interface for AI chatbot
Author: Dippu Kumar
Defines the contract that all AI model implementations must follow
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from langchain.schema import BaseMessage


class BaseAIModel(ABC):
    """Abstract base class for AI models"""
    
    def __init__(self, model_name: str, **kwargs):
        self.model_name = model_name
        self.config = kwargs
        self._setup_model()
    
    @abstractmethod
    def _setup_model(self) -> None:
        """Initialize the specific AI model"""
        pass
    
    @abstractmethod
    def invoke(self, messages: List[BaseMessage]) -> BaseMessage:
        """Send messages to the AI model and get response"""
        pass
    
    @abstractmethod
    def stream(self, messages: List[BaseMessage]) -> Any:
        """Stream response from the AI model"""
        pass
    
    @abstractmethod
    def get_available_models(self) -> List[Dict[str, str]]:
        """Get list of available models for this provider"""
        pass
    
    @abstractmethod
    def validate_api_key(self) -> bool:
        """Validate that the API key is working"""
        pass
    
    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Return the name of the AI provider"""
        pass
    
    @property
    @abstractmethod
    def requires_api_key(self) -> bool:
        """Return True if this model requires an API key"""
        pass
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model"""
        return {
            "provider": self.provider_name,
            "model_name": self.model_name,
            "config": self.config
        }