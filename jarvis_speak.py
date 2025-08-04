import speech_recognition as sr
import subprocess
import threading
import time
import os
import sys
from datetime import datetime
import pytz
import mss
import base64
from PIL import Image
import io
import openai
from jarvis_mine import Jarvis, pipeline, search, JarvisAgent, fetch_html

class VoiceJarvis:
    def __init__(self):
        # Initialize JARVIS core with same search capabilities as jarvis_mine.py
        self.jarvis = Jarvis()
        
        # Speech recognition setup
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Adjust for ambient noise
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        
        # Voice control state
        self.is_listening = False
        self.wake_word = "hey jarvis"
        self.screenshot_command = "look at my screen"
        
        # Taiwan timezone for context
        self.taiwan_tz = pytz.timezone('Asia/Taipei')
        
        print("🎤 Voice JARVIS initialized!")
        print(f"Wake word: '{self.wake_word}'")
        print(f"Screenshot command: '{self.screenshot_command}'")
        print("Say 'hey jarvis' to activate, then speak your command")
        print("Uses same intelligent search method as jarvis_mine.py")
    
    def speak(self, text):
        """Speak text using macOS say command"""
        try:
            # Clean text for speech
            clean_text = text.replace('"', '').replace("'", "")
            subprocess.run(['say', '-v', 'Samantha', clean_text], check=True)
        except Exception as e:
            print(f"Speech error: {e}")
    
    def take_screenshot(self):
        """Take a screenshot of the entire screen"""
        try:
            with mss.mss() as sct:
                # Capture the entire screen
                monitor = sct.monitors[1]  # Primary monitor
                screenshot = sct.grab(monitor)
                
                # Convert to PIL Image
                img = Image.frombytes('RGB', screenshot.size, screenshot.rgb)
                
                # Save temporarily
                temp_path = "temp_screenshot.png"
                img.save(temp_path)
                
                print("📸 Screenshot captured!")
                return temp_path
        except Exception as e:
            print(f"Screenshot error: {e}")
            return None
    
    def analyze_screenshot(self, image_path):
        """Analyze screenshot using JARVIS vision capabilities with same search method"""
        try:
            # Use JARVIS vision to analyze the image
            with open(image_path, "rb") as image_file:
                image_data = base64.b64encode(image_file.read()).decode('utf-8')
            
            # Create prompt for screenshot analysis
            current_time = datetime.now(self.taiwan_tz).strftime("%Y-%m-%d %H:%M:%S")
            prompt = f"""
            Current time: {current_time}
            Location: Taiwan
            
            I've captured a screenshot of my screen. Please analyze what you see and provide a helpful response.
            Describe what's visible on the screen and offer any relevant assistance or observations.
            """
            
            # Use JARVIS vision response (same method as jarvis_mine.py)
            response = self.jarvis.get_ai_response_with_vision(prompt, image_data)
            return response
            
        except Exception as e:
            print(f"Image analysis error: {e}")
            return "Sorry, I couldn't analyze the screenshot properly."
    
    def listen_for_wake_word(self):
        """Listen continuously for the wake word"""
        print("🎧 Listening for wake word...")
        
        while True:
            try:
                with self.microphone as source:
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=3)
                
                try:
                    # Recognize speech
                    text = self.recognizer.recognize_google(audio).lower()
                    print(f"🎤 Heard: {text}")
                    
                    # Check for wake word
                    if self.wake_word in text:
                        print("🔔 Wake word detected!")
                        self.speak("Yes, I'm listening")
                        self.handle_voice_command()
                        
                except sr.UnknownValueError:
                    # No speech detected, continue listening
                    pass
                except sr.RequestError as e:
                    print(f"Speech recognition error: {e}")
                    
            except sr.WaitTimeoutError:
                # Timeout, continue listening
                pass
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
    
    def handle_voice_command(self):
        """Handle voice commands after wake word"""
        print("🎤 Listening for command...")
        
        try:
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            try:
                command = self.recognizer.recognize_google(audio).lower()
                print(f"🎤 Command: {command}")
                
                # Check for screenshot command
                if self.screenshot_command in command:
                    self.speak("Taking a screenshot and analyzing it")
                    self.handle_screenshot_command(command)
                else:
                    # Handle other voice commands
                    self.handle_general_command(command)
                    
            except sr.UnknownValueError:
                self.speak("I didn't catch that. Please try again.")
            except sr.RequestError as e:
                print(f"Speech recognition error: {e}")
                self.speak("Sorry, there was an error with speech recognition.")
                
        except sr.WaitTimeoutError:
            self.speak("I didn't hear a command. Please try again.")
    
    def handle_screenshot_command(self, command):
        """Handle screenshot and analysis"""
        try:
            # Take screenshot
            screenshot_path = self.take_screenshot()
            if screenshot_path:
                # Analyze the screenshot
                self.speak("Analyzing your screen")
                analysis = self.analyze_screenshot(screenshot_path)
                
                # Speak the analysis
                self.speak(analysis)
                
                # Clean up temp file
                try:
                    os.remove(screenshot_path)
                except:
                    pass
            else:
                self.speak("Sorry, I couldn't take a screenshot")
                
        except Exception as e:
            print(f"Screenshot command error: {e}")
            self.speak("Sorry, there was an error processing your request")
    
    def handle_general_command(self, command):
        """Handle general voice commands using the same search method as jarvis_mine.py"""
        try:
            # Add current context
            current_time = datetime.now(self.taiwan_tz).strftime("%Y-%m-%d %H:%M:%S")
            context_command = f"Current time: {current_time}. Location: Taiwan. User said: {command}"
            
            # Use the same pipeline method as jarvis_mine.py for intelligent search
            # This will automatically decide whether to search web or use AI knowledge
            response = self.jarvis.get_ai_response(context_command)
            
            # Speak the response
            self.speak(response)
            
        except Exception as e:
            print(f"General command error: {e}")
            self.speak("Sorry, I couldn't process that command")
    
    def start_voice_control(self):
        """Start the voice control system"""
        print("🚀 Starting Voice JARVIS...")
        print("Commands:")
        print(f"- Say '{self.wake_word}' to activate")
        print(f"- Say '{self.screenshot_command}' to analyze screen")
        print("- Say any other command for general assistance")
        print("- Uses intelligent search (web + AI knowledge)")
        print("- Press Ctrl+C to exit")
        
        # Start listening in a separate thread
        voice_thread = threading.Thread(target=self.listen_for_wake_word, daemon=True)
        voice_thread.start()
        
        try:
            # Keep main thread alive
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n👋 Shutting down Voice JARVIS...")
            self.speak("Goodbye!")

def main():
    """Main function to run Voice JARVIS"""
    print("🎤 Voice JARVIS - Voice-Controlled AI Assistant")
    print("=" * 50)
    
    # Initialize Voice JARVIS
    voice_jarvis = VoiceJarvis()
    
    # Start voice control
    voice_jarvis.start_voice_control()

if __name__ == "__main__":
    main() 