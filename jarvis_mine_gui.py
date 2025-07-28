#!/usr/bin/env python3
"""
JARVIS Mine GUI - Modern Messenger-like Interface
Provides a beautiful graphical interface for JARVIS with text and voice input
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import queue
import speech_recognition as sr
import pyaudio
import time
import os
import sys
from datetime import datetime

# Import JARVIS functionality from jarvis_mine.py
from jarvis_mine import Jarvis

class ModernJarvisMineGUI:
    def __init__(self):
        """Initialize the modern JARVIS GUI"""
        self.root = tk.Tk()
        self.root.title("JARVIS AI Assistant")
        self.root.geometry("1000x800")
        self.root.configure(bg='#0d1117')  # GitHub dark theme
        
        # Make sure window appears on top
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.after_idle(self.root.attributes, '-topmost', False)
        
        # Initialize JARVIS
        self.jarvis = Jarvis()
        
        # Speech recognition setup
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.is_listening = False
        self.audio_queue = queue.Queue()
        
        # Separate queues for different message types
        self.user_message_queue = queue.Queue()  # For user messages (text, voice)
        self.response_queue = queue.Queue()      # For AI responses
        
        # Animation variables
        self.typing_animation_id = None
        self.is_typing = False
        
        # Setup GUI
        self.setup_gui()
        
        # Start message processing thread
        self.processing_thread = threading.Thread(target=self.process_messages, daemon=True)
        self.processing_thread.start()
        
        # Process any queued messages
        self.root.after(100, self.process_message_queue)
        
        # Focus on text input
        self.text_input.focus()
    
    def setup_gui(self):
        """Setup the ultra-modern GUI components"""
        # Configure grid weights for responsive layout
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Main container with gradient effect
        main_container = tk.Frame(self.root, bg='#0d1117')
        main_container.grid(row=0, column=0, sticky='nsew', padx=20, pady=20)
        main_container.grid_rowconfigure(1, weight=1)
        main_container.grid_columnconfigure(0, weight=1)
        
        # Header with modern design
        self.setup_modern_header(main_container)
        
        # Conversation area with beautiful styling
        self.setup_conversation_area(main_container)
        
        # Input area with modern design
        self.setup_input_area(main_container)
        
        # Status bar with animations
        self.setup_status_bar(main_container)
        
        # Welcome message
        self.add_message("JARVIS", "Good evening, Sir. JARVIS ready for your commands.", "assistant")
    
    def setup_modern_header(self, parent):
        """Setup ultra-modern header with gradient and effects"""
        # Header container with rounded corners effect
        header_frame = tk.Frame(parent, bg='#161b22', height=100, relief='flat', bd=0)
        header_frame.grid(row=0, column=0, sticky='ew', pady=(0, 20))
        header_frame.grid_propagate(False)
        
        # Title with gradient-like effect
        title_frame = tk.Frame(header_frame, bg='#161b22')
        title_frame.pack(expand=True, fill='both', padx=20, pady=10)
        
        # JARVIS title with modern styling
        title_label = tk.Label(
            title_frame,
            text="JARVIS AI Assistant",
            font=('Helvetica', 24, 'bold'),
            fg='#58a6ff',
            bg='#161b22'
        )
        title_label.pack(side='left')
        
        # Status indicator
        self.status_label = tk.Label(
            title_frame,
            text="● Online",
            font=('Helvetica', 12),
            fg='#3fb950',
            bg='#161b22'
        )
        self.status_label.pack(side='right')
    
    def setup_conversation_area(self, parent):
        """Setup conversation display area with modern styling"""
        # Conversation container
        conversation_frame = tk.Frame(parent, bg='#0d1117')
        conversation_frame.grid(row=1, column=0, sticky='nsew', pady=(0, 20))
        conversation_frame.grid_rowconfigure(0, weight=1)
        conversation_frame.grid_columnconfigure(0, weight=1)
        
        # Conversation text widget with modern styling
        self.conversation_text = scrolledtext.ScrolledText(
            conversation_frame,
            wrap=tk.WORD,
            bg='#161b22',
            fg='#c9d1d9',
            insertbackground='#58a6ff',
            selectbackground='#21262d',
            font=('Helvetica', 11),
            relief='flat',
            bd=0,
            padx=20,
            pady=20
        )
        self.conversation_text.grid(row=0, column=0, sticky='nsew')
        
        # Make conversation area read-only but allow content display
        self.conversation_text.bind("<Key>", lambda e: "break")
        
        # Scrollbar styling
        scrollbar = self.conversation_text.vbar
        scrollbar.configure(
            troughcolor='#0d1117',
            background='#30363d',
            activebackground='#58a6ff'
        )
    
    def setup_input_area(self, parent):
        """Setup input area with modern design"""
        # Input container
        input_frame = tk.Frame(parent, bg='#0d1117')
        input_frame.grid(row=2, column=0, sticky='ew', pady=(0, 20))
        input_frame.grid_columnconfigure(0, weight=1)
        
        # Input field with modern styling (bigger)
        self.text_input = tk.Text(
            input_frame,
            font=('Helvetica', 12),
            bg='#161b22',
            fg='#c9d1d9',
            insertbackground='#58a6ff',
            relief='flat',
            bd=0,
            highlightthickness=1,
            highlightbackground='#30363d',
            highlightcolor='#58a6ff',
            height=3,  # Make it 3 lines tall
            wrap=tk.WORD
        )
        self.text_input.grid(row=0, column=0, sticky='ew', padx=(0, 10))
        self.text_input.bind('<Return>', self.send_message)
        self.text_input.bind('<KeyRelease>', self.on_input_change)
        self.text_input.bind('<Shift-Return>', lambda e: None)  # Allow Shift+Enter for new line
        
        # Send button with modern styling
        self.send_button = tk.Button(
            input_frame,
            text="Send",
            font=('Helvetica', 11, 'bold'),
            bg='#238636',
            fg='white',
            relief='flat',
            bd=0,
            padx=20,
            pady=8,
            cursor='hand2',
            command=self.send_message
        )
        self.send_button.grid(row=0, column=1, padx=(0, 10))
        
        # Voice button with modern styling
        self.voice_button = tk.Button(
            input_frame,
            text="🎤",
            font=('Helvetica', 16),
            bg='#da3633',
            fg='white',
            relief='flat',
            bd=0,
            padx=15,
            pady=8,
            cursor='hand2',
            command=self.toggle_voice_input
        )
        self.voice_button.grid(row=0, column=2)
        
        # Bind hover effects
        self.bind_hover_effects()
    
    def setup_status_bar(self, parent):
        """Setup status bar with animations"""
        # Status bar container
        status_frame = tk.Frame(parent, bg='#0d1117', height=30)
        status_frame.grid(row=3, column=0, sticky='ew')
        status_frame.grid_propagate(False)
        
        # Status text
        self.status_text = tk.Label(
            status_frame,
            text="Ready",
            font=('Helvetica', 10),
            fg='#8b949e',
            bg='#0d1117'
        )
        self.status_text.pack(side='left')
        
        # Typing indicator
        self.typing_label = tk.Label(
            status_frame,
            text="",
            font=('Helvetica', 10),
            fg='#58a6ff',
            bg='#0d1117'
        )
        self.typing_label.pack(side='right')
    
    def bind_hover_effects(self):
        """Bind hover effects to buttons"""
        def on_enter(event):
            if event.widget == self.send_button:
                event.widget.configure(bg='#2ea043')
            elif event.widget == self.voice_button:
                event.widget.configure(bg='#f85149')
        
        def on_leave(event):
            if event.widget == self.send_button:
                event.widget.configure(bg='#238636')
            elif event.widget == self.voice_button:
                event.widget.configure(bg='#da3633')
        
        self.send_button.bind('<Enter>', on_enter)
        self.send_button.bind('<Leave>', on_leave)
        self.voice_button.bind('<Enter>', on_enter)
        self.voice_button.bind('<Leave>', on_leave)
    
    def on_input_change(self, event=None):
        """Handle input field changes"""
        if self.text_input.get("1.0", tk.END).strip():
            self.send_button.configure(state='normal')
        else:
            self.send_button.configure(state='disabled')
    
    def show_typing_indicator(self):
        """Show typing indicator animation"""
        if not self.is_typing:
            self.is_typing = True
            self.typing_label.configure(text="JARVIS is typing")
            
            def animate_typing():
                if self.is_typing:
                    current_text = self.typing_label.cget("text")
                    if current_text.endswith("..."):
                        self.typing_label.configure(text="JARVIS is typing")
                    else:
                        self.typing_label.configure(text=current_text + ".")
                    self.typing_animation_id = self.root.after(500, animate_typing)
            
            animate_typing()
    
    def hide_typing_indicator(self):
        """Hide typing indicator"""
        self.is_typing = False
        if self.typing_animation_id:
            self.root.after_cancel(self.typing_animation_id)
            self.typing_animation_id = None
        self.typing_label.configure(text="")
    
    def add_message(self, sender, message, message_type):
        """Add a message to the conversation area with modern styling"""
        timestamp = datetime.now().strftime("%H:%M")
        
        # Configure tags for different message types
        self.conversation_text.tag_configure("user", foreground="#58a6ff", font=('Helvetica', 14, 'bold'))
        self.conversation_text.tag_configure("assistant", foreground="#c9d1d9", font=('Helvetica', 11))
        self.conversation_text.tag_configure("timestamp", foreground="#8b949e", font=('Helvetica', 9))
        self.conversation_text.tag_configure("separator", foreground="#30363d", font=('Helvetica', 9))
        
        # Insert message with proper formatting
        self.conversation_text.insert(tk.END, f"{timestamp} ", "timestamp")
        self.conversation_text.insert(tk.END, f"{sender}: ", message_type)
        self.conversation_text.insert(tk.END, f"{message}\n\n")
        
        # Auto-scroll to bottom
        self.conversation_text.see(tk.END)
    
    def send_message(self, event=None):
        """Send a message and get AI response"""
        # Get text from the Text widget
        message = self.text_input.get("1.0", tk.END).strip()
        if not message:
            return
        
        # Clear input field
        self.text_input.delete("1.0", tk.END)
        
        # Add user message to conversation
        self.add_message("You", message, "user")
        
        # Show typing indicator
        self.show_typing_indicator()
        
        # Queue the message for processing
        self.user_message_queue.put(message)
    
    def animate_status(self, text, color):
        """Animate status bar with color transition"""
        def animate():
            self.status_text.configure(text=text, fg=color)
            self.root.after(2000, lambda: self.status_text.configure(text="Ready", fg='#8b949e'))
        
        animate()
    
    def toggle_voice_input(self):
        """Toggle voice input on/off"""
        if not self.is_listening:
            self.start_voice_input()
        else:
            self.stop_voice_input()
    
    def start_voice_input(self):
        """Start voice input"""
        self.is_listening = True
        self.voice_button.configure(bg='#f85149', text="⏹️")
        self.animate_status("Listening...", "#58a6ff")
        
        # Start voice recognition in separate thread
        threading.Thread(target=self.listen_for_speech, daemon=True).start()
    
    def stop_voice_input(self):
        """Stop voice input"""
        self.is_listening = False
        self.voice_button.configure(bg='#da3633', text="🎤")
        self.animate_status("Voice input stopped", "#8b949e")
    
    def listen_for_speech(self):
        """Listen for speech input"""
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                self.process_speech(audio)
        except sr.WaitTimeoutError:
            self.stop_voice_input()
        except Exception as e:
            print(f"Voice recognition error: {e}")
            self.stop_voice_input()
    
    def process_speech(self, audio):
        """Process speech input"""
        try:
            text = self.recognizer.recognize_google(audio)
            if text.strip():
                # Add speech input to text field
                self.text_input.delete("1.0", tk.END)
                self.text_input.insert("1.0", text)
                
                # Send the message
                self.send_message()
                
                self.stop_voice_input()
        except sr.UnknownValueError:
            self.animate_status("Could not understand audio", "#f85149")
            self.stop_voice_input()
        except sr.RequestError as e:
            self.animate_status("Speech recognition error", "#f85149")
            self.stop_voice_input()
    
    def process_messages(self):
        """Process messages in background thread"""
        while True:
            try:
                # Get user message
                user_message = self.user_message_queue.get(timeout=1)
                
                # Get AI response
                ai_response = self.jarvis.get_ai_response(user_message)
                
                # Queue the response
                self.response_queue.put(ai_response)
                
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Error processing message: {e}")
                self.response_queue.put(f"I apologize, Sir. There seems to be an error: {e}")
    
    def process_message_queue(self):
        """Process queued messages in main thread"""
        try:
            # Check for AI responses
            while not self.response_queue.empty():
                response = self.response_queue.get_nowait()
                
                # Hide typing indicator
                self.hide_typing_indicator()
                
                # Add AI response to conversation
                self.add_message("JARVIS", response, "assistant")
                
                # Speak the response
                threading.Thread(target=self.jarvis.speak, args=(response,), daemon=True).start()
                
        except queue.Empty:
            pass
        
        # Schedule next check
        self.root.after(100, self.process_message_queue)
    
    def run(self):
        """Run the GUI"""
        self.root.mainloop()

def main():
    """Main function"""
    app = ModernJarvisMineGUI()
    app.run()

if __name__ == "__main__":
    main() 