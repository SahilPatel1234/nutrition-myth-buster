import streamlit as st
from utils import match_myth, ask_gpt_about_myth

st.title("🥗 Nutrition Myth Buster")
user_input = st.text_input("Enter a nutrition myth you'd like to fact-check:")

if user_input:
    result = match_myth(user_input)  # <-- this is where result is defined

    if result:
        st.markdown(f"### ❌ Myth: {result['claim']}")
        st.markdown(f"**✅ Truth:** {result['explanation']}")
        st.markdown(f"[📖 Source]({result['source']})")
    else:
        st.info("🤔 That myth isn't in our database, but let me check it out for you...")
        gpt_answer = ask_gpt_about_myth(user_input)
        st.markdown(f"### 🤖 GPT says:\n{gpt_answer}")
