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
