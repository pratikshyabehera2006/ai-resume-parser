import streamlit as st
from parser import parse_resume

st.set_page_config(page_title="AI Resume Parser", layout="wide")

st.title("📄 AI Resume Parser")

# Sidebar
st.sidebar.header("📌 Instructions")
st.sidebar.write("1. Upload Resume")
st.sidebar.write("2. View Results")

uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

if uploaded_file:
    with st.spinner("Processing Resume..."):
        result = parse_resume(uploaded_file)

    st.success("✅ Resume Processed Successfully!")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📌 Basic Information")
        st.write(f"**Name:** {result['Name']}")
        st.write(f"**Email:** {result['Email']}")
        st.write(f"**Phone:** {result['Phone']}")

    with col2:
        st.subheader("🛠 Skills")
        st.write(", ".join(result['Skills']))

    # Education
    st.subheader("🎓 Education")
    for edu in result["Education"]:
        st.write("- " + edu)