import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt

st.set_page_config(page_title="Innovation Portal", layout="centered")

CSV_FILE = "ideas.csv"
VOTES_FILE = "votes.csv"

# ---- Simple User Authentication ----
USERS = {
    "alice": "password123",
    "bob": "secret456"
}

def login():
    st.title("🔐 Login to Innovation Portal")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in USERS and USERS[username] == password:
            st.session_state["logged_in"] = True
            st.session_state["user"] = username
            st.success("✅ Login successful!")
            st.rerun()
        else:
            st.error("❌ Invalid username or password")

# ---- First-time login check ----
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login()
    st.stop()

# ---- Innovation Portal Main App ----
st.title("💡 Innovation Portal")
st.write(f"👋 Welcome, **{st.session_state['user']}**")

# ---- Initialize CSV files if not exist ----
if not os.path.exists(CSV_FILE):
    df_init = pd.DataFrame(columns=["Name", "Title", "Description", "Category", "Votes"])
    df_init = df_init.astype({"Votes": "int"})
    df_init.to_csv(CSV_FILE, index=False)

if not os.path.exists(VOTES_FILE):
    votes_init = pd.DataFrame(columns=["Username", "IdeaTitle"])
    votes_init.to_csv(VOTES_FILE, index=False)

# ---- Idea submission form ----
st.header("📝 Submit a New Idea")
with st.form("idea_form"):
    name = st.text_input("Your Name")
    title = st.text_input("Idea Title")
    description = st.text_area("Describe your idea")
    category = st.selectbox("Category", ["Technology", "Operations", "HR", "Customer Experience", "Other"])
    submitted = st.form_submit_button("Submit Idea")

    if submitted:
        if name and title and description:
            new_row = pd.DataFrame([[name, title, description, category, 0]],
                                   columns=["Name", "Title", "Description", "Category", "Votes"])
            new_row["Votes"] = new_row["Votes"].astype(int)
            new_row.to_csv(CSV_FILE, mode='a', header=False, index=False)
            st.success(f"✅ Idea '{title}' submitted by {name}!")
            st.rerun()
        else:
            st.error("⚠️ Please fill out all fields.")

# ---- Load ideas and votes ----
ideas_df = pd.read_csv(CSV_FILE)
ideas_df["Votes"] = pd.to_numeric(ideas_df["Votes"], errors="coerce").fillna(0).astype(int)
votes_df = pd.read_csv(VOTES_FILE)

# ---- Filters ----
st.header("📋 Browse Submitted Ideas")
st.subheader("🔎 Filter Ideas")
search_keyword = st.text_input("Search by keyword (title or description)")
category_filter = st.selectbox("Filter by category", ["All"] + sorted(ideas_df["Category"].unique()))

filtered_df = ideas_df.copy()
if search_keyword:
    keyword = search_keyword.lower()
    filtered_df = filtered_df[
        filtered_df["Title"].str.lower().str.contains(keyword) |
        filtered_df["Description"].str.lower().str.contains(keyword)
    ]
if category_filter != "All":
    filtered_df = filtered_df[filtered_df["Category"] == category_filter]

# ---- Show ideas and vote buttons ----
if filtered_df.empty:
    st.info("No ideas match your search.")
else:
    for idx, row in filtered_df.iterrows():
        with st.expander(f"💡 {row['Title']} by {row['Name']}"):
            st.write(f"**Category:** {row['Category']}")
            st.write(row['Description'])
            st.write(f"👍 **Votes:** {row['Votes']}")

            # Check if user already voted for this idea
            has_voted = not votes_df[
                (votes_df["Username"] == st.session_state["user"]) &
                (votes_df["IdeaTitle"] == row["Title"])
            ].empty

            if has_voted:
                st.info("✅ You have already voted for this idea.")
            else:
                vote_btn = st.button(f"Vote for '{row['Title']}'", key=f"vote_{idx}")
                if vote_btn:
                    # Update votes
                    ideas_df.loc[ideas_df["Title"] == row["Title"], "Votes"] += 1
                    ideas_df.to_csv(CSV_FILE, index=False)

                    # Add vote record
                    new_vote = pd.DataFrame([[st.session_state["user"], row["Title"]]],
                                             columns=["Username", "IdeaTitle"])
                    new_vote.to_csv(VOTES_FILE, mode="a", header=False, index=False)

                    st.success("✅ Your vote has been recorded!")
                    st.rerun()

# ---- Analytics Dashboard ----
st.header("📊 Analytics Dashboard")
if not ideas_df.empty:
    # Top categories
    category_counts = ideas_df["Category"].value_counts()
    st.subheader("Top Categories by Number of Ideas")
    fig1, ax1 = plt.subplots()
    category_counts.plot(kind="bar", ax=ax1, color="skyblue")
    ax1.set_xlabel("Category")
    ax1.set_ylabel("Number of Ideas")
    ax1.set_title("Number of Ideas per Category")
    st.pyplot(fig1)

    # Most voted ideas
    top_voted = ideas_df.sort_values(by="Votes", ascending=False).head(5)
    st.subheader("Top 5 Most Voted Ideas")
    fig2, ax2 = plt.subplots()
    ax2.barh(top_voted["Title"], top_voted["Votes"], color="green")
    ax2.set_xlabel("Votes")
    ax2.set_title("Top 5 Most Voted Ideas")
    ax2.invert_yaxis()
    st.pyplot(fig2)
else:
    st.info("No data available for analytics.")

# ---- Download ideas.csv ----
with open(CSV_FILE, "rb") as file:
    st.download_button(
        label="📥 Download All Ideas (CSV)",
        data=file,
        file_name="ideas.csv",
        mime="text/csv"
    )
