# Universal AI Chatbot Architecture

**Author: Dippu Kumar**

## 🏗️ Factory Pattern Design

This project implements a **Factory Pattern** for AI model management, making it easy to switch between different AI providers (Gemini, OpenAI, Claude) without changing the core chatbot logic.

## 📁 Project Structure

```
langchain/
├── models/                     # AI Model implementations
│   ├── __init__.py            # Package exports
│   ├── base_model.py          # Abstract base class
│   ├── gemini_model.py        # Google Gemini implementation
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
  provider: "gemini"        # Switch between: gemini, openai, claude
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
providers = ['gemini', 'openai', 'claude']

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
providers = ['gemini', 'openai', 'claude']
question = "Explain quantum computing"

for provider in providers:
    model = ModelFactory.create_model(provider)
    response = model.invoke([HumanMessage(question)])
    print(f"{provider}: {response.content}")
```

## 📝 Best Practices

1. **Always use the factory** instead of importing models directly
2. **Handle ImportError** for optional dependencies gracefully
3. **Use configuration files** for provider settings
4. **Implement proper error handling** in model implementations
5. **Follow the interface contract** defined in BaseAIModel
6. **Add comprehensive tests** for new providers

This architecture makes your chatbot future-proof and highly maintainable while providing excellent user experience across different AI providers! 🎯