# 🤖 JARVIS AI Assistant

An Iron Man-inspired AI assistant with voice capabilities, built with Python and OpenAI.

## 🚀 Features

- **Voice Interaction**: Talk to JARVIS and get voice responses
- **Siri-like Voice Quality**: Natural speech patterns and professional voice
- **OpenAI Integration**: Powered by GPT-3.5-turbo for intelligent responses
- **Windows Native TTS**: High-quality text-to-speech using Windows built-in voices
- **Multiple Voice Options**: Automatically selects the best available voice
- **Natural Speech Processing**: Pauses, emphasis, and natural flow like Siri

## 📋 Requirements

- Python 3.7+
- Windows 10/11 (for voice features)
- OpenAI API key
- WSL (Windows Subsystem for Linux) recommended

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/jarvis-ai.git
   cd jarvis-ai
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your OpenAI API key:**
   Edit `config.py` and add your OpenAI API key:
   ```python
   OPENAI_API_KEY = "your-openai-api-key-here"
   ```

## 🎯 Usage

### GUI Interface (Recommended)
For a modern messenger-like interface with text and voice input:

```bash
python jarvis_gui.py
# or
python launch_jarvis_gui.py
```

### Command Line Interface

#### Main JARVIS (Voice-enabled)
```bash
python jarvis_windows.py
```

#### Basic JARVIS (Text-only)
```bash
python jarvis.py
```

#### macOS Optimized
```bash
python jarvis_macos.py
```

## 🎤 Voice Features

### Siri-like Voice Quality
- **Natural speech patterns** with pauses and emphasis
- **Professional male voice** selection
- **Multiple voice testing** to find the best quality
- **Emphasis on important words** like "JARVIS", "Sir", "Tony"

### Voice Settings
- **Rate**: Slightly slower for clarity (-2)
- **Volume**: Full volume (100)
- **Pitch**: Natural pitch (0)
- **Voice**: Microsoft David Desktop (professional male)

### Speech Processing
- Adds natural pauses after greetings
- Emphasizes key words and names
- Includes dramatic pauses for questions
- Natural flow with comma pauses

## 🗂️ Project Structure

```
jarvis-ai/
├── jarvis_windows.py    # Main voice-enabled JARVIS (Siri-like)
├── jarvis.py           # Basic voice-enabled JARVIS
├── config.py           # Configuration settings
├── requirements.txt    # Python dependencies
├── templates/          # Web interface templates
└── README.md          # This file
```

## 🔧 Configuration

Edit `config.py` to customize:
- OpenAI API key
- Voice settings
- User name
- Speech rate and volume

## 🎮 Commands

- **Talk to JARVIS**: Just speak or type your questions
- **Exit**: Say "goodbye", "quit", "exit", or "stop"
- **Voice Input**: Type your messages (voice input requires Windows Speech Recognition setup)

## 🎨 Features in Detail

### Voice Recognition
- Windows Speech Recognition (when enabled)
- Text input fallback for immediate use
- Natural language processing

### Text-to-Speech
- Windows native TTS with multiple voice options
- Siri-like speech patterns
- Professional voice quality
- Natural pauses and emphasis

### AI Responses
- Powered by OpenAI GPT-3.5-turbo
- Siri-like personality
- Knowledgeable about any topic
- Concise and engaging responses

## 🐛 Troubleshooting

### No Sound
- Ensure Windows audio is working
- Check if Windows TTS is available
- Try running in text-only mode

### Voice Quality Issues
- The system automatically tests multiple voices
- Falls back to default voice if needed
- Voice settings can be adjusted in code

### OpenAI API Errors
- Check your API key in `config.py`
- Ensure you have OpenAI API credits
- Check internet connection

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- Inspired by Iron Man's JARVIS
- Voice design inspired by Siri
- Built with OpenAI GPT-3.5-turbo
- Uses Windows native text-to-speech

## 📞 Support

If you encounter any issues:
1. Check the troubleshooting section
2. Ensure all dependencies are installed
3. Verify your OpenAI API key is correct
4. Try running in text-only mode first

---

**"Sometimes you gotta run before you can walk."** - Tony Stark

*JARVIS AI Assistant - Your personal AI companion* 