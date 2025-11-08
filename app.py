import streamlit as st
import json
import tempfile
from parser import parse_and_save  # reuse your existing parser

st.set_page_config(page_title="Credit Card Statement Parser", layout="centered")

st.title("💳 Credit Card Statement Parser")
st.markdown("Upload a credit card statement PDF to extract key details automatically.")

uploaded_file = st.file_uploader("Upload your PDF file", type=["pdf"])

if uploaded_file is not None:
    # Save the uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name

    st.info("Processing your PDF... please wait ⏳")

    # Call your parser
    result = parse_and_save(tmp_path)

    st.success("✅ Extraction complete!")

    # Show the results in a neat format
    st.subheader("Extracted Data:")
    st.json(result)

    # Optionally, offer a download of the result
    st.download_button(
        label="Download Extracted JSON",
        data=json.dumps(result, indent=2),
        file_name="extracted_data.json",
        mime="application/json"
    )
