#!/usr/bin/env python3
"""
JARVIS AI Assistant - macOS Optimized
Uses macOS native text-to-speech with Siri-like quality
"""

import os
import openai
import subprocess
import time
from config import OPENAI_API_KEY

class JarvisMacOS:
    def __init__(self):
        """Initialize JARVIS with macOS native TTS"""
        self.name = "JARVIS"
        self.user_name = "Sir"
        
        # Force English language environment
        os.environ['LANG'] = 'en_US.UTF-8'
        os.environ['LC_ALL'] = 'en_US.UTF-8'
        os.environ['LANGUAGE'] = 'en_US'
        
        # Initialize OpenAI
        self.openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)
        
        # macOS voice settings for Siri-like quality (English only)
        self.voice_settings = {
            'rate': 200,        # Words per minute (Siri-like speed)
            'volume': 100,      # Full volume
            'voice': 'Alex',    # High-quality male voice
            'language': 'en_US' # Force English language
        }
        
        # Available macOS voices (English only, high quality)
        self.available_voices = [
            'Alex',           # High-quality male voice (English)
            'Daniel',         # British male voice (English)
            'Tom',            # Another male option (English)
            'Victoria',       # Female option (English)
            'Samantha',       # Siri-like female voice (English)
            'Fred',           # Male voice (English)
            'Ralph'           # Male voice (English)
        ]
        
        # Setup Siri-like voice
        self.setup_siri_voice()
    
    def setup_siri_voice(self):
        """Setup Siri-like voice using macOS native TTS"""
        try:
            print("🔍 Testing available macOS voices for Siri-like quality...")
            
            # First, get list of available voices to ensure we have English ones
            list_voices_cmd = ['say', '-v', '?']
            voices_result = subprocess.run(list_voices_cmd, capture_output=True, text=True, timeout=10)
            
            if voices_result.returncode == 0:
                available_voices = voices_result.stdout
                print("📋 Available voices on your system:")
                for voice in self.available_voices:
                    if voice in available_voices:
                        print(f"   ✅ {voice} - Available")
                    else:
                        print(f"   ❌ {voice} - Not available")
            
            # Test and find the best available voice
            for voice_name in self.available_voices:
                test_command = [
                    'say', 
                    '-v', voice_name,
                    '-r', str(self.voice_settings['rate']),
                    'JARVIS online and ready'
                ]
                
                # Set environment to force English
                env = os.environ.copy()
                env['LANG'] = 'en_US.UTF-8'
                env['LC_ALL'] = 'en_US.UTF-8'
                env['LANGUAGE'] = 'en_US'
                
                result = subprocess.run(test_command, capture_output=True, timeout=5, env=env)
                
                if result.returncode == 0:
                    self.voice_settings['voice'] = voice_name
                    print(f"✅ Using Siri-like voice: {voice_name}")
                    self.tts_available = True
                    break
            else:
                print("✅ Using default macOS voice")
                self.tts_available = True
                
        except Exception as e:
            print(f"❌ Voice setup error: {e}")
            self.tts_available = False
    
    def speak(self, text):
        """Make JARVIS speak with Siri-like voice quality"""
        print(f"🤖 JARVIS: {text}")
        
        if self.tts_available:
            try:

                
                # Try multiple approaches to ensure English speech
                success = False
                
                # Approach 1: Use Alex voice (which is available)
                try:
                    say_command = [
                        'say',
                        '-v', 'Alex',
                        '-r', '200',
                        text
                    ]
                    
                    env = os.environ.copy()
                    env['LANG'] = 'en_US.UTF-8'
                    env['LC_ALL'] = 'en_US.UTF-8'
                    env['LANGUAGE'] = 'en_US'
                    env['LC_MESSAGES'] = 'en_US.UTF-8'
                    env['LC_COLLATE'] = 'en_US.UTF-8'
                    env['LC_CTYPE'] = 'en_US.UTF-8'
                    env['LC_MONETARY'] = 'en_US.UTF-8'
                    env['LC_NUMERIC'] = 'en_US.UTF-8'
                    env['LC_TIME'] = 'en_US.UTF-8'
                    
                    result = subprocess.run(say_command, capture_output=True, timeout=15, env=env)
                    if result.returncode == 0:
                        success = True
                        print("✅ Speech successful with Alex voice")
                except Exception as e:
                    print(f"Alex voice failed: {e}")
                
                # Approach 2: Use Fred voice (which is available)
                if not success:
                    try:
                        say_command = [
                            'say',
                            '-v', 'Fred',
                            '-r', '200',
                            text
                        ]
                        
                        result = subprocess.run(say_command, capture_output=True, timeout=15, env=env)
                        if result.returncode == 0:
                            success = True
                            print("✅ Speech successful with Fred voice")
                    except Exception as e:
                        print(f"Fred voice failed: {e}")
                
                # Approach 3: Use default voice with English environment
                if not success:
                    try:
                        say_command = [
                            'say',
                            '-r', '200',
                            text
                        ]
                        
                        result = subprocess.run(say_command, capture_output=True, timeout=15, env=env)
                        if result.returncode == 0:
                            success = True
                            print("✅ Speech successful with default voice")
                    except Exception as e:
                        print(f"Default voice failed: {e}")
                
                if not success:
                    print("❌ All speech methods failed")
                
            except Exception as e:
                print(f"Speech error: {e}")
        else:
            print("Voice not available - text only mode")      
  
    def listen(self):
        """Listen for voice input using macOS Speech Recognition"""
        print("🎤 Listening... (Speak now)")
        
        try:
            # Use macOS Speech Recognition
            # This requires macOS Speech Recognition to be enabled
            print("⚠️  Note: You need to enable macOS Speech Recognition")
            print("   Go to: System Preferences > Accessibility > Speech Recognition")
            print("   Or use text input for now")
            
            # For now, use text input as fallback
            return input("👤 You (type): ").strip()
            
        except Exception as e:
            print(f"Listening error: {e}")
            return input("👤 You (type): ").strip()
    
    def get_ai_response(self, user_input):
        """Get AI response with Siri-like personality"""
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": f"""You are {self.name}, Tony Stark's AI assistant with a personality similar to Siri. 
                        CRITICAL RULES:
                        1. ALWAYS respond in English only - NEVER use Chinese or any other language
                        2. ALWAYS use English numerals (1, 2, 3, 2023) - NEVER use Chinese numerals (一, 二, 三, 二零二三)
                        3. ALWAYS use English dates and times
                        4. NEVER include any Chinese characters in your response
                        5. If the user asks in Chinese, still respond in English
                        
                        Respond in a helpful, slightly formal but friendly manner. 
                        Keep responses concise (1-2 sentences) and engaging.
                        Address the user as '{self.user_name}' occasionally.
                        Be conversational, knowledgeable, and slightly witty like Siri.
                        Use natural speech patterns with occasional pauses and emphasis.
                        Show personality and intelligence like Siri but with JARVIS's helpfulness.
                        ENGLISH ONLY - NO EXCEPTIONS."""
                    },
                    {
                        "role": "user",
                        "content": user_input
                    }
                ],
                max_tokens=120
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"I apologize, {self.user_name}. I'm experiencing some connectivity issues with my advanced processing systems."
    
    def greet(self):
        """Greet the user with Siri-like style"""
        hour = time.localtime().tm_hour
        
        if hour < 12:
            greeting = f"Good morning, {self.user_name}. JARVIS at your service."
        elif hour < 17:
            greeting = f"Good afternoon, {self.user_name}. How may I assist you today?"
        else:
            greeting = f"Good evening, {self.user_name}. JARVIS ready for your commands."
        
        self.speak(greeting)
    
    def run(self):
        """Main JARVIS loop with Siri-like experience"""
        print("🚀 Initializing JARVIS with macOS Native TTS...")
        print("🎤 Voice recognition: macOS Speech Recognition")
        print("🔊 Voice output: macOS Native TTS (Siri-like)")
        print("💬 You can also type your messages")
        print("❌ Type 'quit', 'exit', or 'goodbye' to end")
        print("-" * 50)
        
        self.greet()
        
        while True:
            try:
                # Listen for voice input
                user_input = self.listen()
                
                if user_input:
                    # Check for exit commands
                    if any(word in user_input.lower() for word in ['goodbye', 'bye', 'exit', 'quit', 'stop']):
                        self.speak(f"Goodbye, {self.user_name}. JARVIS signing off.")
                        break
                    
                    # Get AI response
                    response = self.get_ai_response(user_input)
                    
                    # Speak the response with Siri-like voice
                    self.speak(response)
                
            except KeyboardInterrupt:
                print("\nShutting down JARVIS...")
                self.speak(f"Goodbye, {self.user_name}. JARVIS signing off.")
                break
            except Exception as e:
                print(f"Error: {e}")
                self.speak(f"I apologize, {self.user_name}. There seems to be an error.")

def main():
    """Main function"""
    print("🤖 JARVIS AI Assistant - macOS Optimized")
    print("Make sure you have set your OPENAI_API_KEY in config.py")
    print("=" * 50)
    
    jarvis = JarvisMacOS()
    jarvis.run()

if __name__ == "__main__":
    main() 