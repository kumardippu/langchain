# LangChain Google Gemini Chatbot

A simple interactive chatbot using LangChain and Google's Gemini AI model.

## 🚀 Features

- Interactive chat with Google Gemini AI
- Secure API key management using `.env` files
- Colorful and user-friendly interface
- Automatic fallback to manual API key entry

## 📋 Prerequisites

- Python 3.9 or higher
- Google AI Studio account
- Terminal/Command Prompt access

## 🛠️ Installation

### Step 1: Clone or Download

```bash
# Create project directory
mkdir langchain-gemini-chat
cd langchain-gemini-chat

# Download the g.py file (or copy it manually)
```

### Step 2: Set Up Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
# Install required packages
pip install langchain langchain-google-genai python-dotenv
```

## 🔑 Getting Google API Key

### Method 1: Get API Key from Google AI Studio

1. Visit [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Click "Get API key" or "Create API key"
4. Copy the generated API key (starts with `AIzaSy...`)

### Method 2: Set Up Environment Variables

#### Option A: Using .env file (Recommended)

1. Create a `.env` file in the project directory:

```bash
touch .env
```

2. Add your API key to the `.env` file:

```env
# Google API Configuration
GOOGLE_API_KEY=AIzaSyC-your_actual_api_key_here
```

3. **Important**: Add `.env` to your `.gitignore` to keep your API key secure:

```bash
echo ".env" >> .gitignore
```

#### Option B: System Environment Variables

```bash
# Add to your shell profile (.bashrc, .zshrc, etc.)
export GOOGLE_API_KEY="AIzaSyC-your_actual_api_key_here"

# Reload your shell or run:
source ~/.zshrc  # or ~/.bashrc
```

## 🎯 Usage

### Run the Chatbot

```bash
python g.py
```

### Expected Output

```
API Key loaded: AIzaSyDpIh...

==================================================
🤖 Gemini AI Chat - Ready!
==================================================

💬 Ask me anything: What is the capital of France?

🤔 Thinking...

🤖 Gemini: The capital of France is Paris.

==================================================
```

### If No API Key is Found

If the script can't find your API key in the `.env` file or environment variables, it will prompt you:

```
GOOGLE_API_KEY not found in .env file or environment variables
Enter API key for Google Gemini: [enter your key here]
```

## 📁 Project Structure

```
langchain-gemini-chat/
├── g.py                 # Main chatbot script
├── .env                 # API key (create this)
├── .gitignore          # Git ignore file
├── README.md           # This file
└── .venv/              # Virtual environment (optional)
```

## 🔧 Troubleshooting

### Common Issues

#### 1. ModuleNotFoundError

```bash
ModuleNotFoundError: No module named 'langchain'
```

**Solution**: Install dependencies
```bash
pip install langchain langchain-google-genai python-dotenv
```

#### 2. ModuleNotFoundError: dotenv

```bash
ModuleNotFoundError: No module named 'dotenv'
```

**Solution**: Install python-dotenv
```bash
pip install python-dotenv
```

#### 3. API Key Issues

- **Error**: Invalid API key
- **Solution**: 
  1. Verify your API key is correct
  2. Check Google AI Studio for API key status
  3. Ensure no extra spaces in your `.env` file

#### 4. Python Version Issues

```bash
ERROR: Could not find a version that satisfies the requirement langchain-google-genai
```

**Solution**: Use Python 3.9 or higher
```bash
python3 --version  # Should be 3.9+
python3 -m pip install langchain-google-genai
```

#### 5. Virtual Environment Issues

If packages are installed globally but not in your virtual environment:

```bash
# Deactivate and reactivate virtual environment
deactivate
source .venv/bin/activate

# Reinstall packages
pip install langchain langchain-google-genai python-dotenv
```

### Environment Verification

Check if everything is set up correctly:

```bash
# Check Python version
python3 --version

# Check if packages are installed
python3 -c "import langchain; print('LangChain:', langchain.__version__)"
python3 -c "import langchain_google_genai; print('Google GenAI: OK')"
python3 -c "from dotenv import load_dotenv; print('python-dotenv: OK')"

# Check if API key is loaded
python3 -c "from dotenv import load_dotenv; import os; load_dotenv(); print('API Key found:', bool(os.environ.get('GOOGLE_API_KEY')))"
```

## 🔒 Security Best Practices

1. **Never commit API keys to version control**
2. **Use `.env` files for local development**
3. **Use environment variables for production**
4. **Add `.env` to `.gitignore`**
5. **Rotate API keys regularly**

## 🚀 Next Steps

### Extend the Chatbot

1. **Add conversation history**:
```python
messages = []
while True:
    question = input("\n💬 Ask me anything (or 'quit' to exit): ")
    if question.lower() == 'quit':
        break
    messages.append(HumanMessage(content=question))
    response = model.invoke(messages)
    messages.append(response)
    print(f"\n🤖 Gemini: {response.content}")
```

2. **Add streaming responses**:
```python
for chunk in model.stream([HumanMessage(content=question)]):
    print(chunk.content, end="", flush=True)
```

3. **Add different AI models**:
```python
# Try different Gemini models
model = ChatGoogleGenerativeAI(model="gemini-1.5-pro")  # More powerful
model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")  # Faster
```

## 📚 Additional Resources

- [LangChain Documentation](https://python.langchain.com/)
- [Google AI Studio](https://aistudio.google.com/)
- [Google Gemini API Documentation](https://ai.google.dev/)
- [Python-dotenv Documentation](https://python-dotenv.readthedocs.io/)

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

---

**Happy Chatting! 🤖✨**

## Reference
https://python.langchain.com/docs/tutorials/llm_chain/
