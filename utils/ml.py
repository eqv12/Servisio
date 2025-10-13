"""
ml.py - Machine Learning Utilities (Google GenAI version)

Purpose:
    Uses Google Generative AI (Gemini) to predict incident category
    and priority based on ticket title or description.
"""

import os
from google import genai

client = genai.Client(api_key="AIzaSyDXx788ps8Ze3mnB7i7nqK8go6HFNDDta8") #GEMINI API KEY

# Define prompt templates
CATEGORY_PROMPT = """
You are an expert IT service desk assistant.
Given a short issue title, classify it into one of these categories:
- Network
- Hardware
- Software
- Access
- Other

Title: "{title}"
Answer with only the category name.
"""

PRIORITY_PROMPT = """
You are an IT ticket triage expert.
Given an issue title, predict its priority level as one of:
- Low
- Medium
- High

Title: "{title}"
Answer with only the priority level.
"""


def predict_category(title: str) -> str:
    """
    Predicts incident category using Google GenAI.
    Falls back to 'Other' on API failure.
    """
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[CATEGORY_PROMPT.format(title=title)]
        )
        text = response.text.strip()
        return text if text in ["Network", "Hardware", "Software", "Access", "Other"] else "Other"
    except Exception as e:
        print("[ML] Warning: Category prediction failed →", e)
        return "Other"


def predict_priority(title: str) -> str:
    """
    Predicts incident priority using Google GenAI.
    Falls back to 'Medium' on API failure.
    """
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[PRIORITY_PROMPT.format(title=title)]
        )
        text = response.text.strip()
        return text if text in ["Low", "Medium", "High"] else "Medium"
    except Exception as e:
        print("[ML] Warning: Priority prediction failed →", e)
        return "Medium"


def forecast_ticket_load(days: int = 7):
    """
    Dummy dashboard projection for future ticket load.
    (Can later be replaced with a time-series model)
    """
    return {
        "labels": [f"Day {i + 1}" for i in range(days)],
        "values": [10 + i * 2 for i in range(days)]
    }
    