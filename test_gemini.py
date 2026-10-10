import os
from dotenv import load_dotenv
from google import genai

# Load .env
load_dotenv()

# Get API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("ERROR: GEMINI_API_KEY not found")
    exit()

# Create Gemini client
client = genai.Client(api_key=api_key)

print("Connecting to Gemini...")

# Send request using the current Interactions API
interaction = client.interactions.create(
    model="gemini-3.8-flash",
    input="Hello Gemini! Give me a one-line introduction."
)

print("\nGemini Response:")
print(interaction.output_text)