# PrivateGPT Document Chat 🤖📄

A production-ready, privacy-focused Retrieval-Augmented Generation (RAG) platform that allows users to upload documents (PDF, DOCX, TXT) and chat with them using grounded AI without fine-tuning or model retraining.

---

## 🚀 Quick Launch (Windows Batch File)

Simply double-click `run.bat` or execute in terminal:
```cmd
run.bat
```
This automatically sets up environment variables, installs missing Python and Node dependencies, and opens both the FastAPI backend (`http://localhost:8000`) and Next.js frontend (`http://localhost:3000`) in dedicated windows!

---

## 🌟 Key Features

- **Strict RAG Grounding**: System prompt strictly limits LLM responses to uploaded document context, preventing hallucinations.
- **FAISS Vector Indexing**: Per-document vector stores saved locally, preventing redundant embedding generation.
- **Multi-Document Support**: Select single or multiple documents for combined similarity search queries.
- **JWT User Authentication**: Secure registration, login, password hashing (bcrypt), and OAuth2 Bearer validation.
- **Token & Cost Tracking**: Live calculation of prompt tokens, completion tokens, embedding costs, and confidence scores.
- **Citations & Source Drawer**: View exact page numbers and highlighted cited passages for every answer.
- **Streaming Response Support**: Token-by-token SSE streaming capability.
- **Clean UI & Dark Mode**: Modern Next.js 14 dashboard with responsive dark/light mode UI.

---

## 🏗️ Architecture Diagram

```
 ┌────────────────────────────────────────────────────────────────┐
 │                      Next.js Frontend (React + Tailwind)       │
 │  - JWT Auth (Login/Register)   - Document Dashboard            │
 │  - SSE Streaming Chat UI       - Citations & Sources Drawer    │
 │  - Cost & Token Tracker        - Dark / Light Mode Toggle      │
 └───────────────────────────────┬────────────────────────────────┘
                                 │ REST & SSE API Calls
 ┌───────────────────────────────▼────────────────────────────────┐
 │                        FastAPI Backend                         │
 │  ┌──────────────────┬──────────────────┬────────────────────┐  │
 │  │ Auth Router      │ Documents Router │ Chat / RAG Router  │  │
 │  └────────┬─────────┴────────┬─────────┴────────┬───────────┘  │
 │           │                  │                  │              │
 │  ┌────────▼─────────┬────────▼──────────────────▼───────────┐  │
 │  │ SQLAlchemy Async │ Document Processing Pipeline          │  │
 │  │ (SQLite / Postgres)│ (pdfplumber, docx, PyPDF2)         │  │
 │  └──────────────────┴──────────────────┬────────────────────┘  │
 │                                        │                       │
 │  ┌─────────────────────────────────────▼────────────────────┐  │
 │  │ Vector Store Engine (FAISS CPU) & Embeddings Manager     │  │
 │  │ Model: text-embedding-3-small                           │  │
 │  └─────────────────────────────────────┬────────────────────┘  │
 │                                        │                       │
 │  ┌─────────────────────────────────────▼────────────────────┐  │
 │  │ LLM Generation & Grounding Pipeline                     │  │
 │  │ Model: gpt-4o-mini / gpt-4o                             │  │
 │  └──────────────────────────────────────────────────────────┘  │
 └────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

- **Backend**: Python 3.12, FastAPI, LangChain, FAISS, SQLAlchemy (Async), SQLite / PostgreSQL support, Pydantic v2, Uvicorn.
- **Frontend**: Next.js 14, React 18, Tailwind CSS, Lucide Icons, Axios.
- **Document Processing**: `pdfplumber`, `PyPDF2`, `python-docx`, Tesseract OCR support.
- **Embeddings & LLM**: OpenAI `text-embedding-3-small` and `gpt-4o-mini` / `gpt-4o`.

---

## 📡 API Reference

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/auth/register` | Register new user account |
| `POST` | `/api/v1/auth/login` | Login and obtain JWT access token |
| `GET` | `/api/v1/auth/me` | Fetch authenticated user profile |
| `POST` | `/api/v1/documents/upload` | Upload & index PDF, DOCX, or TXT document |
| `GET` | `/api/v1/documents` | List user uploaded documents |
| `DELETE` | `/api/v1/documents/{id}` | Delete document and FAISS index |
| `PUT` | `/api/v1/documents/{id}/rename` | Rename document |
| `POST` | `/api/v1/chat` | Execute grounded RAG query |
| `POST` | `/api/v1/chat/stream` | Stream grounded RAG answer token-by-token |
| `GET` | `/api/v1/history` | Fetch conversation history |

---

## 🧪 Running Tests

```bash
cd backend
pytest tests/ -v
```
