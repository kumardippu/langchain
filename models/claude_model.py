"""
Anthropic Claude Model Implementation
"""

import os
import getpass
from typing import List, Dict, Any
from langchain.schema import BaseMessage, AIMessage
from .base_model import BaseAIModel

try:
    from langchain_anthropic import ChatAnthropic

    CLAUDE_AVAILABLE = True
except ImportError:
    CLAUDE_AVAILABLE = False


class ClaudeModel(BaseAIModel):
    """Anthropic Claude Model implementation"""

    def __init__(self, model_name: str = "claude-3-haiku-20240307", **kwargs):
        if not CLAUDE_AVAILABLE:
            raise ImportError(
                "Anthropic package not installed. Run: pip install langchain-anthropic"
            )
        super().__init__(model_name, **kwargs)

    def _setup_model(self) -> None:
        """Initialize Claude model"""
        self._ensure_api_key()

        self.model = ChatAnthropic(
            model=self.model_name,
            temperature=self.config.get("temperature", 0.7),
            max_tokens=self.config.get("max_tokens", 1000),
            api_key=os.environ.get("ANTHROPIC_API_KEY"),
        )

    def _ensure_api_key(self) -> None:
        """Ensure Anthropic API key is available"""
        if not os.environ.get("ANTHROPIC_API_KEY"):
            api_key = getpass.getpass("Enter Anthropic API Key: ")
            os.environ["ANTHROPIC_API_KEY"] = api_key

    def invoke(self, messages: List[BaseMessage]) -> BaseMessage:
        """Send messages to Claude and get response"""
        try:
            response = self.model.invoke(messages)
            return response
        except Exception as e:
            return AIMessage(content=f"Error: {str(e)}")

    def stream(self, messages: List[BaseMessage]) -> Any:
        """Stream response from Claude"""
        try:
            return self.model.stream(messages)
        except Exception as e:
            yield AIMessage(content=f"Error: {str(e)}")

    def get_available_models(self) -> List[Dict[str, str]]:
        """Get available Claude models"""
        return [
            {
                "name": "claude-3-haiku-20240307",
                "description": "Fast and cost-effective Claude model",
                "best_for": "Quick responses, simple tasks",
            },
            {
                "name": "claude-3-sonnet-20240229",
                "description": "Balanced performance and capability",
                "best_for": "Most tasks, good balance",
            },
            {
                "name": "claude-3-opus-20240229",
                "description": "Most capable Claude model",
                "best_for": "Complex reasoning, creative tasks",
            },
            {
                "name": "claude-3-5-sonnet-20241022",
                "description": "Latest improved Sonnet model",
                "best_for": "Enhanced reasoning and analysis",
            },
        ]

    def validate_api_key(self) -> bool:
        """Validate Anthropic API key"""
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
        return "Anthropic Claude"

    @property
    def requires_api_key(self) -> bool:
        return True
