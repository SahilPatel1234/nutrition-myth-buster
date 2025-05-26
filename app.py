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

st.markdown("---")
st.markdown("💡 *Want to help improve this app?*")
new_myth = st.text_input("Submit a new myth you'd like us to investigate:")

if st.button("Submit Myth"):
    if new_myth:
        with open("data/user_submitted_myths.txt", "a") as f:
            f.write(new_myth + "\n")
        st.success("✅ Thanks! We’ve received your suggestion.")
    else:
        st.warning("Please enter a myth before submitting.")
