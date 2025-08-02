"""
Model Factory for creating AI model instances
Author: Dippu Kumar
Implements the Factory Pattern for easy model switching
"""

from typing import Dict, Type, List, Optional
from .base_model import BaseAIModel
from .gemini_model import GeminiModel
from .openai_model import OpenAIModel
from .claude_model import ClaudeModel


class ModelFactory:
    """Factory class for creating AI model instances"""

    # Registry of available model providers
    _models: Dict[str, Type[BaseAIModel]] = {
        "gemini": GeminiModel,
        "openai": OpenAIModel,
        "claude": ClaudeModel,
    }

    # Default models for each provider
    _default_models: Dict[str, str] = {
        "gemini": "gemini-1.5-flash",
        "openai": "gpt-3.5-turbo",
        "claude": "claude-3-haiku-20240307",
    }

    @classmethod
    def create_model(
        self, provider: str, model_name: Optional[str] = None, **kwargs
    ) -> BaseAIModel:
        """
        Create an AI model instance

        Args:
            provider: The AI provider ('gemini', 'openai', 'claude')
            model_name: Specific model name (optional, uses default if not provided)
            **kwargs: Additional configuration parameters

        Returns:
            BaseAIModel: An instance of the requested AI model

        Raises:
            ValueError: If provider is not supported
        """
        provider = provider.lower()

        if provider not in self._models:
            available = ", ".join(self._models.keys())
            raise ValueError(
                f"Unsupported provider '{provider}'. Available: {available}"
            )

        # Use default model if none specified
        if model_name is None:
            model_name = self._default_models[provider]

        model_class = self._models[provider]

        try:
            return model_class(model_name=model_name, **kwargs)
        except ImportError as e:
            raise ImportError(f"Failed to import {provider} model: {e}")
        except Exception as e:
            raise RuntimeError(f"Failed to create {provider} model: {e}")

    @classmethod
    def get_available_providers(self) -> List[str]:
        """Get list of available AI providers"""
        return list(self._models.keys())

    @classmethod
    def get_provider_models(self, provider: str) -> List[Dict[str, str]]:
        """
        Get available models for a specific provider

        Args:
            provider: The AI provider name

        Returns:
            List of model information dictionaries
        """
        provider = provider.lower()

        if provider not in self._models:
            return []

        try:
            # Create a temporary instance to get model info
            model_class = self._models[provider]
            temp_instance = model_class.__new__(model_class)
            return temp_instance.get_available_models()
        except:
            return []

    @classmethod
    def register_model(self, provider: str, model_class: Type[BaseAIModel]) -> None:
        """
        Register a new AI model provider

        Args:
            provider: Name of the provider
            model_class: Model class that implements BaseAIModel
        """
        if not issubclass(model_class, BaseAIModel):
            raise TypeError("Model class must inherit from BaseAIModel")

        self._models[provider.lower()] = model_class

    @classmethod
    def is_provider_available(self, provider: str) -> bool:
        """
        Check if a provider is available and can be imported

        Args:
            provider: The AI provider name

        Returns:
            bool: True if provider is available
        """
        provider = provider.lower()

        if provider not in self._models:
            return False

        try:
            model_class = self._models[provider]
            # Try to create a dummy instance to check imports
            temp_instance = model_class.__new__(model_class)
            return True
        except ImportError:
            return False
        except:
            return True  # Other errors don't mean the provider is unavailable

    @classmethod
    def get_model_info(self, provider: str, model_name: Optional[str] = None) -> Dict:
        """
        Get information about a specific model

        Args:
            provider: The AI provider name
            model_name: Specific model name (optional)

        Returns:
            Dict: Model information
        """
        try:
            model = self.create_model(provider, model_name)
            return model.get_model_info()
        except Exception as e:
            return {"error": str(e)}


# Convenience functions for easy model creation
def create_gemini_model(model_name: str = "gemini-1.5-flash", **kwargs) -> GeminiModel:
    """Create a Gemini model instance"""
    return ModelFactory.create_model("gemini", model_name, **kwargs)


def create_openai_model(model_name: str = "gpt-3.5-turbo", **kwargs) -> OpenAIModel:
    """Create an OpenAI model instance"""
    return ModelFactory.create_model("openai", model_name, **kwargs)


def create_claude_model(
    model_name: str = "claude-3-haiku-20240307", **kwargs
) -> ClaudeModel:
    """Create a Claude model instance"""
    return ModelFactory.create_model("claude", model_name, **kwargs)
