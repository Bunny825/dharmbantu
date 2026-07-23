# Dharmbantu — Indian Law Assistant

Dharmbantu is a generative-AI legal assistant that answers questions about Indian law using
**retrieval-augmented generation (RAG)** over official legal documents — returning grounded answers
with citations, and without hallucinating sections.

**Covers:** Bharatiya Nyaya Sanhita (BNS), Bharatiya Nagarik Suraksha Sanhita (BNSS),
Bharatiya Sakshya Adhiniyam (BSA), and the Code of Civil Procedure (CPC).

## Features

- Context-aware answers via RAG, with accurate section/act citations grounded **only** in official
  text (no hallucination).
- Automated ingestion — scrapes and parses acts from [indiacode.nic.in](https://indiacode.nic.in).
- AstraDB-backed vector search and persistent chat history.
- History-aware retrieval (query reformulation) with an **MMR** retriever for diverse, relevant
  context.
- Conversational Streamlit interface.

## How It Works

1. **Ingestion** — acts are scraped from IndiaCode (BeautifulSoup), parsed, split into chunks, and
   stored.
2. **Indexing** — chunks are embedded (OpenAI) and indexed in AstraDB via Cassio.
3. **Retrieval + answer** — a history-aware retriever reformulates the question from chat history,
   retrieves via MMR, and the LLM answers strictly from the retrieved legal context, with citations.
4. **Memory** — conversation history is persisted with `AstraDBChatMessageHistory`.

## Example

> A shopkeeper sells a soft drink for ₹25 even though the MRP is ₹20.

Dharmbantu cites the relevant sections of the **Legal Metrology Act, 2009** and the **Consumer
Protection Act**, and explains the available remedies — using only text found in the official
documents.

## Tech Stack

- **LangChain** — RAG pipeline, prompt templates, memory
- **OpenAI** — LLM + embeddings
- **AstraDB + Cassio** — vector store & chat-history persistence
- **BeautifulSoup / Unstructured** — web + PDF parsing
- **Streamlit**

## Getting Started

```bash
pip install -r requirements.txt
streamlit run app_for_streamlit_cloud.py
```

Provide your OpenAI API key and AstraDB credentials (via Streamlit secrets).
