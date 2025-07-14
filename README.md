# 🗵️ Dharmbantu — Your Pocket Indian Law Assistant 🇮🇳⚖️

Dharmbantu is a generative AI-powered legal assistant designed to provide instant legal help based entirely on India's official legal documents. It leverages LLMs, LangChain, AstraDB, and Streamlit to serve relevant sections and acts from Indian laws, including:

* Bharatiya Nyaya Sanhita (BNS)
* Bharatiya Nagarik Suraksha Sanhita (BNSS)
* Bharatiya Sakshya Adhiniyam (BSA)
* Code of Civil Procedure (CPC)

## ✨ Key Features

* 🔍 Context-aware answers using RAG (Retrieval Augmented Generation)
* 📝 Accurate section & act citation (no hallucination)
* 📄 PDF scraping and ingestion from [https://indiacode.nic.in](https://indiacode.nic.in)
* 📂 AstraDB-backed vector search & chat history
* 😊 Friendly conversational interface via Streamlit
* 🧠 MMR-based retriever with fine-tuned prompt chains

---

## 📖 Example Use Case

### Scenario:

**A shopkeeper is selling a soft drink for ₹25 even though the MRP is ₹20.**

### Dharmbantu Response:

* Cites relevant sections from **Legal Metrology Act, 2009**.
* Brings in **Consumer Protection Act** (Grievance Redressal Forums).
* Explains legal remedies with plain-language breakdown.
* Returns only data found in official documents (no hallucination).

---

## 🛠️ Project Structure

| File                         | Description                                          |
| ---------------------------- | ---------------------------------------------------- |
| `app_for_streamlit_cloud.py` | Main Streamlit app and RAG pipeline                  |
| `pdf_extraction.py`          | Code for scraping acts from IndiaCode & storing them |
| `partial_docs.pkl`           | Saved parsed law text chunks for fast reload         |
| `failed_urls.pkl`            | Tracks scraping failures for retry                   |
| `acts_pdfs.py`               | Function to return scraped PDF links                 |

---

## 💡 How It Works

1. **Scraping & Parsing**

   * Scrapes IndiaCode pages using BeautifulSoup.
   * Extracts first PDF from each view page.
   * Loads, splits, and stores parsed content as documents.

2. **Embedding + Indexing**

   * Uses OpenAI embeddings to convert documents into vectors.
   * Indexes these chunks into AstraDB via Cassio (LangChain wrapper).

3. **Conversational Interface**

   * User asks a question.
   * LangChain uses `create_history_aware_retriever` and `RunnableWithMessageHistory`.
   * The response is generated based on context documents and chat history.

4. **Response**

   * Returns the answer with direct citations from legal context only.
   * Retains chat history via `AstraDBChatMessageHistory`.

---

## 🦇 Technologies Used

* **LangChain**: RAG pipeline + prompt templates + memory
* **OpenAI**: LLM & Embeddings
* **Cassio + AstraDB**: Vector DB + Memory persistence
* **Unstructured + BeautifulSoup**: PDF + Web parsing
* **Streamlit**: UI frontend

---

## 🚀 Getting Started

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Secrets

Create `.streamlit/secrets.toml`:

```toml
ASTRA_DB_APPLICATION_TOKEN = "your_token"
ASTRA_DB_ID = "your_db_id"
ASTRA_DB_ENDPOINT = "your_endpoint"
```

### Run App

```bash
streamlit run app_for_streamlit_cloud.py
```

---

## 📊 Future Plans

* 🔎 **Landmark Case Agent**: Retrieve landmark judgments related to query.
* 📄 **Court Paper Analyzer**: Upload and analyze court documents.
* 🤖 **Multi-Agent System**:

  * Retrieval Agent (acts/sections)
  * Case Law Agent (precedents)
  * Reasoning Agent (suggestions)
  * Judge Simulator Agent (decision predictor)

---

## 🤝 Why Dharmbantu vs ChatGPT?

| Feature                       | ChatGPT      | Dharmbantu      |
| ----------------------------- | ------------ | --------------- |
| Trained on Indian laws?       | ❌            | ✅               |
| Cites official acts/sections? | ⚠️ Sometimes | ✅ Always        |
| Retains session memory?       | ❌            | ✅               |
| Uses official PDF sources?    | ❌            | ✅               |
| Multi-agent pipeline?         | ❌            | ✅ (in progress) |

---

## 📄 License

MIT License

---

## 📙 Built With Love By

[Baladitya Sai Chinni](https://github.com/baladityasai) | Final Year Student | AI App Dev | Legal Tech Enthusiast
