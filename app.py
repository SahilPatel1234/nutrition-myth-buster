import streamlit as st
import pandas as pd
import os
import time
from datetime import date
import random
from utils import ask_gpt_about_myth

st.set_page_config(
    page_title="Nutrition Myth Buster",
    page_icon="🥗",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Inject custom CSS to style sidebar background color
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        background-color: #16a34a !important;
        color: white;
        padding: 0 !important;
        margin: 0 !important;
        height: 100vh !important;
    }
    [data-testid="stSidebar"] > div {
        padding: 0 !important;
        margin: 0 !important;
        height: 100vh !important;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    .css-1v3fvcr { 
        padding: 0 !important; 
        margin: 0 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# File paths
SUBMISSIONS_CSV = "data/unreviewed_myths.csv"
UNREVIEWED_CSV = "data/unreviewed_myths.csv"
VOTES_CSV = "data/votes.csv"
MAIN_CSV = "data/nutrition_myths.csv"

# Initialize CSV files if missing or empty
for file, cols in [
    (UNREVIEWED_CSV, ["claim", "truth"]),
    (VOTES_CSV, ["myth", "votes"]),
    (MAIN_CSV, ["claim", "truth"]),
]:
    if not os.path.exists(file) or os.path.getsize(file) == 0:
        pd.DataFrame(columns=cols).to_csv(file, index=False)

# Sidebar top myths
st.sidebar.title("🔥 Top Myths by Community Votes")
votes_df = pd.read_csv(VOTES_CSV)
if not votes_df.empty:
    top_myths = votes_df.sort_values(by="votes", ascending=False).head(5)
    for _, row in top_myths.iterrows():
        st.sidebar.markdown(f"**{row['myth']}**  \n👍 Votes: {row['votes']}")
else:
    st.sidebar.write("No votes yet. Be the first to vote!")

# Custom CSS styling
def local_css():
    st.markdown(
        """
        <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f9fafb; color: #222222; }
        .css-1v3fvcr h1 { color: #2e7d32; font-weight: 700; }
        button { border-radius: 8px !important; border: none !important; background-color: #43a047 !important; color: white !important; padding: 10px 24px !important; font-weight: 600 !important; transition: background-color 0.3s ease; }
        button:hover { background-color: #2e7d32 !important; cursor: pointer; }
        [data-testid="stSidebar"] { background-color: #e8f5e9; padding: 20px; }
        hr { border: none; border-top: 1px solid #c8e6c9; margin: 24px 0; }
        textarea { border-radius: 8px !important; border: 1px solid #a5d6a7 !important; padding: 10px !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )

local_css()

# Navigation
st.sidebar.title("🍎 Navigation")
page = st.sidebar.radio("Go to", ["Myth Buster", "Submit Myth", "Admin Review"])

# Myth of the Day
def get_myth_of_the_day():
    try:
        df = pd.read_csv(MAIN_CSV)
        if df.empty:
            return None, None
        random.seed(str(date.today()))
        row = df.sample(1).iloc[0]
        return row['claim'], row['truth']
    except Exception:
        return None, None

# -------- Page: Myth Buster --------
if page == "Myth Buster":
    st.title("🥗 Nutrition Myth Buster")

    myth, truth = get_myth_of_the_day()
    if myth and truth:
        with st.container():
            st.markdown("### 🌟 Myth of the Day")
            st.markdown(f"**Myth:** {myth}")
            st.markdown(f"**Truth:** {truth}")
            st.markdown("---")

    st.write("Enter a nutrition myth you'd like to check and see what AI thinks!")
    user_input = st.text_input("Nutrition Myth", placeholder="e.g. Carbs make you gain weight")

    if user_input:
        with st.spinner("Checking myth with AI..."):
            answer = ask_gpt_about_myth(user_input)
        st.markdown("### 🧠 AI Fact Check:")
        st.write(answer)

    st.markdown("### 🔎 Browse Existing Myths")
    search_query = st.text_input("Search myths", placeholder="e.g. sugar, eggs, keto...")

    try:
        myths_df = pd.read_csv(MAIN_CSV)
        if not myths_df.empty:
            filtered = myths_df[myths_df["claim"].str.contains(search_query, case=False, na=False)] if search_query else myths_df
            for _, row in filtered.iterrows():
                with st.expander(f"❓ {row['claim']}"):
                    st.markdown(f"✅ **Truth:** {row['truth']}")
        else:
            st.info("No reviewed myths available yet.")
    except Exception as e:
        st.error(f"Error loading myths: {e}")

    votes_df = pd.read_csv(VOTES_CSV)
    match = votes_df[votes_df["myth"] == user_input]
    current_votes = int(match["votes"].values[0]) if not match.empty else 0

    vote_placeholder = st.empty()
    vote_placeholder.markdown(f"**Current Votes:** {current_votes}")

    col1, col2 = st.columns(2)
    if "voted" not in st.session_state:
        st.session_state.voted = {}

    def animate_votes(start, end):
        step = 1 if end > start else -1
        for v in range(start, end + step, step):
            vote_placeholder.markdown(f"**Current Votes:** {v}")
            time.sleep(0.05)

    with col1:
        if st.button("👍 Upvote") and not st.session_state.voted.get(user_input):
            new_votes = current_votes + 1
            if match.empty:
                new_row = pd.DataFrame([{"myth": user_input, "votes": new_votes}])
                votes_df = pd.concat([votes_df, new_row], ignore_index=True)
            else:
                votes_df.loc[votes_df["myth"] == user_input, "votes"] = new_votes
            votes_df.to_csv(VOTES_CSV, index=False)
            st.session_state.voted[user_input] = True
            animate_votes(current_votes, new_votes)
            st.experimental_rerun()

    with col2:
        if st.button("👎 Downvote") and not st.session_state.voted.get(user_input):
            new_votes = current_votes - 1
            if match.empty:
                new_row = pd.DataFrame([{"myth": user_input, "votes": new_votes}])
                votes_df = pd.concat([votes_df, new_row], ignore_index=True)
            else:
                votes_df.loc[votes_df["myth"] == user_input, "votes"] = new_votes
            votes_df.to_csv(VOTES_CSV, index=False)
            st.session_state.voted[user_input] = True
            animate_votes(current_votes, new_votes)
            st.experimental_rerun()

    st.markdown("---")

# -------- Page: Submit Myth --------
elif page == "Submit Myth":
    st.title("📩 Submit a New Myth for Review")
    with st.form("submit_myth_form"):
        new_myth = st.text_input("New Myth", help="Describe the myth you want to submit.")
        correction = st.text_area("Correction or Explanation (optional)", help="Add a brief correction or explanation if you want.")
        submitted = st.form_submit_button("Submit Myth")
        if submitted:
            if new_myth:
                df = pd.read_csv(UNREVIEWED_CSV)
                df = pd.concat([
                    df,
                    pd.DataFrame([{"claim": new_myth, "truth": correction or "To be reviewed"}])
                ], ignore_index=True)
                df.to_csv(UNREVIEWED_CSV, index=False)
                st.success("✅ Your myth has been submitted for review!")
            else:
                st.error("Please enter a myth before submitting.")

# -------- Page: Admin Review --------
else:
    st.title("🔐 Admin Review Submitted Myths")
    password = st.text_input("Enter admin password", type="password")
    if password != "Broncos2006!":
        st.warning("🔐 Enter the correct password to view unreviewed myths.")
    else:
        unreviewed = pd.read_csv(UNREVIEWED_CSV)
        if unreviewed.empty:
            st.success("🎉 No myths pending review!")
        else:
            for i, row in unreviewed.iterrows():
                with st.container():
                    st.markdown(f"**Myth:** {row['claim']}")
                    st.markdown(f"**Correction:** {row['truth']}")
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(f"✅ Approve {i}", key=f"approve_{i}"):
                            approved = pd.read_csv(MAIN_CSV)
                            approved = pd.concat([approved, pd.DataFrame([row])], ignore_index=True)
                            approved.to_csv(MAIN_CSV, index=False)
                            unreviewed.drop(index=i, inplace=True)
                            unreviewed.to_csv(UNREVIEWED_CSV, index=False)
                            st.success("✅ Myth approved and added.")
                            st.experimental_rerun()
                    with col2:
                        if st.button(f"❌ Reject {i}", key=f"reject_{i}"):
                            unreviewed.drop(index=i, inplace=True)
                            unreviewed.to_csv(UNREVIEWED_CSV, index=False)
                            st.warning("❌ Myth rejected.")
                            st.experimental_rerun()
                st.markdown("---")
