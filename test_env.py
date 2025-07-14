from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

# Get the value of your OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")

# Print it
if api_key:
    print("✅ .env loaded successfully!")
    print("Your OpenAI API Key is:", api_key)
else:
    print("❌ Failed to load API key. Check .env file.")
