import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Innovation Portal", layout="centered")
st.title("💡 Innovation Portal")

CSV_FILE = "ideas.csv"

# ---- Initialize CSV file if it doesn't exist ----
if not os.path.exists(CSV_FILE):
    df_init = pd.DataFrame(columns=["Name", "Title", "Description", "Category"])
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
            new_row = pd.DataFrame([[name, title, description, category]],
                                   columns=["Name", "Title", "Description", "Category"])
            new_row.to_csv(CSV_FILE, mode='a', header=False, index=False)
            st.success(f"✅ Idea '{title}' submitted by {name}!")
            st.rerun()  # ✅ Correct method to refresh app
        else:
            st.error("⚠️ Please fill out all fields.")

# ---- Display submitted ideas ----
st.header("📋 Browse Submitted Ideas")
try:
    ideas_df = pd.read_csv(CSV_FILE)
    st.dataframe(ideas_df, use_container_width=True)
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
