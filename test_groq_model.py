#!/usr/bin/env python3
"""
Test script for the new Groq model implementation
Author: Dippu Kumar
"""

from langchain.schema import HumanMessage

from models.model_factory import ModelFactory, create_groq_model


def test_groq_via_factory():
    """Test Groq model via ModelFactory"""
    print("🚀 Testing Groq Model via Factory")
    print("=" * 50)
    
    try:
        # Create Groq model using factory
        groq_model = ModelFactory.create_model("groq")
        
        # Test message
        message = [HumanMessage(content="Hello! Tell me a fun fact about AI.")]
        
        print("🤖 Sending message to Groq...")
        response = groq_model.invoke(message)
        print(f"✅ Groq Response: {response.content}")
        
        # Show model info
        print(f"\n📊 Provider: {groq_model.provider_name}")
        print(f"🆓 Free Tier: {groq_model.is_free_tier_available}")
        
        # Show available models
        print("\n📋 Available Groq Models:")
        for model in groq_model.get_available_models():
            print(f"  • {model['name']}: {model['description']}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Make sure you have:")
        print("   1. Installed: pip install langchain-groq")
        print("   2. Set GROQ_API_KEY in .env or environment")


def test_groq_convenience_function():
    """Test Groq model via convenience function"""
    print("\n🚀 Testing Groq Model via Convenience Function")
    print("=" * 50)
    
    try:
        # Create Groq model using convenience function
        groq_model = create_groq_model(
            model_name="llama3-70b-8192",  # Use the more powerful model
            temperature=0.9
        )
        
        # Test message
        message = [HumanMessage(content="Write a haiku about programming.")]
        
        print("🤖 Sending creative request to Llama 3 70B...")
        response = groq_model.invoke(message)
        print(f"✅ Creative Response:\n{response.content}")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def show_all_providers():
    """Show all available providers"""
    print("\n📊 All Available AI Providers")
    print("=" * 50)
    
    providers = ModelFactory.get_available_providers()
    for provider in providers:
        available = "✅" if ModelFactory.is_provider_available(provider) else "❌"
        print(f"{available} {provider.title()}")


if __name__ == "__main__":
    print("🧪 Groq Model Integration Test")
    print("=" * 50)
    
    # Show all providers first
    show_all_providers()
    
    # Test Groq model
    test_groq_via_factory()
    test_groq_convenience_function()
    
    print("\n✨ Test completed!")
    print("🔥 Groq is now integrated into your model factory!")
