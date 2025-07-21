#!/usr/bin/env python3
"""
Test script to verify OpenAI API key
"""

import openai
from config import OPENAI_API_KEY

def test_api_key():
    """Test if the OpenAI API key is valid"""
    print("🔍 Testing OpenAI API key...")
    print(f"API Key (first 10 chars): {OPENAI_API_KEY[:10]}...")
    
    if not OPENAI_API_KEY or OPENAI_API_KEY == "your-openai-api-key-here":
        print("❌ Error: API key is missing or placeholder")
        return False
    
    if not OPENAI_API_KEY.startswith("sk-"):
        print("❌ Error: API key format is invalid (should start with 'sk-')")
        return False
    
    try:
        # Initialize OpenAI client
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        
        # Test with a simple request
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Hello"}
            ],
            max_tokens=10
        )
        
        print("✅ API key is valid and working!")
        print(f"Response: {response.choices[0].message.content}")
        return True
        
    except Exception as e:
        print(f"❌ API key test failed: {e}")
        return False

if __name__ == "__main__":
    test_api_key() 