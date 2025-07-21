#!/usr/bin/env python3
"""
Debug script to test macOS speech functionality
"""

import subprocess
import sys

def test_basic_speech():
    """Test basic speech functionality"""
    print("🔍 Testing basic speech functionality...")
    
    try:
        # Test 1: Basic say command
        print("Test 1: Basic 'say' command")
        result = subprocess.run(['say', 'Hello, this is a test'], capture_output=True, timeout=5)
        print(f"Result: {result.returncode}")
        if result.stderr:
            print(f"Error: {result.stderr.decode()}")
        
        # Test 2: List available voices
        print("\nTest 2: List available voices")
        result = subprocess.run(['say', '-v', '?'], capture_output=True, text=True, timeout=10)
        print(f"Result: {result.returncode}")
        if result.stdout:
            voices = result.stdout
            print("Available voices:")
            for line in voices.split('\n')[:10]:  # Show first 10
                if line.strip():
                    print(f"  {line}")
        
        # Test 3: Test specific voice
        print("\nTest 3: Test Alex voice")
        result = subprocess.run(['say', '-v', 'Alex', 'Testing Alex voice'], capture_output=True, timeout=5)
        print(f"Result: {result.returncode}")
        
        # Test 4: Test with rate
        print("\nTest 4: Test with speech rate")
        result = subprocess.run(['say', '-v', 'Alex', '-r', '175', 'Testing speech rate'], capture_output=True, timeout=5)
        print(f"Result: {result.returncode}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_jarvis_speech():
    """Test JARVIS-style speech"""
    print("\n🔍 Testing JARVIS-style speech...")
    
    try:
        # Test the exact command JARVIS would use
        test_text = "Today is August 12, 2023, Sir."
        say_command = [
            'say',
            '-v', 'Alex',
            '-r', '175',
            test_text
        ]
        
        print(f"Command: {' '.join(say_command)}")
        result = subprocess.run(say_command, capture_output=True, timeout=10)
        print(f"Result: {result.returncode}")
        
        if result.stderr:
            print(f"Error: {result.stderr.decode()}")
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🤖 JARVIS Speech Debug Tool")
    print("=" * 40)
    
    # Test basic functionality
    basic_ok = test_basic_speech()
    
    # Test JARVIS-style speech
    jarvis_ok = test_jarvis_speech()
    
    print("\n" + "=" * 40)
    print("📊 Results:")
    print(f"Basic speech: {'✅ OK' if basic_ok else '❌ FAILED'}")
    print(f"JARVIS speech: {'✅ OK' if jarvis_ok else '❌ FAILED'}")
    
    if not basic_ok:
        print("\n💡 Suggestions:")
        print("1. Check if 'say' command is available")
        print("2. Check macOS System Preferences > Accessibility > Speech")
        print("3. Try: which say")
    
    if not jarvis_ok:
        print("\n💡 JARVIS-specific issues:")
        print("1. Check if Alex voice is available")
        print("2. Try different voice names")
        print("3. Check speech rate settings") 