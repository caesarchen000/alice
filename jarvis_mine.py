import os
import openai
import subprocess
import time
import asyncio
import requests
import datetime
from typing import List
from googlesearch import search as _search
from bs4 import BeautifulSoup
from charset_normalizer import detect
from requests_html import AsyncHTMLSession
import urllib3
urllib3.disable_warnings()
from config import OPENAI_API_KEY


class Jarvis:
    def __init__(self):

        # user and client
        self.name = "Jarvis"
        self.user_name="Sir"

        # model and api
        self.open_ai_key = OPENAI_API_KEY
        self.model = "gpt-4o"
        self.openai_client = openai.OpenAI(api_key=self.open_ai_key)
        self.session = AsyncHTMLSession()

        # conversation history
        self.conversation_history = []
        self.conversation_history_length=10
        self.chat_history = []  # For casual conversation memory

        #voice setting
        self.voice_setting = {
            "rate": 200,
            "volume": 100,
            "speed": 1.5,
            "voice": "en-US-Standard-A",
            "language": "en-US",
        }

    def generate_response(self, messages, max_tokens=200, temperature=0.1):
        """
        Generate response using OpenAI with controlled parameters like Llama
        """
        try:
            response = self.openai_client.chat.completions.create(
                model=self.model,
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

    
    def speak(self, _text: str):
        """Speak the given text using macOS native TTS"""
        
        # Use macOS native 'say' command with voice settings
        voice = "Daniel"  # Good male voice for JARVIS
        rate = self.voice_setting["rate"]
        
        # Build the say command
        cmd = [
            "say",
            "-v", voice,
            "-r", str(rate),
            _text
        ]
        
        # Execute the command
        subprocess.run(cmd, check=True, timeout=30)
        print(f"🗣️ JARVIS: {_text}")

    def greet(self):
        hour=time.localtime().tm_hour
        if hour<12:
            greeting=f"Good morning, {self.user_name}. JARVIS at your service."
        elif hour<17:
            greeting=f"Good afternoon, {self.user_name}. How may I assist you today?"
        else:
            greeting=f"Good evening, {self.user_name}. JARVIS ready for your commands." 
        self.speak(greeting)

    def listen(self):
        print("Listening... (Speak now)")

        try:
            return input("You: ").strip()
        except Exception as e:
            print(f"Error: {e}")
            return input("You: ").strip()

    def get_ai_response(self, user_input):
        """Get AI response - either casual chat or Q&A based on input type"""
        try:
            # Check if this is a casual conversation or a question that needs web search
            if self.is_casual_conversation(user_input):
                # Use direct AI response for casual chat with memory
                messages = [
                    {"role": "system", "content": f"You are JARVIS, a friendly AI assistant. You're chatting with {self.user_name}. Be conversational, friendly, and engaging. Keep responses natural and not too formal. You can ask questions, share thoughts, and have a normal conversation. Remember previous parts of the conversation to maintain context."}
                ]
                
                # Add conversation history (last 10 exchanges)
                for msg in self.chat_history[-20:]:  # Keep last 20 messages
                    messages.append(msg)
                
                # Add current user input
                messages.append({"role": "user", "content": user_input})
                
                response = self.generate_response(messages, max_tokens=150, temperature=0.7)
                
                # Add to conversation history
                self.chat_history.append({"role": "user", "content": user_input})
                self.chat_history.append({"role": "assistant", "content": response})
                
                # Keep only last 20 messages to avoid context overflow
                if len(self.chat_history) > 20:
                    self.chat_history = self.chat_history[-20:]
            else:
                # Use pipeline for questions that might need web search, but also record the conversation
                response = pipeline(user_input)
                
                # Add to conversation history for search-based responses too
                self.chat_history.append({"role": "user", "content": user_input})
                self.chat_history.append({"role": "assistant", "content": response})
                
                # Keep only last 20 messages to avoid context overflow
                if len(self.chat_history) > 20:
                    self.chat_history = self.chat_history[-20:]
            return response
        except Exception as e:
            print(f"Error getting AI response: {e}")
            return f"I apologize, {self.user_name}. I'm experiencing some connectivity issues."
    
    def get_ai_response_with_vision(self, user_input, image_data=None):
        """Get AI response with vision support for image analysis"""
        try:
            messages = [
                {"role": "system", "content": f"You are JARVIS, a friendly AI assistant with vision capabilities. You're chatting with {self.user_name}. You can see and analyze images. Be conversational, friendly, and engaging. Keep responses natural and not too formal. You can ask questions, share thoughts, and have a normal conversation. Remember previous parts of the conversation to maintain context."}
            ]
            
            # Add conversation history
            for msg in self.chat_history[-20:]:
                messages.append(msg)
            
            # Prepare user message
            if image_data:
                if user_input:
                    # Both text and image
                    user_message = [
                        {"type": "text", "text": user_input},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}}
                    ]
                else:
                    # Only image
                    user_message = [
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}}
                    ]
            else:
                # Only text
                user_message = user_input
            
            messages.append({"role": "user", "content": user_message})
            
            # Generate response with vision model
            response = self.generate_response_with_vision(messages, max_tokens=200, temperature=0.7)
            
            # Add to conversation history
            self.chat_history.append({"role": "user", "content": user_input or "[Image]"})
            self.chat_history.append({"role": "assistant", "content": response})
            
            # Keep only last 20 messages to avoid context overflow
            if len(self.chat_history) > 20:
                self.chat_history = self.chat_history[-20:]
                
            return response
        except Exception as e:
            print(f"Error getting AI response with vision: {e}")
            return f"I apologize, {self.user_name}. I'm experiencing some connectivity issues with image processing."
    
    def generate_response_with_vision(self, messages, max_tokens=200, temperature=0.7):
        """Generate response using OpenAI with vision capabilities"""
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",  # Use GPT-4o for vision
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=0.9,
                frequency_penalty=0.1,
                presence_penalty=0.1
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Vision response generation error: {e}")
            return f"I apologize, {self.user_name}. I'm experiencing some connectivity issues."
    
    def is_casual_conversation(self, user_input):
        """Use AI to determine if the input is casual conversation or needs web search"""
        try:
            messages = [
                {"role": "system", "content": """You are a conversation classifier. Your job is to determine if a user's input is:
                
                CASUAL CONVERSATION (respond with "casual"):
                - Greetings, small talk, personal opinions
                - Emotional expressions, feelings, thoughts
                - Jokes, entertainment requests
                - Personal questions about you or the user
                - General conversation, chit-chat
                - Philosophical discussions, opinions
                
                QUESTION NEEDING WEB SEARCH (respond with "search"):
                - Factual questions about current events, people, places
                - Questions about specific dates, times, prices, weather
                - Questions requiring up-to-date information
                - Questions about recent news, politics, sports
                - Questions about specific facts, statistics, data
                - Questions that might have changed answers over time
                
                Respond with ONLY "casual" or "search" - no other text."""},
                {"role": "user", "content": f"Classify this input: {user_input}"}
            ]
            
            response = self.generate_response(messages, max_tokens=10, temperature=0.1)
            response = response.strip().lower()
            
            print(f"🤖 AI classified '{user_input}' as: {response}")
            
            return response == "casual"
            
        except Exception as e:
            print(f"Error in conversation classification: {e}")
            # Fallback: treat as casual if it's short or doesn't contain question words
            input_lower = user_input.lower()
            return len(user_input.split()) <= 5 or not any(word in input_lower for word in ['what', 'who', 'where', 'when', 'how', 'why', '?'])
    
    def run(self):
        """Main JARVIS loop"""
        self.greet()
        while True:
            try:
                user_input = self.listen()
                if user_input:
                    if any(word in user_input.lower() for word in ['goodbye', 'bye', 'exit', 'quit', 'stop']):
                        self.speak(f"Goodbye, {self.user_name}. JARVIS signing off.")
                        break
                    if any(word in user_input.lower() for word in ['clear memory', 'forget', 'reset conversation']):
                        self.conversation_history = []
                        self.speak(f"Memory cleared, {self.user_name}. Starting fresh.")
                        continue
                    response = self.get_ai_response(user_input)
                    self.speak(response)

            except KeyboardInterrupt:
                print("\nShutting down JARVIS...")
                self.speak(f"Goodbye, {self.user_name}. JARVIS signing off.")
                break
            except Exception as e:
                print(f"Error: {e}")
                self.speak(f"I apologize, {self.user_name}. There seems to be an error.")

# Web search functions (moved outside class for modularity)
def fetch_url(url: str):
    """Optimized synchronous URL fetching using requests with shorter timeouts"""
    try:
        print(f"🔗 Fetching: {url}")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10, verify=False)
        
        if response.status_code == 200:
            content_type = response.headers.get('Content-Type', '')
            print(f"📄 Content-Type: {content_type}")
            
            if 'text/html' in content_type:
                print(f"✅ Successfully fetched: {url}")
                return response.text
            else:
                print(f"❌ Not HTML content: {content_type}")
                return None
        else:
            print(f"❌ HTTP {response.status_code} for {url}")
            return None
    except Exception as e:
        print(f"❌ Error fetching {url}: {e}")
        return None

def search(keyword: str, n_results: int=2) -> List[str]:
    """Search function that searches keywords and returns text content from web pages"""
    try:
        print(f"🔍 Searching for: '{keyword}'")
        keyword = keyword[:100]
        
        # Search using Google 
        search_urls = list(_search(keyword, num_results=n_results * 2, lang="en", unique=True))
        print(f"📄 Found {len(search_urls)} URLs from search")
        
        if not search_urls:
            print("❌ No search URLs found")
            return []
        
        # Fetch HTML content synchronously
        results = []
        for url in search_urls[:n_results * 2]:  # Limit to fewer URLs
            html_content = fetch_url(url)
            if html_content:
                results.append(html_content)
                if len(results) >= n_results:  # Stop when we have enough
                    break
        
        print(f"📄 Successfully fetched {len(results)} HTML pages")
        
        # Parse HTML and extract text with faster processing
        text_results = []
        for html_content in results:
            try:
                soup = BeautifulSoup(html_content, 'html.parser')
                
                # Remove script and style elements for faster processing
                for script in soup(["script", "style"]):
                    script.decompose()
                
                text_content = soup.get_text()
                # Clean up the text more efficiently
                lines = (line.strip() for line in text_content.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                text_content = ' '.join(chunk for chunk in chunks if chunk)
                
                if len(text_content) > 300:  # Shorter content for faster processing
                    text_content = text_content[:300] + "..."
                text_results.append(text_content)
            except Exception as e:
                print(f"❌ Error parsing HTML: {e}")
                continue
        
        print(f"📄 Extracted text from {len(text_results)} pages")
        return text_results[:n_results]
        
    except Exception as e:
        print(f"❌ Search error: {e}")
        return []

class JarvisAgent():

    def __init__(self, role_description: str, task_description: str, llm: Jarvis, temperature=0.2, max_tokens=512, verbose=False):
        self.role_description = role_description   # Role means who this agent should act like. e.g. the history expert, the manager......
        self.task_description = task_description    # Task description instructs what task should this agent solve.
        self.temperature=temperature
        self.verbose=verbose
        self.max_tokens=max_tokens
        self.llm = llm  # LLM indicates which LLM backend this agent is using.
    
    def inference(self, message:str) -> str:
        # Format the messsages first.
        if self.verbose:
            print(f" Agent Role {self.role_description}")
            print(f" Tasks: {self.task_description}")
            print(f" User message: {message}")
        messages = [
            {"role": "system", "content": f"your role：{self.role_description}, please reply in English"},  
            {"role": "user", "content": f"your task: {self.task_description}\n message: {message}"},
        ]
        return self.llm.generate_response(messages)

# Create a Jarvis instance for the agents
jarvis_instance = Jarvis()

question_extraction_agent = JarvisAgent(
    role_description="You are a question extraction agent, your task is to extract the question from the message, and avoid responding things irrelevant to the question",
    task_description="""1. Please extract the question from the message and delete the irrelevant information
                        2. Dont just answer the question
                        3. When generating response, please directly answer the question, no need to say anything else
                    """,
    llm=jarvis_instance,
    verbose=False
)

keyword_extraction_agent = JarvisAgent(
    role_description="You are a keyword extraction agent, your task is to extract the keywords from the message for web searching",
    task_description="""1. please extract the keywords from the message and delete the irrelevant information and 助詞
                        2. additional rule: if the question contains "most", "how many", "how long", "how tall", "who", "where", "first", "last", "who's", "which", "according to...", then these words must be included in the keywords
                        3. dont just answer the questions
                        4. when generating response, please directly answer the keywords, no need to say anything else, and use comma to separate the keywords
                        5. if the question contains "according to...", then should also add the "according to..." to the keywords
                    """,
    llm=jarvis_instance,
    verbose=False
)

qa_agent = JarvisAgent(
    role_description="You are a direct question answering agent that gives clear, concise answers",
    task_description="""ANSWER STRATEGY:
                        1. Give direct, concise answers - no long explanations
                        2. If web search results show clear information: Use it and say "Based on web search"
                        3. If web search is unclear/contradictory: Use your knowledge and say "Based on my knowledge"
                        4. For current information (prices, news, current events): Trust recent web search results
                        5. For historical facts: Use your knowledge if web search is unclear
                        6. Keep answers short and to the point
                        
                        You will be given:
                        1. the question
                        2. the web search results
                        
                        Goal: Give a clear, direct answer
                        Answer format: Short, direct response with source mentioned
                        Your response should be in English
                    """,
    llm=jarvis_instance,
    verbose=False
)

'''      RAG PIPELINE:      '''

def fetch_html(url):
    """ Fetches clean text from a webpage using requests & BeautifulSoup. """
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            print(f"Failed to fetch {url}, Status Code: {response.status_code}")
            return None
        
        # Parse HTML
        soup = BeautifulSoup(response.text, "html.parser")

        # Remove unnecessary elements
        for script in soup(["script", "style", "header", "footer", "nav", "aside"]):
            script.extract()

        # Extract visible text
        text = soup.get_text(separator=" ")

        # Clean up extra spaces
        clean_text = " ".join(text.split())

        return clean_text[:10000]  # Truncate to avoid excessive length

    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None
    
def pipeline(question: str) -> str:
    core_question=question_extraction_agent.inference(question)
    print(f"core question:{core_question}")
    search_keywords=keyword_extraction_agent.inference(core_question)
    print(f"search keywords:{search_keywords}")
    search_results=search(search_keywords)
    print(f"search results:{search_results}")
    MAX_CONTEXT_SIZE = 8000  # Reduced context size for faster processing
    # Ensure the text fits within the model’s limit
    retrieved_text = "\n\n".join(search_results)  # Join all search results into one text block
    retrieved_text = retrieved_text[:MAX_CONTEXT_SIZE] if len(retrieved_text) > MAX_CONTEXT_SIZE else retrieved_text
    # print("=== Step 4 : Answering the Question ===")
    # Get current date and time
    current_date = datetime.datetime.now().strftime("%B %d, %Y")
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    
    qa_prompt= f"""
    CURRENT DATE: {current_date} at {current_time}
    
    Question: {core_question}
    
    Web search results:
    ===============================
    {retrieved_text}
    ===============================
    
    Instructions:
    1. Give a direct, concise answer
    2. If web search shows clear information: Use it and say "Based on web search"
    3. If web search is unclear: Use your knowledge and say "Based on my knowledge"
    4. Keep it short and to the point
    """
    answer=qa_agent.inference(qa_prompt)
    print(f"answer:{answer}")
    return answer

if __name__ == "__main__":
    jarvis = Jarvis()
    jarvis.run()