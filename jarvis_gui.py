#!/usr/bin/env python3
"""
JARVIS GUI - Ultra Modern Messenger-like Interface
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

# Import JARVIS functionality
from jarvis_macos import JarvisMacOS

class ModernJarvisGUI:
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
        self.jarvis = JarvisMacOS()
        
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
        
        # Main title with modern font
        title_label = tk.Label(
            title_frame, 
            text="🤖 JARVIS AI Assistant", 
            font=("SF Pro Display", 28, "bold"),
            bg='#161b22',
            fg='#58a6ff'
        )
        title_label.pack()
        
        # Subtitle with subtle styling
        subtitle_label = tk.Label(
            title_frame,
            text="Your Personal AI Companion • Powered by Advanced AI",
            font=("SF Pro Display", 12),
            bg='#161b22',
            fg='#7d8590'
        )
        subtitle_label.pack(pady=(5, 0))
        
        # Status indicator
        self.status_indicator = tk.Label(
            title_frame,
            text="●",
            font=("SF Pro Display", 16),
            bg='#161b22',
            fg='#238636'
        )
        self.status_indicator.pack(side='right', anchor='ne', padx=(0, 20))
    
    def setup_conversation_area(self, parent):
        """Setup beautiful conversation area"""
        # Conversation container with modern styling
        conv_container = tk.Frame(parent, bg='#161b22', relief='flat', bd=0)
        conv_container.grid(row=1, column=0, sticky='nsew', pady=(0, 20))
        conv_container.grid_rowconfigure(0, weight=1)
        conv_container.grid_columnconfigure(0, weight=1)
        
        # Conversation text area with ultra-modern styling (read-only)
        self.conversation_text = scrolledtext.ScrolledText(
            conv_container,
            wrap=tk.WORD,
            bg='#0d1117',
            fg='#f0f6fc',
            font=("SF Pro Display", 12),
            insertbackground='#58a6ff',
            selectbackground='#21262d',
            relief='flat',
            bd=0,
            padx=25,
            pady=25,
            spacing1=5,  # Line spacing
            spacing2=2,
            spacing3=5
        )
        
        # Make it read-only by binding events to prevent editing
        self.conversation_text.bind("<Key>", lambda e: "break")
        self.conversation_text.bind("<Button-1>", lambda e: "break")
        self.conversation_text.bind("<Button-2>", lambda e: "break")
        self.conversation_text.bind("<Button-3>", lambda e: "break")
        self.conversation_text.bind("<B1-Motion>", lambda e: "break")
        self.conversation_text.bind("<B2-Motion>", lambda e: "break")
        self.conversation_text.bind("<B3-Motion>", lambda e: "break")
        self.conversation_text.bind("<ButtonRelease-1>", lambda e: "break")
        self.conversation_text.bind("<ButtonRelease-2>", lambda e: "break")
        self.conversation_text.bind("<ButtonRelease-3>", lambda e: "break")
        self.conversation_text.bind("<Double-Button-1>", lambda e: "break")
        self.conversation_text.bind("<Triple-Button-1>", lambda e: "break")
        self.conversation_text.grid(row=0, column=0, sticky='nsew', padx=2, pady=2)
        
        # Configure tags for beautiful message styling
        self.conversation_text.tag_configure("user_message", foreground="#58a6ff", font=("SF Pro Display", 12, "bold"))
        self.conversation_text.tag_configure("assistant_message", foreground="#7ee787", font=("SF Pro Display", 12, "bold"))
        self.conversation_text.tag_configure("timestamp", foreground="#7d8590", font=("SF Pro Display", 10))
        self.conversation_text.tag_configure("typing", foreground="#7d8590", font=("SF Pro Display", 12, "italic"))
        self.conversation_text.tag_configure("user_bubble", background="#1f6feb", foreground="#ffffff")
        self.conversation_text.tag_configure("assistant_bubble", background="#238636", foreground="#ffffff")
    
    def setup_input_area(self, parent):
        """Setup modern input area with beautiful design"""
        # Input container with modern styling
        input_container = tk.Frame(parent, bg='#161b22', relief='flat', bd=0)
        input_container.grid(row=2, column=0, sticky='ew', pady=(0, 20))
        input_container.grid_columnconfigure(0, weight=1)
        
        # Text input with modern styling
        self.text_input = tk.Entry(
            input_container,
            font=("SF Pro Display", 14),
            bg='#21262d',
            fg='#f0f6fc',
            insertbackground='#58a6ff',
            relief='flat',
            bd=0,
            highlightthickness=2,
            highlightcolor='#58a6ff',
            highlightbackground='#30363d'
        )
        self.text_input.grid(row=0, column=0, sticky='ew', padx=(0, 15), pady=10, ipady=12)
        self.text_input.bind("<Return>", self.send_message)
        self.text_input.bind("<KeyRelease>", self.on_input_change)
        
        # Button container
        button_frame = tk.Frame(input_container, bg='#161b22')
        button_frame.grid(row=0, column=1, sticky='e', pady=10)
        
        # Voice input button with modern design
        self.voice_button = tk.Button(
            button_frame,
            text="🎤",
            font=("SF Pro Display", 18),
            bg='#238636',
            fg='#ffffff',
            relief='flat',
            bd=0,
            padx=20,
            pady=12,
            command=self.toggle_voice_input,
            cursor='hand2',
            activebackground='#2ea043',
            activeforeground='#ffffff'
        )
        self.voice_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Send button with modern styling
        self.send_button = tk.Button(
            button_frame,
            text="Send",
            font=("SF Pro Display", 12, "bold"),
            bg='#1f6feb',
            fg='#ffffff',
            relief='flat',
            bd=0,
            padx=25,
            pady=12,
            command=self.send_message,
            cursor='hand2',
            activebackground='#388bfd',
            activeforeground='#ffffff'
        )
        self.send_button.pack(side=tk.LEFT)
        
        # Bind hover effects
        self.bind_hover_effects()
    
    def setup_status_bar(self, parent):
        """Setup animated status bar"""
        status_frame = tk.Frame(parent, bg='#161b22', height=40)
        status_frame.grid(row=3, column=0, sticky='ew')
        status_frame.grid_propagate(False)
        
        self.status_label = tk.Label(
            status_frame,
            text="Ready to assist you, Sir.",
            font=("SF Pro Display", 11),
            bg='#161b22',
            fg='#7ee787'
        )
        self.status_label.pack(expand=True)
    
    def bind_hover_effects(self):
        """Bind beautiful hover effects to buttons"""
        def on_enter(event):
            widget = event.widget
            if widget == self.voice_button:
                widget.configure(bg='#2ea043')
            elif widget == self.send_button:
                widget.configure(bg='#388bfd')
        
        def on_leave(event):
            widget = event.widget
            if widget == self.voice_button:
                if not self.is_listening:
                    widget.configure(bg='#238636')
                else:
                    widget.configure(bg='#da3633')
            elif widget == self.send_button:
                widget.configure(bg='#1f6feb')
        
        self.voice_button.bind("<Enter>", on_enter)
        self.voice_button.bind("<Leave>", on_leave)
        self.send_button.bind("<Enter>", on_enter)
        self.send_button.bind("<Leave>", on_leave)
    
    def on_input_change(self, event=None):
        """Handle input changes for visual feedback"""
        text = self.text_input.get().strip()
        if text:
            self.send_button.configure(bg='#2ea043')
        else:
            self.send_button.configure(bg='#1f6feb')
    
    def show_typing_indicator(self):
        """Show beautiful typing indicator animation"""
        if self.is_typing:
            return
        
        self.is_typing = True
        dots = 0
        
        def animate_typing():
            nonlocal dots
            if not self.is_typing:
                return
            
            typing_text = "🤖 JARVIS is thinking" + "●" * (dots % 4)
            self.conversation_text.insert(tk.END, f"[{datetime.now().strftime('%H:%M')}] {typing_text}\n", "typing")
            self.conversation_text.see(tk.END)
            
            dots += 1
            self.typing_animation_id = self.root.after(600, animate_typing)
        
        animate_typing()
    
    def hide_typing_indicator(self):
        """Hide typing indicator"""
        self.is_typing = False
        if self.typing_animation_id:
            self.root.after_cancel(self.typing_animation_id)
            self.typing_animation_id = None
        
        # Remove typing indicator from text
        content = self.conversation_text.get("1.0", tk.END)
        lines = content.split('\n')
        new_lines = []
        for line in lines:
            if "🤖 JARVIS is thinking" not in line:
                new_lines.append(line)
        
        self.conversation_text.delete("1.0", tk.END)
        self.conversation_text.insert("1.0", '\n'.join(new_lines))
    
    def add_message(self, sender, message, message_type):
        """Add a message to the conversation display with beautiful styling"""
        timestamp = datetime.now().strftime("%H:%M")
        
        if message_type == "user":
            color_tag = "user_message"
            prefix = "👤 You"
            bubble_tag = "user_bubble"
        else:
            color_tag = "assistant_message"
            prefix = "🤖 JARVIS"
            bubble_tag = "assistant_bubble"
        
        # Format message with modern styling
        formatted_message = f"[{timestamp}] {prefix}: {message}\n\n"
        
        # Add to text widget
        self.conversation_text.insert(tk.END, formatted_message)
        self.conversation_text.see(tk.END)
        
        # Apply beautiful styling
        start = self.conversation_text.index("end-2c linestart")
        end = self.conversation_text.index("end-1c")
        
        # Apply timestamp styling
        timestamp_start = f"{start}+0c"
        timestamp_end = f"{start}+{len(timestamp) + 2}c"
        self.conversation_text.tag_add("timestamp", timestamp_start, timestamp_end)
        
        # Apply message styling
        message_start = f"{start}+{len(timestamp) + 3}c"
        message_end = end
        self.conversation_text.tag_add(color_tag, message_start, message_end)
    
    def send_message(self, event=None):
        """Send a text message with enhanced feedback"""
        message = self.text_input.get().strip()
        if message:
            print(f"User sending message: {message}")
            
            # Clear input
            self.text_input.delete(0, tk.END)
            self.on_input_change()  # Update button color
            
            # Add user message to display
            self.add_message("User", message, "user")
            
            # Show typing indicator
            self.show_typing_indicator()
            
            # Update status with animation
            self.animate_status("Processing your request, Sir...", "#f78166")
            
            # Queue message for processing
            self.user_message_queue.put(message)
            print(f"Message queued for processing: {message}")
    
    def animate_status(self, text, color):
        """Animate status bar text with smooth transitions"""
        def animate():
            current_text = self.status_label.cget("text")
            if current_text != text:
                # Fade out
                self.status_label.configure(fg='#7d8590')
                self.root.after(200, lambda: self.status_label.configure(text=text, fg=color))
        
        animate()
    
    def toggle_voice_input(self):
        """Toggle voice input on/off with enhanced feedback"""
        if not self.is_listening:
            self.start_voice_input()
        else:
            self.stop_voice_input()
    
    def start_voice_input(self):
        """Start voice input with visual feedback"""
        self.is_listening = True
        self.voice_button.config(text="⏹️", bg='#da3633')
        self.animate_status("Listening... Speak now", "#da3633")
        
        # Start voice recognition in separate thread
        threading.Thread(target=self.listen_for_speech, daemon=True).start()
    
    def stop_voice_input(self):
        """Stop voice input with visual feedback"""
        self.is_listening = False
        self.voice_button.config(text="🎤", bg='#238636')
        self.animate_status("Voice input stopped", "#7ee787")
    
    def listen_for_speech(self):
        """Listen for speech input"""
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                while self.is_listening:
                    try:
                        audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=10)
                        
                        # Process speech in separate thread
                        threading.Thread(target=self.process_speech, args=(audio,), daemon=True).start()
                        
                    except sr.WaitTimeoutError:
                        continue
                    except sr.UnknownValueError:
                        continue
                        
        except Exception as e:
            print(f"Voice recognition error: {e}")
            self.stop_voice_input()
    
    def process_speech(self, audio):
        """Process speech input with enhanced feedback"""
        try:
            # Recognize speech
            text = self.recognizer.recognize_google(audio)
            
            if text.strip():
                # Add to GUI (thread-safe)
                self.root.after(0, lambda: self.add_message("User", text, "user"))
                self.root.after(0, lambda: self.animate_status("Processing your request, Sir...", "#f78166"))
                
                # Show typing indicator
                self.root.after(0, self.show_typing_indicator)
                
                # Queue for processing
                self.user_message_queue.put(text)
                
        except sr.UnknownValueError:
            self.root.after(0, lambda: self.animate_status("Could not understand audio", "#da3633"))
        except sr.RequestError as e:
            self.root.after(0, lambda: self.animate_status(f"Speech recognition error: {e}", "#da3633"))
        except Exception as e:
            print(f"Speech processing error: {e}")
    
    def process_messages(self):
        """Process messages in background thread"""
        print("Message processing thread started")
        while True:
            try:
                # Get user message from user queue
                message = self.user_message_queue.get()
                print(f"Background thread processing user message: {message}")
                
                # Get JARVIS response
                response = self.jarvis.get_ai_response(message)
                print(f"JARVIS response: {response}")
                
                # Queue response for GUI thread to handle
                self.response_queue.put(response)
                print("Response queued for GUI thread")
                
            except Exception as e:
                print(f"Message processing error: {e}")
                self.response_queue.put(f"I apologize, Sir. There was an error: {e}")
    
    def process_message_queue(self):
        """Process queued messages for GUI updates"""
        try:
            while True:
                # Get response from response queue
                response = self.response_queue.get_nowait()
                print(f"GUI thread processing response: {response[:50]}...")
                
                # Hide typing indicator
                self.hide_typing_indicator()
                
                # Add JARVIS response to display
                self.add_message("JARVIS", response, "assistant")
                self.animate_status("Ready to assist you, Sir.", "#7ee787")
                print("✅ Response displayed in GUI: " + response[:50] + "...")
                
        except queue.Empty:
            pass
        finally:
            # Schedule next check
            self.root.after(100, self.process_message_queue)
    
    def run(self):
        """Run the GUI"""
        self.root.mainloop()

def main():
    """Main function"""
    print("🤖 Starting Modern JARVIS GUI...")
    gui = ModernJarvisGUI()
    gui.run()

if __name__ == "__main__":
    main() 