import openai
import os
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_chatbot_response(messages, model="gpt-3.5-turbo"):
    from openai import OpenAI
    client = OpenAI()
    suggestion_prompt = {
        "role": "system",
        "content": "You are a helpful customer support assistant. Based on the user's last message, suggest 3 relevant actions or questions they might want help with. Reply ONLY with a numbered list of suggestions, no extra text."
    }
    prompt_messages = [suggestion_prompt] + messages
    response = client.chat.completions.create(
        model=model,
        messages=prompt_messages,
        max_tokens=256,
        temperature=0.7
    )
    return response.choices[0].message.content
