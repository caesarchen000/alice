#!/usr/bin/env python3
"""
JARVIS AI Assistant - Windows Speech Recognition
Uses Windows built-in speech recognition and Siri-like text-to-speech
"""

import os
import openai
import subprocess
import time
from config import OPENAI_API_KEY

class JarvisWindows:
    def __init__(self):
        """Initialize JARVIS with OpenAI and Siri-like voice"""
        self.name = "JARVIS"
        self.user_name = "Sir"
        
        # Initialize OpenAI
        self.openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)
        
        # Siri-like voice settings
        self.voice_settings = {
            'rate': -2,        # Slightly slower for clarity like Siri
            'volume': 100,     # Full volume
            'pitch': 0,        # Natural pitch
            'voice_name': 'Microsoft David Desktop'  # Professional male voice
        }
        
        # Available voices (Windows TTS voices)
        self.available_voices = [
            'Microsoft David Desktop',
            'Microsoft Zira Desktop', 
            'Microsoft Mark Desktop',
            'Microsoft James Desktop'
        ]
        
        # Setup Siri-like voice
        self.setup_siri_voice()
    
    def setup_siri_voice(self):
        """Setup Siri-like voice with multiple options"""
        try:
            print("🔍 Testing available voices for Siri-like quality...")
            
            # Test and find the best available voice
            for voice_name in self.available_voices:
                test_command = f'''
                Add-Type -AssemblyName System.Speech
                $speak = New-Object System.Speech.Synthesis.SpeechSynthesizer
                $speak.Rate = {self.voice_settings['rate']}
                $speak.Volume = {self.voice_settings['volume']}
                try {{
                    $speak.SelectVoice("{voice_name}")
                    $speak.Speak("JARVIS online and ready")
                    Write-Host "Voice {voice_name} works"
                }} catch {{
                    Write-Host "Voice {voice_name} not available"
                }}
                '''
                
                result = subprocess.run([
                    'powershell.exe', 
                    '-Command', 
                    test_command
                ], capture_output=True, timeout=10)
                
                if "Voice " + voice_name + " works" in result.stdout.decode():
                    self.voice_settings['voice_name'] = voice_name
                    print(f"✅ Using Siri-like voice: {voice_name}")
                    self.tts_available = True
                    break
            else:
                print("✅ Using default voice with Siri-like settings")
                self.tts_available = True
                
        except Exception as e:
            print(f"❌ Voice setup error: {e}")
            self.tts_available = False
    
    def speak(self, text):
        """Make JARVIS speak with Siri-like voice quality"""
        print(f"🤖 JARVIS: {text}")
        
        if self.tts_available:
            try:
                # Process text for natural Siri-like speech
                processed_text = self.process_text_for_siri_speech(text)
                
                ps_command = f'''
                Add-Type -AssemblyName System.Speech
                $speak = New-Object System.Speech.Synthesis.SpeechSynthesizer
                $speak.Rate = {self.voice_settings['rate']}
                $speak.Volume = {self.voice_settings['volume']}
                try {{
                    $speak.SelectVoice("{self.voice_settings['voice_name']}")
                }} catch {{
                    Write-Host "Using default voice"
                }}
                $speak.Speak("{processed_text}")
                '''
                
                subprocess.run([
                    'powershell.exe', 
                    '-Command', 
                    ps_command
                ], capture_output=True, timeout=15)
                
            except Exception as e:
                print(f"Speech error: {e}")
        else:
            print("Voice not available - text only mode")
    
    def process_text_for_siri_speech(self, text):
        """Process text to sound more natural like Siri and force English"""
        import re
        
        # Remove ALL Chinese characters first
        processed = re.sub(r'[\u4e00-\u9fff]', '', text)
        
        # Convert ALL numbers to spelled-out English words
        number_to_words = {
            '0': 'zero', '1': 'one', '2': 'two', '3': 'three', '4': 'four', '5': 'five',
            '6': 'six', '7': 'seven', '8': 'eight', '9': 'nine', '10': 'ten',
            '11': 'eleven', '12': 'twelve', '13': 'thirteen', '14': 'fourteen', '15': 'fifteen',
            '16': 'sixteen', '17': 'seventeen', '18': 'eighteen', '19': 'nineteen',
            '20': 'twenty', '21': 'twenty one', '22': 'twenty two', '23': 'twenty three',
            '24': 'twenty four', '25': 'twenty five', '26': 'twenty six', '27': 'twenty seven',
            '28': 'twenty eight', '29': 'twenty nine', '30': 'thirty', '31': 'thirty one',
            '2023': 'twenty twenty three', '2024': 'twenty twenty four', '2025': 'twenty twenty five',
            '2026': 'twenty twenty six', '2027': 'twenty twenty seven'
        }
        
        # Replace numbers with spelled-out words (handle word boundaries)
        for number, word in number_to_words.items():
            # Replace standalone numbers
            processed = re.sub(rf'\b{number}\b', word, processed)
            # Replace numbers at end of sentences
            processed = re.sub(rf'{number}([.!?])', f'{word}\\1', processed)
            # Replace numbers with commas
            processed = re.sub(rf'{number},', f'{word},', processed)
        
        # Add natural pauses and emphasis like Siri
        if any(word in processed.lower() for word in ['hello', 'hi', 'good morning', 'good afternoon', 'good evening']):
            processed = processed.replace('.', '...')
        
        # Add emphasis to important words
        emphasis_words = ['JARVIS', 'Sir', 'Tony', 'Stark', 'Iron Man', 'Stark Industries']
        for word in emphasis_words:
            if word.lower() in processed.lower():
                processed = processed.replace(word, f"<emphasis>{word}</emphasis>")
        
        # Add natural pauses before responses
        if processed.startswith('I') or processed.startswith('Well') or processed.startswith('Let me'):
            processed = f"<break time='300ms'/> {processed}"
        
        # Add pauses for dramatic effect
        if '?' in processed:
            processed = processed.replace('?', '? <break time="200ms"/>')
        
        # Add pauses for natural flow
        if ',' in processed:
            processed = processed.replace(',', ', <break time="100ms"/>')
        
        # Escape quotes for PowerShell
        processed = processed.replace('"', '\\"')
        
        return processed
    
    def listen(self):
        """Listen for voice input using Windows Speech Recognition"""
        print("🎤 Listening... (Speak now)")
        
        try:
            # Use Windows Speech Recognition
            # This requires Windows Speech Recognition to be enabled
            print("⚠️  Note: You need to enable Windows Speech Recognition")
            print("   Go to: Settings > Ease of Access > Speech Recognition")
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
                        IMPORTANT: Always respond in English only, regardless of the user's input language.
                        CRITICAL: Always use English numerals (1, 2, 3, 2023) never Chinese numerals (一, 二, 三, 二零二三).
                        Respond in a helpful, slightly formal but friendly manner. 
                        Keep responses concise (1-2 sentences) and engaging.
                        Address the user as '{self.user_name}' occasionally.
                        Be conversational, knowledgeable, and slightly witty like Siri.
                        Use natural speech patterns with occasional pauses and emphasis.
                        Show personality and intelligence like Siri but with JARVIS's helpfulness.
                        NEVER respond in Chinese or any other language - English only.
                        ALWAYS use English numbers and dates."""
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
        print("🚀 Initializing JARVIS with Siri-like Voice...")
        print("🎤 Voice recognition: Windows Speech Recognition")
        print("🔊 Voice output: Siri-like Windows TTS")
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
    print("🤖 JARVIS AI Assistant - Siri-like Voice")
    print("Make sure you have set your OPENAI_API_KEY in config.py")
    print("=" * 50)
    
    jarvis = JarvisWindows()
    jarvis.run()

if __name__ == "__main__":
    main() 