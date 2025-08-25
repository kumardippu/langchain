import os

from langchain.schema import HumanMessage

try:
    from langchain_ollama import ChatOllama
    OLLAMA_AVAILABLE = True
except ImportError:
    print("❌ Ollama package not installed. Install with: pip install langchain-ollama")
    OLLAMA_AVAILABLE = False

if OLLAMA_AVAILABLE:
    print("🦙 Ollama - Free Local AI Models")
    print("=" * 50)
    print("📋 Available models:")
    print("1. llama3.2 (3B) - Fast and lightweight")
    print("2. llama3.2 (1B) - Very fast, basic tasks")
    print("3. qwen2.5 (7B) - Good for coding")
    print("4. mistral (7B) - General purpose")
    
    print("\n💡 First time? Install Ollama from: https://ollama.ai")
    print("💡 Then run: ollama pull llama3.2")
    
    # Initialize the model
    try:
        model = ChatOllama(
            model="llama3.2",  # 3B model - good balance of speed/quality
            temperature=0.7
        )
        
        print("\n✅ Ollama model loaded successfully!")
        print("=" * 50)
        
        while True:
            question = input("\n💬 Ask me anything (or 'quit' to exit): ")
            
            if question.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
                
            if not question.strip():
                continue

            # Get response from AI
            print("\n🦙 Thinking locally...")
            try:
                response = model.invoke([HumanMessage(content=question)])
                print(f"\n🤖 Llama: {response.content}")
            except Exception as e:
                print(f"❌ Error: {e}")
                print("💡 Make sure Ollama is running and the model is installed")
                print("💡 Try: ollama serve (in another terminal)")
                print("💡 Then: ollama pull llama3.2")
            
            print("\n" + "=" * 50)
            
    except Exception as e:
        print(f"❌ Failed to initialize Ollama: {e}")
        print("💡 Make sure Ollama is installed and running")
else:
    print("Install Ollama: pip install langchain-ollama")
