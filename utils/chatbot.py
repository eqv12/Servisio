"""
chatbot.py - ITIL Helpdesk Chatbot for Servisio (Fixed Version)

Purpose:
    Provides a conversational ITIL support assistant
    using Google GenAI (Gemini) with correct API usage.
"""

import os
from google import genai

# Initialize client
client = genai.Client(api_key="AIzaSyDXx788ps8Ze3mnB7i7nqK8go6HFNDDta8")

SYSTEM_PROMPT = """
You are ServisioBot, an IT Service Desk Assistant.
You help employees report incidents, understand ITIL concepts,
and check ticket-related details in a friendly and clear manner.

Capabilities:
- Help users report incidents (ask title, category, and priority)
- Explain ITIL processes (incident, problem, change, SLA)
- Provide short and meaningful answers
- Ask clarifying questions when needed
"""

def ask_chatbot(message: str) -> str:
    """
    Sends the user's message to Google GenAI and returns the bot reply.
    """
    try:
        # Combine system prompt + user message into one string
        prompt = f"{SYSTEM_PROMPT}\nUser: {message}\nServisioBot:"
        
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        print("[Chatbot] Error:", e)
        return "I'm sorry, I'm having trouble responding right now."

print(ask_chatbot("what category does the incident 'Virtual Machine installation problem' comes under?"))