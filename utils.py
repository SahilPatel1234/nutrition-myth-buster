import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")  # Make sure to set this in your environment

def ask_gpt_about_myth(user_input):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or "gpt-4" if available
            messages=[
                {"role": "system", "content": "You are a kind and knowledgeable nutrition expert."},
                {"role": "user", "content": f"Is this nutrition myth true or false: '{user_input}'? Please explain clearly with scientific reasoning."}
            ],
            temperature=0.6,
            max_tokens=300
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Sorry, I couldn't fetch an answer from GPT right now. Error: {e}"
