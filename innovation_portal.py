import streamlit as st
import pandas as pd

st.set_page_config(page_title="Innovation Portal", layout="centered")

st.title("💡 Innovation Portal")

# ---- Form for submitting ideas ----
st.header("Submit a New Idea")
with st.form("idea_form"):
    name = st.text_input("Your Name")
    title = st.text_input("Idea Title")
    description = st.text_area("Describe your idea")
    category = st.selectbox("Category", ["Technology", "Operations", "HR", "Customer Experience", "Other"])
    submitted = st.form_submit_button("Submit Idea")

    if submitted:
        st.success(f"✅ Idea '{title}' submitted by {name}!")

# ---- Display example ideas ----
st.header("Browse Submitted Ideas")
data = {
    "Title": ["Smart AI Assistant", "Eco-friendly Packaging"],
    "Category": ["Technology", "Operations"],
    "Submitted By": ["Alice", "Bob"],
    "Status": ["Under Review", "Approved"],
    "Votes": [10, 25]
}
df = pd.DataFrame(data)
st.dataframe(df)
