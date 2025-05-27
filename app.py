import streamlit as st
from utils import ask_gpt_about_myth

st.set_page_config(page_title="Nutrition Myth Buster", page_icon="🥗")

st.title("🥗 Nutrition Myth Buster")
st.write("Enter a nutrition myth you'd like to check:")

user_input = st.text_input("")

if user_input:
    with st.spinner("Checking myth with AI..."):
        answer = ask_gpt_about_myth(user_input)
    st.markdown("### AI Fact Check:")
    st.write(answer)
