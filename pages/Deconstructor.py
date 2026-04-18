import streamlit as st
from dotenv import load_dotenv

# ---- CONFIG ----
st.set_page_config(page_title="Research Paper Deconstructor", layout="wide")

load_dotenv()

# ---- IMPORTS ----
from deconstructor.ingestion import ingest_pdfs
from deconstructor.retriever import retrieve
from deconstructor.memory import build_memory
from deconstructor.database import (
    create_session,
    load_messages,
    save_message,
    list_sessions,
    delete_session,
    delete_messages_by_session,
)

st.title("Research Paper Deconstructor")

# ---- SESSION STATE ----
if "session_id" not in st.session_state:
    st.session_state.session_id = create_session()

if "memory" not in st.session_state:
    st.session_state.memory = build_memory([])

if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None


# ---- SIDEBAR ----
with st.sidebar:
    st.subheader("Chats")

    # ➕ New Chat
    if st.button("➕ New Chat", use_container_width=True):
        st.session_state.session_id = create_session()
        st.session_state.memory = build_memory([])
        st.session_state.vectorstore = None
        st.rerun()

    st.divider()

    # 📂 Existing Chats
    for s in list_sessions():
        col1, col2 = st.columns([4, 1])

        # Highlight current session
        label = "👉 " + s["name"] if s["id"] == st.session_state.session_id else s["name"]

        # Select chat
        with col1:
            if st.button(
                label,
                key=f"session_{s['id']}",
                use_container_width=True,
            ):
                st.session_state.session_id = s["id"]
                st.session_state.memory = build_memory(load_messages(s["id"]))
                st.session_state.vectorstore = None
                st.rerun()

        # Delete chat
        with col2:
            if st.button("❌", key=f"delete_{s['id']}"):
                delete_session(s["id"])

                # If current session deleted → create new one
                if s["id"] == st.session_state.session_id:
                    st.session_state.session_id = create_session()
                    st.session_state.memory = build_memory([])
                    st.session_state.vectorstore = None

                st.rerun()

    st.divider()

    # 🧹 Clear Current Chat
    if st.button("🧹 Clear Current Chat", use_container_width=True):
        delete_messages_by_session(st.session_state.session_id)
        st.session_state.memory = build_memory([])
        st.session_state.vectorstore = None
        st.rerun()


# ---- FILE UPLOAD ----
uploaded_files = st.file_uploader(
    "Upload research papers (PDF)",
    type=["pdf"],
    accept_multiple_files=True,
)

if uploaded_files:
    from shared.embeddings import get_embeddings
    from shared.config import CHROMA_PERSIST_DIR
    from langchain_community.vectorstores import Chroma
    import tempfile
    import os

    vectorstore = Chroma(
        collection_name=st.session_state.session_id,
        persist_directory=str(CHROMA_PERSIST_DIR),
        embedding_function=get_embeddings(),
    )

    # Save uploaded files temporarily
    files = []
    for f in uploaded_files:
        path = os.path.join(tempfile.gettempdir(), f.name)
        with open(path, "wb") as out:
            out.write(f.getvalue())
        files.append({
            "path": path,
            "filename": f.name,
            "source": "upload"
        })

    ingest_pdfs(vectorstore, st.session_state.session_id, files)
    st.session_state.vectorstore = vectorstore

    st.success("Documents processed")


# ---- CHAT HISTORY ----
messages = load_messages(st.session_state.session_id)

for msg in messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# ---- CHAT INPUT ----
question = st.chat_input("Ask a question about the documents")

if question:
    if st.session_state.vectorstore is None:
        st.warning("Please upload and process a PDF first.")
        st.stop()

    # Save user message
    save_message(st.session_state.session_id, "user", question)

    with st.chat_message("user"):
        st.markdown(question)

    # Retrieve context
    docs = retrieve(
        st.session_state.vectorstore,
        st.session_state.session_id,
        question
    )

    context = "\n\n".join(d.page_content for d in docs)

    # Generate answer
    from deconstructor.llm import ask

    answer = ask(
        f"Context:\n{context}\n\nQuestion:\n{question}\nAnswer:"
    )

    # Save assistant response
    save_message(st.session_state.session_id, "assistant", answer)

    with st.chat_message("assistant"):
        st.markdown(answer)