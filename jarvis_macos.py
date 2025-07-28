#!/usr/bin/env python3
"""
JARVIS AI Assistant - macOS Optimized
Uses macOS native text-to-speech with Siri-like quality
"""

import os
import openai
import subprocess
import time
import asyncio
from typing import List
from googlesearch import search as _search
from bs4 import BeautifulSoup
from charset_normalizer import detect
from requests_html import AsyncHTMLSession
import urllib3
urllib3.disable_warnings()
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
        
        # Initialize async search capabilities
        self.session = AsyncHTMLSession()
        
        # Initialize conversation memory
        self.conversation_history = []
        self.max_history_length = 10  # Keep last 10 exchanges
        
        # Location context - Taiwan
        self.location_context = {
            'country': 'Taiwan',
            'region': 'Asia',
            'timezone': 'Asia/Taipei',
            'language': 'English',
            'currency': 'TWD (New Taiwan Dollar)',
            'major_cities': ['Taipei', 'Kaohsiung', 'Taichung', 'Tainan', 'Taoyuan']
        }
        
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
    
    async def worker(self, url: str):
        """Async worker to fetch HTML content from URL"""
        try:
            header_response = await asyncio.wait_for(self.session.head(url, verify=False), timeout=10)
            if 'text/html' not in header_response.headers.get('Content-Type', ''):
                return None
            r = await asyncio.wait_for(self.session.get(url, verify=False), timeout=10)
            return r.text
        except:
            return None
    
    async def get_htmls(self, urls):
        """Get HTML content from multiple URLs asynchronously"""
        tasks = (self.worker(url) for url in urls)
        return await asyncio.gather(*tasks)
    
    async def search(self, keyword: str, n_results: int = 3) -> List[str]:
        """
        Async search function that searches keywords and returns text content from web pages.
        
        Warning: You may suffer from HTTP 429 errors if you search too many times in a period of time.
        """
        keyword = keyword[:100]
        # First, search the keyword and get the results. Also, get 2 times more results in case some of them are invalid.
        results = list(_search(keyword, n_results * 3, lang="en", unique=True))
        # Then, get the HTML from the results. Also, the helper function will filter out the non-HTML urls.
        results = await self.get_htmls(results)
        # Filter out the None values.
        results = [x for x in results if x is not None]
        # Parse the HTML.
        results = [BeautifulSoup(x, 'html.parser') for x in results]
        # Get the text from the HTML and remove the spaces. Also, filter out the non-utf-8 encoding.
        results = [''.join(x.get_text().split()) for x in results if detect(x.encode()).get('encoding') == 'utf-8']
        # Return the first n results.
        return results[:n_results]
    
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
                    
                    result = subprocess.run(say_command, capture_output=True, timeout=30, env=env)
                    if result.returncode == 0:
                        success = True
                        print("✅ Speech successful with Alex voice")
                except Exception as e:
                    print(f"Alex voice failed: {e}")
                                
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
    

    
    async def get_web_search_results(self, query):
        """Get web search results using async search with keyword extraction"""
        try:
            # Extract keywords from the query
            keywords = self.extract_search_keywords_with_context(query, "")
            print(f"🔑 Extracted keywords: {keywords}")
            
            # Clean up keywords for search
            search_keywords = keywords.replace(',', ' ').replace('  ', ' ').strip()
            print(f"🔍 Searching with keywords: '{search_keywords}'")
            
            # Perform async search
            search_results = await self.search(search_keywords, n_results=3)
            
            if search_results:
                # Format results for AI with better structure
                search_info = self.format_search_results_from_text(search_results)
                print(f"📄 Found {len(search_results)} search results")
                return search_info
            else:
                print("❌ No search results found")
                return self.get_fallback_response(query)
                
        except Exception as e:
            print(f"Search error: {e}")
            return self.get_fallback_response(query)
    

    
    def format_search_results(self, results):
        """Format search results for AI consumption"""
        # Format general search results
        search_info = "Based on recent web search results:\n\n"
        
        for i, result in enumerate(results[:3], 1):
            title = result.get('title', '').strip()
            snippet = result.get('snippet', '').strip()
            url = result.get('url', '').strip()
            
            # Clean up the snippet
            if len(snippet) > 300:
                snippet = snippet[:300] + "..."
            
            search_info += f"📄 Result {i}:\n"
            search_info += f"Title: {title}\n"
            search_info += f"Summary: {snippet}\n"
            if url:
                search_info += f"Source: {url}\n"
            search_info += "\n"
        
        return search_info
    
    def format_search_results_from_text(self, text_results):
        """Format text search results for AI consumption"""
        search_info = "Based on recent web search results:\n\n"
        
        for i, text_content in enumerate(text_results[:3], 1):
            # Clean up the text content
            cleaned_text = text_content.strip()
            if len(cleaned_text) > 500:
                cleaned_text = cleaned_text[:500] + "..."
            
            search_info += f"📄 Result {i}:\n"
            search_info += f"Content: {cleaned_text}\n"
            search_info += "\n"
        
        return search_info
    
    def get_fallback_response(self, query):
        """Get fallback response when search fails"""
        return f"I couldn't find recent information about '{query}'. The topic might not be searchable or available."
    
    def check_time_query(self, user_input):
        """Check if the query is asking for time in a specific city"""
        import re
        
        user_input_lower = user_input.lower()
        print(f"🔍 Checking time query: '{user_input_lower}'")
        
        # Check for general time queries (no specific city)
        general_time_patterns = [
            r"what(?:'s|\s+is)\s+the\s+time(?:\s+right\s+now|\s+currently|\s+now)?$",
            r"what\s+time\s+(?:is\s+it\s+)?(?:right\s+now|\s+currently|\s+now)?$",
            r"time(?:\s+right\s+now|\s+currently|\s+now)?$",
            r"current\s+time$"
        ]
        
        # Check for general time queries first
        for pattern in general_time_patterns:
            if re.search(pattern, user_input_lower):
                print(f"✅ General time query detected - using Taiwan as default")
                return self.get_time_in_city("taiwan")
        
        # Simple and robust city extraction
        city = None
        
        # Pattern 1: "what time is it in [city]"
        match = re.search(r"what\s+time\s+(?:is\s+it\s+)?(?:in|at)\s+([a-zA-Z\s]+?)(?:\s+right\s+now|\s+currently|\s+now)?$", user_input_lower)
        if match:
            city = match.group(1).strip()
            print(f"✅ Pattern 1 matched: '{city}'")
        
        # Pattern 2: "time in [city]"
        if not city:
            match = re.search(r"time\s+(?:in|at)\s+([a-zA-Z\s]+?)(?:\s+right\s+now|\s+currently|\s+now)?$", user_input_lower)
            if match:
                city = match.group(1).strip()
                print(f"✅ Pattern 2 matched: '{city}'")
        
        # Pattern 3: "[city] time"
        if not city:
            match = re.search(r"([a-zA-Z\s]+?)\s+time(?:\s+right\s+now|\s+currently|\s+now)?$", user_input_lower)
            if match:
                city = match.group(1).strip()
                print(f"✅ Pattern 3 matched: '{city}'")
        
        # Pattern 4: "what's the time in [city]"
        if not city:
            match = re.search(r"what(?:'s|\s+is)\s+the\s+time\s+(?:in|at)\s+([a-zA-Z\s]+?)(?:\s+right\s+now|\s+currently|\s+now)?$", user_input_lower)
            if match:
                city = match.group(1).strip()
                print(f"✅ Pattern 4 matched: '{city}'")
        
        # Pattern 5: Just a city name (fallback)
        if not city:
            # Check if it's just a city name
            common_cities = ['taipei', 'london', 'new york', 'tokyo', 'beijing', 'shanghai', 'singapore', 'sydney', 'paris', 'berlin', 'moscow', 'dubai', 'mumbai', 'seoul', 'hong kong', 'bangkok', 'manila', 'jakarta', 'los angeles', 'la', 'nyc']
            for common_city in common_cities:
                if common_city in user_input_lower:
                    city = common_city
                    print(f"✅ Pattern 5 matched: '{city}'")
                    break
        
        if city:
            # Clean up common words and extra spaces
            city = re.sub(r'\b(now|right\s+now|currently|the)\b', '', city).strip()
            city = re.sub(r'\s+', ' ', city)  # Normalize spaces
            
            if city and len(city) > 2:  # Make sure we have a real city name
                print(f"✅ Final city: '{city}' from input: '{user_input}'")
                return self.get_time_in_city(city)
            else:
                print(f"❌ City too short or empty: '{city}'")
        
        print(f"❌ No time pattern matched for: '{user_input}'")
        return None
    
    def get_time_in_city(self, city_name):
        """Get current time in a specific city"""
        import datetime
        import pytz
        
        # City to timezone mapping - expanded with more variations
        city_timezones = {
            'taiwan': 'Asia/Taipei',
            'taipei': 'Asia/Taipei',
            'taipei taiwan': 'Asia/Taipei',
            'taiwan taipei': 'Asia/Taipei',
            'london': 'Europe/London',
            'new york': 'America/New_York',
            'nyc': 'America/New_York',
            'los angeles': 'America/Los_Angeles',
            'la': 'America/Los_Angeles',
            'tokyo': 'Asia/Tokyo',
            'beijing': 'Asia/Shanghai',
            'shanghai': 'Asia/Shanghai',
            'singapore': 'Asia/Singapore',
            'sydney': 'Australia/Sydney',
            'paris': 'Europe/Paris',
            'berlin': 'Europe/Berlin',
            'moscow': 'Europe/Moscow',
            'dubai': 'Asia/Dubai',
            'mumbai': 'Asia/Kolkata',
            'seoul': 'Asia/Seoul',
            'hong kong': 'Asia/Hong_Kong',
            'bangkok': 'Asia/Bangkok',
            'manila': 'Asia/Manila',
            'jakarta': 'Asia/Jakarta'
        }
        
        # Clean and normalize city name
        city_clean = city_name.lower().strip()
        city_clean = ' '.join(city_clean.split())  # Normalize spaces
        
        print(f"🔍 Looking up timezone for city: '{city_clean}'")
        
        # If no specific city or just asking for current time, use Taiwan as default
        if not city_clean or city_clean in ['now', 'current', 'time', 'what', 'the']:
            try:
                tz = pytz.timezone('Asia/Taipei')
                current_time = datetime.datetime.now(tz)
                time_str = current_time.strftime("%I:%M %p")
                date_str = current_time.strftime("%B %d, %Y")
                return f"The current time in Taiwan is {time_str} on {date_str}."
            except Exception as e:
                print(f"❌ Error getting time for Taiwan: {e}")
                return f"I couldn't get the current time. Error: {e}"
        
        if city_clean in city_timezones:
            try:
                tz = pytz.timezone(city_timezones[city_clean])
                current_time = datetime.datetime.now(tz)
                time_str = current_time.strftime("%I:%M %p")
                date_str = current_time.strftime("%B %d, %Y")
                return f"The current time in {city_name.title()} is {time_str} on {date_str}."
            except Exception as e:
                print(f"❌ Error getting time for {city_clean}: {e}")
                return f"I couldn't get the time for {city_name}. Error: {e}"
        else:
            print(f"❌ No timezone found for: '{city_clean}'")
            print(f"📋 Available cities: {list(city_timezones.keys())}")
            return f"I don't have timezone information for '{city_name}'. Please try a major city like Taipei, London, New York, Tokyo, etc."
    
    def generate_response(self, messages, max_tokens=200, temperature=0.1):
        """
        Generate response using OpenAI with controlled parameters like Llama
        """
        try:
            response = self.openai_client.chat.completions.create(
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=0.9,
                frequency_penalty=0.1,
                presence_penalty=0.1
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Response generation error: {e}")
            return f"I apologize, {self.user_name}. I'm experiencing some connectivity issues."
    
    async def SEARCH(self, query):
        """
        Async search method similar to Search Tool - performs web search and returns results
        """
        try:
            print(f"🔍 SEARCH: '{query}'")
            
            # Extract keywords for search
            keywords = self.extract_search_keywords_with_context(query, "")
            print(f"🔑 Extracted keywords: {keywords}")
            
            # Clean up keywords for search
            search_keywords = keywords.replace(',', ' ').replace('  ', ' ').strip()
            print(f"🔍 Searching with keywords: '{search_keywords}'")
            
            # Perform async search
            results = await self.search(search_keywords, n_results=3)
            
            if results:
                # Format results
                search_info = self.format_search_results_from_text(results)
                print(f"📄 Found {len(results)} search results")
                return search_info
            else:
                print("❌ No search results found")
                return f"No search results found for '{query}'"
                
        except Exception as e:
            print(f"Search error: {e}")
            return f"Search failed for '{query}': {e}"
    
    async def get_ai_response(self, user_input):
        """Get AI response using intelligent question analysis and web search with conversation memory"""
        try:
            # Get conversation context
            conversation_context = self.get_conversation_context()
            
            # Get current date/time for context with proper timezone handling
            import datetime
            import pytz
            
            # Get current time in Taiwan timezone (default location)
            taiwan_tz = pytz.timezone('Asia/Taipei')
            current_time_taiwan = datetime.datetime.now(taiwan_tz)
            current_date = current_time_taiwan.strftime("%B %d, %Y")
            current_time_str = current_time_taiwan.strftime("%I:%M %p")
            current_year = current_time_taiwan.year
            
            # Set Taiwan as default timezone context
            self.default_timezone = 'Asia/Taipei'
            self.default_location = 'Taiwan'
            
            # Step 1: Try to answer from knowledge base first
            print("💡 Attempting to answer from knowledge base...")
            
            # Check if this is a time query for a specific city
            time_query = self.check_time_query(user_input)
            if time_query:
                response_text = time_query
            else:
                # Try to answer from knowledge base using generate_response
                messages = [
                    {
                        "role": "system",
                        "content": f"""You are {self.name}, Tony Stark's AI assistant with a personality similar to Siri. 
                        CRITICAL RULES:
                        1. ALWAYS respond in English only - NEVER use Chinese or any other language
                        2. If the user asks in Chinese, you can respond in Chinese
                        
                        IMPORTANT CONTEXT:
                        - Default timezone is Taiwan (Asia/Taipei)
                        - When users ask about "time" without specifying a city, use Taiwan time
                        - Use conversation context to understand references
                        - If the user says "his", "her", "it", "that", refer to the conversation context
                        - Maintain continuity with previous questions
                        - Be genuinely honest about your knowledge limitations
                        
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
                        "content": f"""CURRENT DATE/TIME INFORMATION:
- Current Date: {current_date}
- Current Time: {current_time_str}
- Current Year: {current_year}
        
Conversation context:
{conversation_context}
        
Question: {user_input}"""
                    }
                ]
                response_text = self.generate_response(messages, max_tokens=200, temperature=0.1)
            
            # Step 2: Check if the answer seems uncertain or incomplete
            uncertain_indicators = [
                "i don't know", "i'm not sure", "i don't have", "i cannot", "i'm unable",
                "i don't have access", "i don't have information", "i don't have data",
                "i don't have knowledge", "i don't have details", "i don't have specifics",
                "i don't have current", "i don't have recent", "i don't have latest",
                "i don't have up-to-date", "i don't have accurate", "i don't have reliable",
                "i don't have complete", "i don't have comprehensive", "i don't have thorough",
                "i don't have sufficient", "i don't have adequate", "i don't have enough",
                "i don't have the information", "i don't have the data", "i don't have the knowledge",
                "i don't have the details", "i don't have the specifics", "i don't have the current",
                "i don't have the recent", "i don't have the latest", "i don't have the up-to-date",
                "i don't have the accurate", "i don't have the reliable", "i don't have the complete",
                "i don't have the comprehensive", "i don't have the thorough", "i don't have the sufficient",
                "i don't have the adequate", "i don't have the enough"
            ]
            
            response_lower = response_text.lower()
            needs_web_search = any(indicator in response_lower for indicator in uncertain_indicators)
            
            print(f"📝 Knowledge base response: {response_text}")
            print(f"🔍 Uncertainty detected: {needs_web_search}")
            
            # Also check for specific topics that should always trigger web search
            web_search_topics = [
                "war", "conflict", "election", "recall", "vote", "political", "campaign",
                "current events", "latest news", "breaking news", "recent developments",
                "what happened", "what will happen", "when did", "where did", "how did",
                "specific date", "specific time", "current situation", "ongoing"
            ]
            
            user_input_lower = user_input.lower()
            topic_requires_search = any(topic in user_input_lower for topic in web_search_topics)
            
            if topic_requires_search:
                needs_web_search = True
                print(f"🎯 Topic requires web search: {topic_requires_search}")
            
            print(f"🌐 Final decision - Web search needed: {needs_web_search}")
            
            if needs_web_search:
                print("🌐 Knowledge base answer seems uncertain, searching the web...")
                print(f"📝 Original question: {user_input}")
                
                # Step 3: Perform web search with the original question
                print(f"🔍 Searching web for: '{user_input}'")
                search_results = await self.get_web_search_results(user_input)
                print(f"📋 Search results received: {len(search_results) if search_results else 0} characters")
                print(f"📄 Search results preview: {search_results[:200] if search_results else 'None'}...")
                
                                # Step 4: Generate response with web data and context using generate_response
                messages = [
                    {
                        "role": "system",
                        "content": f"""You are {self.name}, Tony Stark's AI assistant with a personality similar to Siri. 
                        CRITICAL RULES:
                        1. ALWAYS respond in English only - NEVER use Chinese or any other language
                        2. If the user asks in Chinese, you can respond in Chinese
                        
                        IMPORTANT CONTEXT:
                        - Default timezone is Taiwan (Asia/Taipei)
                        - When users ask about "time" without specifying a city, use Taiwan time
                        - Use conversation context to understand references
                        - If the user says "his", "her", "it", "that", refer to the conversation context
                        - Maintain continuity with previous questions
                        - Be genuine about the search process
                        
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
                        "content": f"Conversation context:\n{conversation_context}\n\nCurrent question: {user_input}\n\nWeb search results:\n{search_results}\n\nIMPORTANT: Provide a specific and accurate response based on the search results. If the search results don't contain the specific information requested, be honest and say what you found instead. Focus on the most relevant information from the search results."
                    }
                ]
                ai_response = self.generate_response(messages, max_tokens=250, temperature=0.1)
                
                # Add to conversation history
                self.add_to_conversation_history(user_input, ai_response)
                
                return ai_response
            else:
                # Step 5: Answer from knowledge base with context
                print("💡 Answering from knowledge base with context...")
                
                # Check if this is a time query for a specific city
                time_query = self.check_time_query(user_input)
                if time_query:
                    response_text = time_query
                else:
                                        messages = [
                        {
                            "role": "system",
                            "content": f"""You are {self.name}, Tony Stark's AI assistant with a personality similar to Siri. 
                            CRITICAL RULES:
                            1. ALWAYS respond in English only - NEVER use Chinese or any other language
                            2. If the user asks in Chinese, you can respond in Chinese
                            
                            IMPORTANT CONTEXT:
                            - Default timezone is Taiwan (Asia/Taipei)
                            - When users ask about "time" without specifying a city, use Taiwan time
                            - Use conversation context to understand references
                            - If the user says "his", "her", "it", "that", refer to the conversation context
                            - Maintain continuity with previous questions
                            - Be genuinely honest about your knowledge limitations
                            
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
                            "content": f"""CURRENT DATE/TIME INFORMATION:
- Current Date: {current_date}
- Current Time: {current_time_str}
- Current Year: {current_year}
        
Conversation context:
{conversation_context}
        
Question: {user_input}"""
                        }
                    ]
                    response_text = self.generate_response(messages, max_tokens=200, temperature=0.1)
                
                ai_response = response_text
                
                # Add to conversation history
                self.add_to_conversation_history(user_input, ai_response)
                
                return ai_response
                
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
    
    async def run(self):
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
                    
                    # Check for clear memory command
                    if any(word in user_input.lower() for word in ['clear memory', 'forget', 'reset conversation']):
                        self.conversation_history = []
                        self.speak(f"Memory cleared, {self.user_name}. Starting fresh.")
                        continue
                    
                    # Get AI response
                    response = await self.get_ai_response(user_input)
                    
                    # Speak the response with Siri-like voice
                    self.speak(response)
                
            except KeyboardInterrupt:
                print("\nShutting down JARVIS...")
                self.speak(f"Goodbye, {self.user_name}. JARVIS signing off.")
                break
            except Exception as e:
                print(f"Error: {e}")
                self.speak(f"I apologize, {self.user_name}. There seems to be an error.")

    def create_question_analysis_agent(self):
        """Create an agent to analyze and extract core questions"""
        return {
            "role": "system",
            "content": """You are a question analysis expert. Your task is to:
            1. Extract the core question from user input
            2. Determine if this is casual conversation or information request
            3. Focus on what the user actually wants to know
            4. Return only the essential question
            5. Consider the current date when making decisions:
               - If asking for information after 2023, likely needs web search
               - If asking for "current", "latest", "recent", "today", "now", needs web search
               - If asking for factual knowledge that doesn't change (math, history, science), doesn't need web search
               - If it's casual conversation (greetings, chit-chat, opinions), doesn't need web search
            6. Be honest about uncertainty - if you're not confident, suggest web search
            7. Consider confidence level in your analysis
            
            Examples:
            - "Hello" → NO web search (casual greeting)
            - "How are you?" → NO web search (casual conversation)
            - "What's 2+2?" → NO web search (basic math)
            - "Who is Einstein?" → NO web search (historical fact)
            - "Tell me a joke" → NO web search (casual request)
            - "What's the weather today?" → YES web search (current info)
            - "Latest news about AI" → YES web search (current info)"""
        }
    
    def create_keyword_extraction_agent(self):
        """Create an agent to extract search keywords"""
        return {
            "role": "system", 
            "content": """You are a keyword extraction expert for web search. Your task is to:

EXTRACTION RULES:
1. Extract the MOST IMPORTANT keywords that will find the specific information requested
2. Focus on specific names, places, dates, events, organizations
3. Include temporal words: "latest", "current", "recent", "2024", "2025", "today", "now"
4. Include action words: "happened", "occurred", "started", "ended", "announced"
5. For current events: include "latest news" or "current events"
6. For historical events: include the specific year or time period
7. For conflicts/wars: include both countries/parties involved
8. Remove common words like "what", "when", "where", "how", "is", "the", "a", "an"

EXAMPLES:
- "When did the Israel and Iran war happen?" → "Israel Iran war conflict when started occurred"
- "What will happen during the 7/26?" → "July 26 2024 events Taiwan latest news"
- "Election recall Taiwan" → "Taiwan election recall vote latest news"
- "Latest news about AI" → "AI artificial intelligence latest news current events"

Return ONLY the keywords separated by commas, no explanations."""
        }
    
    def analyze_question(self, user_input):
        """Analyze the question to determine if web search is needed"""
        try:
            # Get current time for context
            import datetime
            current_time = datetime.datetime.now()
            current_date = current_time.strftime("%B %d, %Y")
            current_year = current_time.year
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    self.create_question_analysis_agent(),
                    {
                        "role": "user",
                        "content": f"""Current date: {current_date} (Year: {current_year})

Analyze this question: {user_input}

Consider:
- If the question asks for information after 2023, it likely needs web search
- If it asks for "current", "latest", "recent", "today", "now" information, it needs web search
- If it asks for factual knowledge that doesn't change (math, history, science), it doesn't need web search
- If you're unsure about the accuracy of your knowledge, be honest and suggest web search

Respond with:
1. Core question: [extracted question]
2. Needs web search: [yes/no]
3. Reason: [why web search is needed or not]
4. Confidence level: [high/medium/low]"""
                    }
                ],
                max_tokens=200,
                temperature=0.1
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Question analysis error: {e}")
            return "Needs web search: yes"
    
    def analyze_question_with_context(self, user_input, conversation_context, current_date, current_time_str, current_year):
        """Analyze the question with conversation context and current date"""
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    self.create_question_analysis_agent(),
                    {
                        "role": "user",
                                                    "content": f"""CURRENT DATE/TIME INFORMATION:
- Current Date: {current_date}
- Current Time: {current_time_str}
- Current Year: {current_year}

LOCATION CONTEXT (Taiwan):
- Country: Taiwan
- Region: Asia
- Timezone: Asia/Taipei
- Major Cities: Taipei, Kaohsiung, Taichung, Tainan, Taoyuan
- Currency: TWD (New Taiwan Dollar)

Conversation context:
{conversation_context}

Current question: {user_input}

ANALYSIS RULES:
- For current date/time questions: Answer directly using provided date/time (NO web search needed)
- For time in specific cities: Answer directly using timezone calculations (NO web search needed)
- For weather in Taiwan: Needs web search (use Taiwan location context)
- For Taiwan news/events: Needs web search (current events in Taiwan)
- For Taiwan stock market: Needs web search (TWSE - Taiwan Stock Exchange)
- For general weather, news, stock prices, current events: Needs web search (information changes)
- For math, history, science facts: No web search needed (static knowledge)
- For information after 2023 that you're unsure about: Needs web search
- For casual conversation: No web search needed
- If uncertain about accuracy: Suggest web search

EXAMPLES:
- "What's the date today?" → NO web search (use provided date)
- "What time is it in London?" → NO web search (use timezone calculation)
- "What's the weather in Taipei?" → YES web search (Taiwan weather)
- "What's the weather?" → YES web search (assume Taiwan location)
- "Taiwan news today" → YES web search (Taiwan current events)
- "What's 2+2?" → NO web search (static fact)
- "Latest news about AI" → YES web search (current events)
- "Who is Einstein?" → NO web search (historical fact)

Respond with:
1. Core question: [extracted question with context]
2. Needs web search: [yes/no]
3. Reason: [why web search is needed or not]
4. Confidence level: [high/medium/low]"""
                    }
                ],
                max_tokens=200,
                temperature=0.1
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Question analysis error: {e}")
            return "Needs web search: yes"
    
    def extract_search_keywords_with_context(self, question, conversation_context):
        """Extract keywords for web search with conversation context"""
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    self.create_keyword_extraction_agent(),
                    {
                        "role": "user", 
                        "content": f"""Conversation context:
{conversation_context}

Extract search keywords from: {question}

IMPORTANT: 
- Use conversation context to understand references (his, her, it, that)
- Focus on specific names, places, dates, events
- Include "latest" or "current" if asking for recent information
- Include "news" if asking about current events
- Make keywords search-friendly (e.g., "earthquake Taiwan" not "earthquake in Taiwan")

Return only the keywords separated by commas, no explanations."""
                    }
                ],
                max_tokens=100,
                temperature=0.1
            )
            keywords = response.choices[0].message.content.strip()
            print(f"🔑 Extracted keywords with context: {keywords}")
            return keywords
        except Exception as e:
            print(f"Keyword extraction error: {e}")
            return question
    
    def add_to_conversation_history(self, user_input, ai_response):
        """Add exchange to conversation history"""
        self.conversation_history.append({
            'user': user_input,
            'assistant': ai_response,
            'timestamp': time.time()
        })
        
        # Keep only the last max_history_length exchanges
        if len(self.conversation_history) > self.max_history_length:
            self.conversation_history = self.conversation_history[-self.max_history_length:]
    
    def get_conversation_context(self):
        """Get recent conversation context for AI"""
        if not self.conversation_history:
            return ""
        
        context = "Recent conversation context:\n"
        for i, exchange in enumerate(self.conversation_history[-3:], 1):  # Last 3 exchanges
            context += f"{i}. User: {exchange['user']}\n"
            context += f"   Assistant: {exchange['assistant']}\n\n"
        
        return context
    
    def extract_search_keywords(self, question):
        """Extract keywords for web search"""
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    self.create_keyword_extraction_agent(),
                    {
                        "role": "user", 
                        "content": f"""Extract search keywords from: {question}

IMPORTANT: 
- Focus on specific names, places, dates, events
- Include "latest" or "current" if asking for recent information
- Include "news" if asking about current events
- Make keywords search-friendly (e.g., "earthquake Taiwan" not "earthquake in Taiwan")

Return only the keywords separated by commas, no explanations."""
                    }
                ],
                max_tokens=100,
                temperature=0.1
            )
            keywords = response.choices[0].message.content.strip()
            print(f"🔑 Extracted keywords: {keywords}")
            return keywords
        except Exception as e:
            print(f"Keyword extraction error: {e}")
            return question

async def main():
    """Main function"""
    print("🤖 JARVIS AI Assistant - macOS Optimized")
    print("Make sure you have set your OPENAI_API_KEY in config.py")
    print("=" * 50)
    
    jarvis = JarvisMacOS()
    await jarvis.run()

if __name__ == "__main__":
    asyncio.run(main()) 