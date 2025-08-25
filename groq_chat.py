import getpass
import os

from dotenv import load_dotenv
from langchain.schema import HumanMessage

# Load environment variables from .env file
load_dotenv()

try:
    from langchain_groq import ChatGroq
    GROQ_AVAILABLE = True
except ImportError:
    print("❌ Groq package not installed. Install with: pip install langchain-groq")
    GROQ_AVAILABLE = False

if GROQ_AVAILABLE:
    # Check if API key exists, if not prompt for it
    if not os.environ.get("GROQ_API_KEY"):
        print("🔑 Get your free Groq API key from: https://console.groq.com/keys")
        print("GROQ_API_KEY not found in .env file or environment variables")
        os.environ["GROQ_API_KEY"] = getpass.getpass("Enter API key for Groq: ")

    print(
        f"✅ API Key loaded: {os.environ.get('GROQ_API_KEY')[:10]}..."
        if os.environ.get("GROQ_API_KEY")
        else "❌ No API key found"
    )

    # Initialize the model (Groq has several free models)
    model = ChatGroq(
        model="mixtral-8x7b-32768",  # Fast and capable free model
        temperature=0.7
    )

    # Interactive chat
    print("\n" + "=" * 50)
    print("🚀 Groq AI Chat - Super Fast & Free!")
    print("Model: Mixtral-8x7B")
    print("=" * 50)
    
    while True:
        question = input("\n💬 Ask me anything (or 'quit' to exit): ")
        
        if question.lower() in ['quit', 'exit', 'q']:
            print("👋 Goodbye!")
            break
            
        if not question.strip():
            continue

        # Get response from AI
        print("\n🚀 Thinking at lightning speed...")
        try:
            response = model.invoke([HumanMessage(content=question)])
            print(f"\n🤖 Groq: {response.content}")
        except Exception as e:
            print(f"❌ Error: {e}")
            print("💡 Try using your Gemini model in g.py instead")
        
        print("\n" + "=" * 50)
