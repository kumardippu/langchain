import getpass
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Check if API key exists, if not prompt for it
if not os.environ.get("GOOGLE_API_KEY"):
    print("GOOGLE_API_KEY not found in .env file or environment variables")
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter API key for Google Gemini: ")

print(f"API Key loaded: {os.environ.get('GOOGLE_API_KEY')[:10]}..." if os.environ.get("GOOGLE_API_KEY") else "No API key found")

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage

# Initialize the model
model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

# Interactive chat
print("\n" + "="*50)
print("🤖 Gemini AI Chat - Ready!")
print("="*50)
question = input("\n💬 Ask me anything: ")

# Get response from AI
print("\n🤔 Thinking...")
response = model.invoke([HumanMessage(content=question)])
print(f"\n🤖 Gemini: {response.content}")
print("\n" + "="*50)