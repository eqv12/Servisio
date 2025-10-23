import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load the .env file to get the API key
load_dotenv()

print("Attempting to list available Gemini models...")

try:
    # Configure the SDK with your key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in .env file.")
    else:
        genai.configure(api_key=api_key)

        print("\n--- Models Supporting 'generateContent' ---")
        
        # List all models and filter for the one we need
        for model in genai.list_models():
            if 'generateContent' in model.supported_generation_methods:
                print(f"- {model.name}")
                
        print("\n-------------------------------------------")
        print("Check the list above for a suitable model name.")

except Exception as e:
    print(f"\nAn error occurred while trying to connect to the API: {e}")