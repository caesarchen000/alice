#!/usr/bin/env python3
"""
JARVIS AI Assistant - Basic Voice Conversation
Just A Rather Very Intelligent System
"""

import os
import time
import speech_recognition as sr
import pyttsx3
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Jarvis:
    def __init__(self):
        """Initialize JARVIS with speech recognition and synthesis"""
        self.name = "JARVIS"
        self.user_name = "Sir"
        
        # Initialize OpenAI
        self.openai_client = openai.OpenAI(
            api_key=os.getenv('OPENAI_API_KEY', 'your-openai-api-key-here')
        )
        
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Initialize text-to-speech
        self.engine = pyttsx3.init()
        self.setup_voice()
        
        # Adjust for ambient noise
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
    
    def setup_voice(self):
        """Configure JARVIS's voice"""
        voices = self.engine.getProperty('voices')
        
        # Try to find a male voice for JARVIS
        for voice in voices:
            if 'male' in voice.name.lower() or 'david' in voice.name.lower():
                self.engine.setProperty('voice', voice.id)
                break
        
        # Set voice properties
        self.engine.setProperty('rate', 150)    # Speed of speech
        self.engine.setProperty('volume', 0.8)  # Volume level
    
    def speak(self, text):
        """Make JARVIS speak in English"""
        print(f"JARVIS: {text}")
        
        # Process text to force English
        processed_text = self.force_english_text(text)
        
        self.engine.say(processed_text)
        self.engine.runAndWait()
    
    def force_english_text(self, text):
        """Force text to be English-only for speech synthesis"""
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
        
        # Clean up extra spaces and ensure proper formatting
        processed = re.sub(r'\s+', ' ', processed).strip()
        
        return processed
    
    def listen(self):
        """Listen for voice input"""
        try:
            with self.microphone as source:
                print("Listening...")
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            print("Processing speech...")
            text = self.recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text.lower()
            
        except sr.WaitTimeoutError:
            print("No speech detected")
            return None
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return None
    
    def get_ai_response(self, user_input):
        """Get AI response from OpenAI"""
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": f"You are {self.name}, Tony Stark's AI assistant. IMPORTANT: Always respond in English only, regardless of the user's input language. CRITICAL: Always use English numerals (1, 2, 3, 2023) never Chinese numerals (一, 二, 三, 二零二三). Respond in a helpful, slightly formal manner. Keep responses concise and engaging. Address the user as '{self.user_name}' occasionally. Be conversational and knowledgeable about any topic. NEVER respond in Chinese or any other language - English only. ALWAYS use English numbers and dates."
                    },
                    {
                        "role": "user",
                        "content": user_input
                    }
                ],
                max_tokens=150
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"I apologize, {self.user_name}. I'm experiencing some connectivity issues with my advanced processing systems. Error: {str(e)}"
    
    def greet(self):
        """Greet the user"""
        hour = time.localtime().tm_hour
        if hour < 12:
            greeting = f"Good morning, {self.user_name}. How may I assist you today?"
        elif hour < 17:
            greeting = f"Good afternoon, {self.user_name}. How may I assist you today?"
        else:
            greeting = f"Good evening, {self.user_name}. How may I assist you today?"
        
        self.speak(greeting)
    
    def run(self):
        """Main JARVIS loop"""
        self.greet()
        
        while True:
            try:
                # Listen for voice input
                user_input = self.listen()
                
                if user_input:
                    # Check for exit commands
                    if any(word in user_input for word in ['goodbye', 'bye', 'exit', 'quit', 'stop']):
                        self.speak(f"Goodbye, {self.user_name}. JARVIS signing off.")
                        break
                    
                    # Get AI response
                    response = self.get_ai_response(user_input)
                    
                    # Speak the response
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
    print("Initializing JARVIS...")
    print("Make sure you have set your OPENAI_API_KEY in a .env file")
    print("Press Ctrl+C to exit")
    print("-" * 50)
    
    jarvis = Jarvis()
    jarvis.run()

if __name__ == "__main__":
    main() 