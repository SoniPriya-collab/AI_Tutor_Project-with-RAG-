from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv
import os

load_dotenv()

def process_pdf(file_path):
    loader = PyPDFLoader(file_path)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(docs)

    embeddings = OpenAIEmbeddings()

    db = Chroma.from_documents(
        chunks,
        embeddings,
        persist_directory="db"
    )

    return db


def ask_question(db, query):
    docs = db.similarity_search(query, k=3)
    context = "\n".join([doc.page_content for doc in docs])

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )

    prompt = f"""
You are a helpful tutor.
Answer ONLY from the context below.

Context:
{context}

Question:
{query}
"""

    response = llm.invoke(prompt)
    return response.content