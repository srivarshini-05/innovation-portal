import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Innovation Portal", layout="centered")

CSV_FILE = "ideas.csv"

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

# ---- Initialize CSV file if not exists ----
if not os.path.exists(CSV_FILE):
    df_init = pd.DataFrame(columns=["Name", "Title", "Description", "Category", "Votes"])
    df_init.to_csv(CSV_FILE, index=False)

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
            new_row.to_csv(CSV_FILE, mode='a', header=False, index=False)
            st.success(f"✅ Idea '{title}' submitted by {name}!")
            st.rerun()
        else:
            st.error("⚠️ Please fill out all fields.")

# ---- Display submitted ideas with voting ----
st.header("📋 Browse Submitted Ideas")

try:
    ideas_df = pd.read_csv(CSV_FILE)

    for idx, row in ideas_df.iterrows():
        with st.expander(f"💡 {row['Title']} by {row['Name']}"):
            st.write(f"**Category:** {row['Category']}")
            st.write(row['Description'])
            st.write(f"👍 **Votes:** {row['Votes']}")

            vote_btn = st.button(f"Vote for '{row['Title']}'", key=f"vote_{idx}")
            if vote_btn:
                ideas_df.at[idx, "Votes"] += 1
                ideas_df.to_csv(CSV_FILE, index=False)
                st.success("✅ Vote recorded!")
                st.rerun()

except Exception as e:
    st.error("Error loading ideas.")
    st.text(str(e))

# ---- Download ideas.csv ----
with open(CSV_FILE, "rb") as file:
    st.download_button(
        label="📥 Download All Ideas (CSV)",
        data=file,
        file_name="ideas.csv",
        mime="text/csv"
    )
