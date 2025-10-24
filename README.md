
# RAG Chatbot with Ollama + PostgreSQL

## Overview
This project implements a **Retrieval-Augmented Generation (RAG)** chatbot using a local **Ollama** model and **PostgreSQL with pgvector**.  
The chatbot retrieves relevant document chunks from a database using vector similarity search and uses a generative model to produce human-like, contextually accurate answers.

This setup allows you to run a **fully local RAG system** - no external API calls, no OpenAI keys required.

---

## What is RAG (Retrieval-Augmented Generation)?
RAG combines **information retrieval** and **language generation**.

1. **Retrieval**: The system searches a knowledge base (like documents, manuals, or FAQs) for information related to the user's question.
2. **Augmentation**: The most relevant pieces of information (called *contexts*) are combined with the question.
3. **Generation**: A language model uses that information to generate an answer that's grounded in facts - not hallucinations.

This architecture is ideal for **building assistants that answer questions using your own data** (e.g., product manuals, policies, research papers, your custom tool).

---

## How It Works

### 1. **Embedding**
- Each document or paragraph is converted into a **vector** - a list of floating‑point numbers representing its meaning.
- These vectors are stored in PostgreSQL using the **pgvector** extension.

### 2. **Vector Similarity Search**
- When a user asks a question, it's also embedded into a vector.
- The database compares this question vector to stored document vectors using **cosine similarity** to find the closest matches.

#### Cosine Similarity Explained
Imagine each vector as a point in space.  
The **cosine similarity** measures the angle between two vectors - smaller angles mean the vectors are more alike. 
Mathematically:

```
cosine_similarity = (A · B) / (||A|| × ||B||)
```

Where:
- `A · B` = dot product of the two vectors  
- `||A||` and `||B||` = their magnitudes (lengths)

A cosine value of **1** means identical direction (perfect match),  
**0** means no similarity, and **–1** means opposite meanings.

---

## Tech Stack

| Component | Purpose |
|------------|----------|
| **PostgreSQL + pgvector** | Stores document embeddings and supports vector search |
| **Ollama** | Runs local LLMs for embedding and response generation |
| **Python (psycopg)** | Handles database management and schema creation |
| **DeepSeek‑R1** | Final chosen generative model for concise, context‑aware answers |

---

## Experimentation Summary

### Embedding Models
- **`embeddinggemma`** – Tried for embeddings but caused internal server errors in Ollama.
- **`llama3-chatqa`** – A generative model, not suitable for embeddings.
- **Final Choice:** **`nomic-embed-text`**, A compatible Ollama embedding model producing **768‑dimension vectors**.

### Generative Models
- **`llama3`** – Generated short and incomplete answers.
- **Final Choice:** **`deepseek‑r1`**, which provides concise, accurate responses without redundant text.

### Chunking Strategy
We tested:
- **Section-level chunks** -> Too big, lost context.  
- **Sentence-level chunks** -> Worked best for meaningful retrieval.

---

## Database Schema
The `documents` table:

```sql
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    title VARCHAR NOT NULL,
    content TEXT NOT NULL,
    embedding VECTOR(768),
    date TIMESTAMP DEFAULT now()
);
```

Common issue encountered:
```
type "vector" does not exist
```
**Solution:** Run `CREATE EXTENSION vector;` inside your database (not globally).

---

## Setup Instructions

### 1. Create Database
```bash
python src/test.py
```
This script automatically:
1. Creates the database  
2. Installs the `pgvector` extension  
3. Creates the schema and tables  
4. Adds indexes for fast retrieval

### 2. Ingest Your Data
Place your documentation or `.txt` files inside `src/data` folder and call:
```python
Handler.Injest()
```
This will embed and store document chunks.

### 3. Ask Questions
```bash
python src/main.py
```
Example:
```
User: Can I clone a VM?
Bot: Yes. Go to Compute -> Virtual Machines -> Clone. Select the source VM and desired configuration.
```

---

## How to Build Your Own RAG Chatbot

1. **Prepare your data** – Convert your documentation into text.
2. **Embed** – Use an embedding model (like one from Ollama) to turn text into vectors.
3. **Store in pgvector** – Create a table with `VECTOR()` columns.
4. **Retrieve** – Find top‑k similar vectors using cosine similarity.
5. **Generate** – Pass those retrieved chunks into an LLM (like DeepSeek‑R1) to get an answer.

This modular design lets you replace:
- The model (any Ollama LLM)
- The vector DB (PostgreSQL, Milvus, or FAISS)
- The UI (CLI, web, or API)

---

## Commands Summary

| Command | Description |
|----------|-------------|
| `python src/test.py` | Setup database, schema, and indexes |
| `python src/main.py` | Run chatbot |
| `Handler.Injest()` | Ingest documentation into vector DB |

---

## Lessons Learned
- pgvector must be installed **inside** your target database, not globally.  
- **Documentation style and format are the real key** to achieving high-quality retrieval.  
  - The clearer, cleaner, and more structured your documents are,  
    the easier they are to chunk, embed, and store accurately — resulting in far better answers.  
- **Small, well-segmented text chunks** improve retrieval precision.  
- **FAQ-style documentation** works best, as each question and answer can be stored as its own semantic unit.  
- Local Ollama models make RAG practical without depending on APIs.  
- **DeepSeek-R1** outperforms other local models in consistency, tone, and clarity.  

---

## Final Notes
This project demonstrates how **Retrieval-Augmented Generation (RAG)** works end-to-end —  
from text ingestion, vector storage, and similarity search, to context-aware question answering.

The **quality of your results** depends heavily on the **clarity and structure of your documentation**.  
Well-formatted, logically divided, and consistently written documentation yields far better embeddings, retrievals, and generated responses.

Below is the **exact prompt template** used for response generation:

```
prompt = f"""
    You are Alfred the product assistant.
    Answer using ONLY the provided context.
    If the answer is not explicitly stated in the context, reply exactly:
    \"I couldn't find this in the documentation provided.\"

    [CONTEXT]
    {context}

    [QUESTION]
    {question}

    [INSTRUCTIONS]
    - Do not use outside knowledge.
    - Quote the relevant line(s) from the context when possible.
    - If missing, respond exactly with: I couldn't find this in the documentation provided.

    [ANSWER]
"""
```

This prompt ensures:
- The model answers strictly from the provided documentation.  
- Hallucinations are prevented by design.  
- Responses remain clear, concise, and traceable to the original source.

---

License
-----------
Proprietary License - All Rights Reserved
© 2025 Jawwad Ahmed Abbasi, Kodelle Inc.

This project is protected under a proprietary license.
You may view and learn from the source code for educational or portfolio purposes,
but commercial use, modification, or redistribution requires a paid license or written permission.

For licensing or commercial use inquiries: jawwad@kodelle.com

---

## Author
**Jawwad Ahmed Abbasi**  
Senior Software Developer  
[GitHub](https://github.com/jawwadabbasi) | [YouTube](https://www.youtube.com/@jawwad_abbasi)