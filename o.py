import getpass
import os

from dotenv import load_dotenv
from langchain.schema import HumanMessage
from langchain_openai import ChatOpenAI

# Load environment variables from .env file
load_dotenv()

# Check if API key exists, if not prompt for it
if not os.environ.get("OPENAI_API_KEY"):
    print("OPENAI_API_KEY not found in .env file or environment variables")
    os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter API key for OpenAI: ")

print(
    f"API Key loaded: {os.environ.get('OPENAI_API_KEY')[:10]}..."
    if os.environ.get("OPENAI_API_KEY")
    else "No API key found"
)


# Initialize the model
model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

# Interactive chat
print("\n" + "=" * 50)
print("🤖 OpenAI GPT Chat - Ready!")
print("=" * 50)
question = input("\n💬 Ask me anything: ")

# Get response from AI
print("\n🤔 Thinking...")
response = model.invoke([HumanMessage(content=question)])
print(f"\n🤖 OpenAI GPT: {response.content}")
print("\n" + "=" * 50)
