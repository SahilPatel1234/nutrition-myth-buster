import openai
import os

openai.api_key = os.getenv("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")

def ask_gpt_about_myth(user_input):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Or "gpt-4" if your key has access
            messages=[
                {"role": "system", "content": "You are a helpful nutrition expert. Respond to myths with scientifically accurate explanations, being kind, empathetic, and informative."},
                {"role": "user", "content": f"Is this myth true or false: '{user_input}'? Explain your answer in simple terms with scientific reasoning."}
            ],
            temperature=0.6,
            max_tokens=300
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Sorry, I couldn’t fetch an answer from GPT right now. Error: {e}"


import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv("data/nutrition_myths.csv")

def match_myth(user_input):
    vectorizer = TfidfVectorizer().fit_transform([user_input] + df['claim'].tolist())
    similarity = cosine_similarity(vectorizer[0:1], vectorizer[1:]).flatten()
    best_match_index = similarity.argmax()

    if similarity[best_match_index] > 0.4:
        return df.iloc[best_match_index].to_dict()
    return None
