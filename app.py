import streamlit as st
from utils import match_myth

st.title("🧠 Nutrition Myth Buster")
user_input = st.text_input("Enter a nutrition claim you'd like to verify:")

if user_input:
    result = match_myth(user_input)
    if result:
        st.markdown(f"**Verdict:** {result['truth_label']}")
        st.markdown(f"**Explanation:** {result['explanation']}")
        st.markdown(f"🔗 [Source]({result['source']})")
    else:
        st.warning("Sorry, I couldn't find that myth in my database.")
