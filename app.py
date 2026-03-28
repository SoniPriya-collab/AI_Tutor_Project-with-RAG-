import streamlit as st
from rag_pipeline import process_pdf, ask_question

st.set_page_config(page_title="AI Tutor", layout="centered")

st.title("📚 AI Tutor")

uploaded_file = st.file_uploader("Upload PDF", type="pdf")

# Process PDF
if uploaded_file:
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.read())

    st.success("PDF uploaded successfully!")

    if "db" not in st.session_state:
        try:
            with st.spinner("Processing PDF..."):
                st.session_state.db = process_pdf("temp.pdf")
            st.success("File processed successfully!")
        except Exception as e:
            st.error(f"Error processing PDF: {e}")

# Always show input box
query = st.text_input("Ask a question")

if query:
    if "db" in st.session_state:
        try:
            with st.spinner("Thinking..."):
                answer = ask_question(st.session_state.db, query)

            st.markdown("### ✅ Answer")
            st.write(answer)

        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please upload and process a PDF first.")