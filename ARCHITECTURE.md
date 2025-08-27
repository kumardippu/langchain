# Universal AI Chatbot Architecture

**Author: Dippu Kumar**

## 🏗️ Factory Pattern Design

This project implements a **Factory Pattern** for AI model management, making it easy to switch between different AI providers (Gemini, Groq, OpenAI, Claude) without changing the core chatbot logic. It also includes **intelligent quota management** with automatic provider switching.

## 📁 Project Structure

```
langchain/
├── models/                     # AI Model implementations
│   ├── __init__.py            # Package exports
│   ├── base_model.py          # Abstract base class
│   ├── gemini_model.py        # Google Gemini implementation
│   ├── groq_model.py          # Groq implementation (Ultrafast)
│   ├── openai_model.py        # OpenAI implementation
│   ├── claude_model.py        # Anthropic Claude implementation
│   └── model_factory.py       # Factory for creating models
├── g.py                       # Simple basic chatbot
├── enhanced_chat.py           # Enhanced chatbot (reference)
├── universal_chatbot.py       # Universal multi-provider chatbot
├── run_chatbot.py            # Launcher script
├── config.yaml               # Configuration file
├── requirements.txt          # Dependencies
└── README.md                 # Main documentation
```

## 🎯 Design Patterns Used

### 1. **Factory Pattern**
- **Purpose**: Create AI model instances without specifying exact classes
- **Benefits**: Easy to add new providers, switch models at runtime
- **Implementation**: `ModelFactory` class in `models/model_factory.py`

### 2. **Abstract Base Class (ABC)**
- **Purpose**: Define contract for all AI model implementations
- **Benefits**: Ensures consistency, enables polymorphism
- **Implementation**: `BaseAIModel` in `models/base_model.py`

### 3. **Strategy Pattern**
- **Purpose**: Different AI providers as interchangeable strategies
- **Benefits**: Runtime switching, easy testing
- **Implementation**: Each model class implements the same interface

## 🔧 Key Components

### BaseAIModel (Abstract Base Class)

```python
class BaseAIModel(ABC):
    @abstractmethod
    def invoke(self, messages: List[BaseMessage]) -> BaseMessage:
        """Send messages to AI and get response"""
        pass
    
    @abstractmethod
    def stream(self, messages: List[BaseMessage]) -> Any:
        """Stream response from AI"""
        pass
    
    @abstractmethod
    def get_available_models(self) -> List[Dict[str, str]]:
        """Get list of available models"""
        pass
```

### ModelFactory

```python
# Easy model creation
model = ModelFactory.create_model('gemini', 'gemini-1.5-flash')
model = ModelFactory.create_model('openai', 'gpt-4')
model = ModelFactory.create_model('claude', 'claude-3-sonnet')

# Runtime provider switching
available_providers = ModelFactory.get_available_providers()
```

### Configuration-Driven

```yaml
ai_provider:
  provider: "gemini"        # Switch between: gemini, groq, openai, claude
  model: "gemini-1.5-flash" # Model name
  temperature: 0.7          # Parameters
```

## 🔄 How to Add New AI Providers

### Step 1: Create Model Implementation

```python
# models/new_provider_model.py
from .base_model import BaseAIModel

class NewProviderModel(BaseAIModel):
    def _setup_model(self):
        # Initialize the new provider's client
        pass
    
    def invoke(self, messages):
        # Implement message sending
        pass
    
    def stream(self, messages):
        # Implement streaming
        pass
    
    # ... implement other abstract methods
```

### Step 2: Register in Factory

```python
# models/model_factory.py
from .new_provider_model import NewProviderModel

class ModelFactory:
    _models = {
        'gemini': GeminiModel,
        'groq': GroqModel,
        'openai': OpenAIModel,
        'claude': ClaudeModel,
        'newprovider': NewProviderModel  # Add here
    }
```

### Step 3: Update Configuration

```yaml
# config.yaml
providers:
  newprovider:
    default_model: "new-model-name"
    models:
      - "new-model-name"
      - "another-model"
```

### Step 4: Add Dependencies

```
# requirements.txt
# New Provider (optional)
# new-provider-package>=1.0.0
```

## 🎮 Usage Examples

### Basic Usage

```python
from models import ModelFactory

# Create any model using factory
model = ModelFactory.create_model('gemini')
response = model.invoke([HumanMessage("Hello!")])
print(response.content)
```

### Runtime Switching

```python
# Switch providers easily
providers = ['gemini', 'groq', 'openai', 'claude']

for provider in providers:
    if ModelFactory.is_provider_available(provider):
        model = ModelFactory.create_model(provider)
        response = model.invoke([HumanMessage("Hello!")])
        print(f"{provider}: {response.content}")
```

### Configuration-Based

```python
# Load from config
config = load_config('config.yaml')
provider = config['ai_provider']['provider']
model_name = config['ai_provider']['model']

model = ModelFactory.create_model(provider, model_name)
```

## 🏃‍♂️ Running Different Versions

### Option 1: Launcher Script
```bash
python run_chatbot.py
# Interactive menu to choose chatbot version
```

### Option 2: Direct Execution
```bash
# Simple version (single interaction)
python g.py

# Enhanced version (conversation history, rich UI)
python enhanced_chat.py

# Universal version (multi-provider, factory pattern)
python universal_chatbot.py
```

## 🔧 Benefits of This Architecture

### 1. **Flexibility**
- Switch AI providers without code changes
- Runtime provider switching
- Easy A/B testing

### 2. **Maintainability**
- Clear separation of concerns
- Each provider in its own module
- Consistent interface across providers

### 3. **Extensibility**
- Add new providers easily
- Minimal changes to existing code
- Plugin-like architecture

### 4. **Testability**
- Mock any provider for testing
- Test each provider independently
- Consistent testing interface

### 5. **Production Ready**
- Error handling and fallbacks
- Configuration-driven
- Graceful degradation

## 🚀 Advanced Features

### 🧠 Intelligent Quota Management

The Universal Chatbot includes smart quota management that automatically switches providers when limits are reached:

```python
# Automatic quota detection and switching
class UniversalChatBot:
    def is_quota_error(self, error_message: str) -> bool:
        """Detect various quota error patterns"""
        quota_indicators = [
            "quota", "rate limit", "429",
            "generativelanguage.googleapis.com/generate_content_free_tier_requests",
            "exceeded your current quota"
        ]
        return any(indicator in error_message.lower() for indicator in quota_indicators)
    
    def auto_switch_provider(self, exclude_provider: str = None) -> bool:
        """Smart provider switching with priority system"""
        # Special priority: Gemini → Groq (free & fast)
        if current_provider == "gemini":
            provider_priority = ["groq", "openai", "claude"]
        else:
            provider_priority = ["openai", "groq", "claude", "gemini"]
        
        # Try each provider in priority order
        for provider in provider_priority:
            try:
                self.setup_model(provider)
                return True
            except Exception:
                continue
        return False
```

**Key Features:**
- ✅ **Smart Detection**: Recognizes quota errors from different providers
- ✅ **Priority Switching**: Gemini → Groq (optimized for free tier users)
- ✅ **Conversation Preservation**: History maintained across switches
- ✅ **Retry Logic**: Up to 3 attempts to find working providers
- ✅ **User Notifications**: Clear messages about switches and reasons

### Auto-Fallback
```python
# Automatically fallback to available provider
try:
    model = ModelFactory.create_model('preferred_provider')
except:
    model = ModelFactory.create_model('fallback_provider')
```

### Provider Health Checks
```python
# Check if provider is working
if model.validate_api_key():
    print("Provider is healthy")
else:
    print("Provider has issues")
```

### Model Comparison
```python
# Compare responses from different providers
providers = ['gemini', 'groq', 'openai', 'claude']
question = "Explain quantum computing"

for provider in providers:
    model = ModelFactory.create_model(provider)
    response = model.invoke([HumanMessage(question)])
    print(f"{provider}: {response.content}")
```

### Quota-Aware Usage Pattern
```python
# Production-ready pattern with quota management
class ProductionChatBot:
    def __init__(self):
        self.primary_provider = "gemini"
        self.fallback_providers = ["groq", "openai", "claude"]
        self.current_model = None
        self.setup_model(self.primary_provider)
    
    def chat(self, message: str) -> str:
        max_retries = len(self.fallback_providers) + 1
        
        for retry in range(max_retries):
            try:
                response = self.current_model.invoke([HumanMessage(message)])
                return response.content
            except Exception as e:
                if self.is_quota_error(str(e)) and retry < max_retries - 1:
                    # Switch to next available provider
                    next_provider = self.fallback_providers[retry]
                    self.setup_model(next_provider)
                    continue
                else:
                    raise e
```

## 📝 Best Practices

1. **Always use the factory** instead of importing models directly
2. **Handle ImportError** for optional dependencies gracefully
3. **Use configuration files** for provider settings
4. **Implement proper error handling** in model implementations
5. **Follow the interface contract** defined in BaseAIModel
6. **Add comprehensive tests** for new providers
7. **🆕 Implement quota-aware patterns** for production use
8. **🆕 Use Groq as fallback** for cost-effective scaling
9. **🆕 Design with auto-switching** in mind from the start

## 🎯 Architecture Benefits

### 🔄 **Intelligent Resilience**
- **Quota Management**: Never get stuck by API limits
- **Smart Fallbacks**: Automatic provider switching with priority logic
- **Error Recovery**: Graceful handling of provider failures

### 💰 **Cost Optimization**
- **Free Tier Maximization**: Gemini → Groq switching optimizes free usage
- **Provider Diversity**: Spread load across multiple providers
- **Dynamic Scaling**: Switch to paid tiers only when needed

### 👤 **User Experience**
- **Zero Interruption**: Seamless conversations across provider switches
- **Transparent Operation**: Clear notifications about switches
- **History Preservation**: Conversation context maintained

### 🏗️ **Developer Experience**
- **Simple Integration**: Factory pattern abstracts complexity
- **Easy Extension**: Add new providers with minimal code
- **Configuration-Driven**: No code changes for provider switches

This architecture makes your chatbot future-proof and highly maintainable while providing excellent user experience across different AI providers! 🎯