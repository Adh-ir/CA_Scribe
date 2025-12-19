import os
import sys
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
print(f"Checking Groq Key: {api_key[:4]}...{api_key[-4:] if api_key else 'None'}")

if not api_key or api_key == "deprecated":
    print("Groq API Key is missing or marked as deprecated.")
    sys.exit(1)

client = Groq(api_key=api_key)

try:
    print("Attempting simple Groq request...")
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Say hello",
            }
        ],
        model="llama-3.3-70b-versatile",
    )
    print("Success! Groq responded:")
    print(chat_completion.choices[0].message.content)
except Exception as e:
    print("Groq Request Failed!")
    print(f"Error Type: {type(e).__name__}")
    print(f"Error Message: {e}")
