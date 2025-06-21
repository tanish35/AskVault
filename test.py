from google import genai
from lib.config import settings

client = genai.Client(api_key=settings.google_api_key)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Explain how AI works in a few words",
)

print(response.text)
