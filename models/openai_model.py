"""
OpenAI Model Implementation
"""

import getpass
import os
from typing import Any, Dict, List

from langchain.schema import AIMessage, BaseMessage

from .base_model import BaseAIModel

try:
    from langchain_openai import ChatOpenAI

    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class OpenAIModel(BaseAIModel):
    """OpenAI Model implementation"""

    def __init__(self, model_name: str = "gpt-3.5-turbo", **kwargs):
        if not OPENAI_AVAILABLE:
            raise ImportError(
                "OpenAI package not installed. Run: pip install langchain-openai"
            )
        super().__init__(model_name, **kwargs)

    def _setup_model(self) -> None:
        """Initialize OpenAI model"""
        self._ensure_api_key()

        self.model = ChatOpenAI(
            model=self.model_name,
            temperature=self.config.get("temperature", 0.7),
            max_tokens=self.config.get("max_tokens", 1000),
            api_key=os.environ.get("OPENAI_API_KEY"),
        )

    def _ensure_api_key(self) -> None:
        """Ensure OpenAI API key is available"""
        if not os.environ.get("OPENAI_API_KEY"):
            api_key = getpass.getpass("Enter OpenAI API Key: ")
            os.environ["OPENAI_API_KEY"] = api_key

    def invoke(self, messages: List[BaseMessage]) -> BaseMessage:
        """Send messages to OpenAI and get response"""
        try:
            response = self.model.invoke(messages)
            return response
        except Exception as e:
            # Re-raise the exception so it can be handled by the automatic switching logic
            raise e

    def stream(self, messages: List[BaseMessage]) -> Any:
        """Stream response from OpenAI"""
        try:
            return self.model.stream(messages)
        except Exception as e:
            yield AIMessage(content=f"Error: {str(e)}")

    def get_available_models(self) -> List[Dict[str, str]]:
        """Get available OpenAI models"""
        return [
            {
                "name": "gpt-3.5-turbo",
                "description": "Fast and cost-effective model",
                "best_for": "General chat, simple tasks",
            },
            {
                "name": "gpt-4",
                "description": "Most capable GPT-4 model",
                "best_for": "Complex reasoning, analysis",
            },
            {
                "name": "gpt-4-turbo",
                "description": "Faster GPT-4 with larger context",
                "best_for": "Long conversations, complex tasks",
            },
            {
                "name": "gpt-4o",
                "description": "Latest optimized GPT-4 model",
                "best_for": "Best performance and speed",
            },
        ]

    def validate_api_key(self) -> bool:
        """Validate OpenAI API key"""
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
        return "OpenAI"

    @property
    def requires_api_key(self) -> bool:
        return True
