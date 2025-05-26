import streamlit as st
from utils import match_myth, ask_gpt_about_myth

# --- Page setup ---
st.set_page_config(
    page_title="Nutrition Myth Buster",
    page_icon="🥗",
    layout="centered"
)

# --- Sidebar ---
st.sidebar.title("📘 About")
st.sidebar.markdown(
    """
    Welcome to the Nutrition Myth Buster!  
    This AI-powered app helps fact-check popular nutrition myths based on reliable sources.  
      
    🔎 Enter a myth below to check it.  
    💬 Submit new myths to help improve the app.  
    """
)

# --- App Title & Intro ---
st.title("🥗 Nutrition Myth Buster")
st.markdown("Enter a nutrition myth you'd like to fact-check:")

# --- User Input ---
user_input = st.text_input("")

if user_input:
    # Try to match myth in database
    result = match_myth(user_input)

    if result:
        st.error(f"❌ Myth: {result['claim']}")
        st.success(f"✅ Truth: {result['explanation']}")
        st.markdown(f"[📖 Source]({result['source']})")
    else:
        st.info("🤔 That myth isn't in our database, but let me check it out for you...")
        gpt_answer = ask_gpt_about_myth(user_input)
        with st.expander("🤖 GPT Explanation"):
            st.markdown(gpt_answer)

st.markdown("---")

# --- User Myth Submission ---
st.markdown("💡 *Want to help improve this app?*")
new_myth = st.text_input("Submit a new myth you'd like us to investigate:")

if st.button("Submit Myth"):
    if new_myth.strip():
        with open("data/user_submitted_myths.txt", "a") as f:
            f.write(new_myth.strip() + "\n")
        st.success("✅ Thanks! We’ve received your suggestion.")
    else:
        st.warning("Please enter a myth before submitting.")
