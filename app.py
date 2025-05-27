import streamlit as st
import pandas as pd
import os
from utils import ask_gpt_about_myth

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

# Custom CSS for styling
def local_css():
    st.markdown(
        """
        <style>
        /* General */
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f9fafb;
            color: #222222;
        }
        /* Header */
        .css-1v3fvcr h1 {
            color: #2e7d32;
            font-weight: 700;
        }
        /* Buttons */
        button {
            border-radius: 8px !important;
            border: none !important;
            background-color: #43a047 !important;
            color: white !important;
            padding: 10px 24px !important;
            font-weight: 600 !important;
            transition: background-color 0.3s ease;
        }
        button:hover {
            background-color: #2e7d32 !important;
            cursor: pointer;
        }
        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: #e8f5e9;
            padding: 20px;
        }
        /* Separator */
        hr {
            border: none;
            border-top: 1px solid #c8e6c9;
            margin: 24px 0;
        }
        /* Textarea */
        textarea {
            border-radius: 8px !important;
            border: 1px solid #a5d6a7 !important;
            padding: 10px !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

local_css()

st.set_page_config(
    page_title="Nutrition Myth Buster",
    page_icon="🥗",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Sidebar navigation menu
st.sidebar.title("🍎 Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Myth Buster", "Submit Myth", "Admin Review"],
)

# -------- Page: Myth Buster --------
if page == "Myth Buster":
    st.title("🥗 Nutrition Myth Buster")
    st.write(
        "Enter a nutrition myth you'd like to check and see what AI thinks!"
    )

    user_input = st.text_input("Nutrition Myth", placeholder="e.g. Carbs make you gain weight")

    if user_input:
        with st.spinner("Checking myth with AI..."):
            answer = ask_gpt_about_myth(user_input)

        st.markdown("### 🧠 AI Fact Check:")
        st.write(answer)

        # Voting system
        votes_df = pd.read_csv(VOTES_CSV)
        match = votes_df[votes_df["myth"] == user_input]
        current_votes = int(match["votes"].values[0]) if not match.empty else 0

        st.markdown(f"**Current Votes:** {current_votes}")

        col1, col2 = st.columns(2)
        if "voted" not in st.session_state:
            st.session_state.voted = {}

        with col1:
            if st.button("👍 Upvote"):
                if not st.session_state.voted.get(user_input):
                    if match.empty:
                        new_row = pd.DataFrame([{"myth": user_input, "votes": 1}])
                        votes_df = pd.concat([votes_df, new_row], ignore_index=True)
                    else:
                        votes_df.loc[votes_df["myth"] == user_input, "votes"] += 1
                    st.session_state.voted[user_input] = True
                    votes_df.to_csv(VOTES_CSV, index=False)
                    st.experimental_rerun()

        with col2:
            if st.button("👎 Downvote"):
                if not st.session_state.voted.get(user_input):
                    if match.empty:
                        new_row = pd.DataFrame([{"myth": user_input, "votes": -1}])
                        votes_df = pd.concat([votes_df, new_row], ignore_index=True)
                    else:
                        votes_df.loc[votes_df["myth"] == user_input, "votes"] -= 1
                    st.session_state.voted[user_input] = True
                    votes_df.to_csv(VOTES_CSV, index=False)
                    st.experimental_rerun()

        st.markdown("---")

# -------- Page: Submit Myth --------
elif page == "Submit Myth":
    st.title("📩 Submit a New Myth for Review")

    with st.form("submit_myth_form"):
        new_myth = st.text_input("New Myth", help="Describe the myth you want to submit.")
        correction = st.text_area(
            "Correction or Explanation (optional)",
            help="Add a brief correction or explanation if you want."
        )
        submitted = st.form_submit_button("Submit Myth")

        if submitted:
            if new_myth:
                df = pd.read_csv(UNREVIEWED_CSV)
                df = pd.concat(
                    [
                        df,
                        pd.DataFrame(
                            [{"claim": new_myth, "truth": correction or "To be reviewed"}]
                        ),
                    ],
                    ignore_index=True,
                )
                df.to_csv(UNREVIEWED_CSV, index=False)
                st.success("✅ Your myth has been submitted for review!")
            else:
                st.error("Please enter a myth before submitting.")

# -------- Page: Admin Review --------
else:
    st.title("🔐 Admin Review Submitted Myths")

    password = st.text_input("Enter admin password", type="password")
    if password != "Broncos2006!":
        st.warning("🔒 Enter the correct password to view unreviewed myths.")
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
