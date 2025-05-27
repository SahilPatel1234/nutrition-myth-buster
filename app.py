import streamlit as st
from utils import ask_gpt_about_myth
import pandas as pd
import os

st.set_page_config(page_title="Nutrition Myth Buster", page_icon="🥗")

st.title("🥗 Nutrition Myth Buster")
st.write("Enter a nutrition myth you'd like to check:")

# --- Myth checking section ---
user_input = st.text_input("Nutrition Myth", placeholder="e.g. Carbs make you gain weight")

if user_input:
    with st.spinner("Checking myth with AI..."):
        answer = ask_gpt_about_myth(user_input)
    st.markdown("### 🧠 AI Fact Check:")
    st.write(answer)

st.markdown("---")

# --- Submit your own myth ---
st.subheader("📩 Submit a New Myth for the Database")

with st.form("submit_myth"):
    new_myth = st.text_input("New Myth")
    correction = st.text_area("Correction or Explanation (optional)")
    submitted = st.form_submit_button("Submit")

    if submitted and new_myth:
        df_path = "data/nutrition_myths.csv"
        
        # Make sure the CSV exists
        if not os.path.exists(df_path):
            df = pd.DataFrame(columns=["claim", "truth"])
        else:
            df = pd.read_csv(df_path)

        # Add new entry
        new_entry = {"claim": new_myth, "truth": correction if correction else "To be reviewed"}
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)

        # Save updated file
        df.to_csv(df_path, index=False)
        st.success("✅ Your myth has been submitted!")
