
# 📚 AskVault
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/tanish35/AskVault)

An AI-powered RAG (Retrieval-Augmented Generation) platform where users can upload any type of document and ask questions based on its content. Powered by FastAPI, Qdrant, LangChain, HuggingFace embeddings, Redis memory, and CrewAI for intelligent agent orchestration.

https://github.com/user-attachments/assets/6573e8ba-f794-4927-a428-7578b1e1d608


---

## 🚀 Features

- 🧠 Retrieval-Augmented Generation (RAG) pipeline with CrewAI + Gemini/OpenAI
- 🧠 Context-aware conversations with persistent memory powered by Redis
- 📎 Supports multi-format document parsing (PDF, DOCX, TXT, PPTX, etc.) via `unstructured`
- 🧲 Fast and scalable semantic search using LangChain + Qdrant
- 🧩 Modular CrewAI agents for document understanding and reasoning
- 📦 Document embeddings generated using HuggingFace (`MiniLM-L6-v2`) or any other model
- 👥 Per-user document isolation for private, personalized search
- 🔄 End-to-end contextual QA based entirely on uploaded content
- 🌐 Ready-to-integrate with any frontend (e.g., Next.js)

---

## 🧱 Stack

| Layer             | Tech Used                                                         |
| ----------------- | ----------------------------------------------------------------- |
| **Backend**       | FastAPI, Prisma (PostgreSQL)                                      |
| **Frontend**      | Next.js                                                           |
| **LLM Agents**    | [CrewAI](https://github.com/joaomdmoura/crewAI)                   |
| **Vector DB**     | Qdrant (local or cloud)                                           |
| **Embeddings**    | HuggingFace `all-MiniLM-L6-v2`                                    |
| **Memory**        | Redis + LangChain `ConversationBufferMemory`                     |
| **Parsing**       | [`unstructured`](https://github.com/Unstructured-IO/unstructured) |
| **Auth**          | `python-jose`, `bcrypt`                                           |
| **Vector Search** | LangChain + QdrantVectorStore                                     |

---

## 🔗 API Reference

Interactive API docs available at:

[http://localhost:8000/docs](http://localhost:8000/docs)


---

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/tanish35/AskVault.git
cd AskVault
````

---

### 2. Initialize Python environment with `uv`

> [uv](https://github.com/astral-sh/uv) is a modern Python package/dependency manager.

```bash
uv init
uv install
```

---

### 3. Configure Environment Variables

Create a `.env` file:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/AskVault
QDRANT_URL=http://localhost:6333
REDIS_URL=redis://localhost:6379
SECRET_KEY=your_jwt_secret
GEMINI_API_KEY=your_gemini_api_key
```

---

### 4. Set up PostgreSQL & Prisma

```bash
npx prisma generate
npx prisma migrate dev --name init
```

---

### 5. Run Qdrant and Redis locally (or use cloud versions)

```bash
docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant
docker run -p 6379:6379 redis
```

Ensure your `.env` variables match these.

---

### 6. Start the FastAPI server

```bash
uv run fastapi dev
```

---

### 7. Start the frontend (Next.js)

Inside the `frontend/` folder:

```bash
npm install
npm run dev
```

---

## 📎 Document Types Supported

Thanks to `unstructured`, these formats are supported:

* `.pdf`
* `.docx`
* `.txt`
* `.pptx`
* `.html`
* `.eml`, `.msg`
* `.md`, `.rst`

---

## 🧠 RAG Agent (CrewAI)

The app uses `CrewAI` to define a **document expert agent** that:

* Uses `LangChain` tools to search your documents
* Responds only using context retrieved from Qdrant
* Maintains **conversational state using Redis-based memory** to understand context across turns
* Handles user-specific queries using JWT-based filtering

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a new branch for your feature or fix
3. Make your changes and commit them
4. Push to your branch
5. Create a pull request

---

## 📌 License

MIT © 2025 – Tanish Majumdar

