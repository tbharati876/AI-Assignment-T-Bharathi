#  Financial Document Analyzer - VWO GenAI Debug Challenge

A robust, enterprise-grade financial analysis system built with **CrewAI** and **FastAPI**. This repository serves as a successful resolution of the VWO Internship Debug Challenge, featuring local RAG (Retrieval-Augmented Generation) and asynchronous task processing.

##  Table of Contents
- [The Debug Log](#-the-debug-log)
- [Architecture & Bonus Features](#-architecture--bonus-features)
- [Tech Stack](#-tech-stack)
- [Getting Started](#-getting-started)
- [API Documentation](#-api-documentation)

---

##  The Debug Log

### 1. Deterministic Bug: The "OpenAI Dependency"
- **Issue:** The original `PDFSearchTool` was hardcoded to use OpenAI for both text embeddings and internal RAG summarization, leading to `401 Unauthorized` errors when no API key was present.
- **Fix:** Overrode the tool's internal configuration to use **HuggingFace** (`all-MiniLM-L6-v2`) for local vector embeddings. This allows the system to index and search the Tesla PDF entirely on the local machine/Colab instance.

### 2. Inefficient Prompts: "Agentic Drift"
- **Issue:** Agents had generic backstories and vague task descriptions, causing them to hallucinate metrics or enter infinite loops.
- **Fix:** - Implemented **Persona-Driven Prompting**: Defined the agent as a *Senior Wall Street Research Analyst*.
    - **Structured Output constraints**: Forced the agent to return data in Markdown tables to ensure the results are parseable and professional.

### 3. Framework Stability
- **Issue:** Version mismatch between Pydantic v2 and CrewAI v0.130.0.
- **Fix:** Downgraded to `pydantic==1.10.13` to maintain compatibility with the specific CrewAI version required for the assignment.

---

##  Architecture & Bonus Features

###  0-to-1 Startup Architecture
I have upgraded the system from a simple script to a **Scalable Queue Model**:

1. **Local RAG Pipeline:** Uses HuggingFace transformers to process the `TSLA-Q2-2025-Update.pdf` without external API costs.
2. **Asynchronous Worker (Bonus):** Implemented using FastAPI's `BackgroundTasks`. This allows the API to handle concurrent uploads. The user receives a `task_id` immediately while the "worker" processes the document in the background.
3. **Database Persistence (Bonus):** Integrated **SQLite** to store the history of all analyses. This provides a "source of truth" for previous reports.



---

##  Tech Stack
- **Framework:** CrewAI (Agent Orchestration)
- **API:** FastAPI (Asynchronous Web Framework)
- **Local AI:** HuggingFace / Sentence-Transformers (Embeddings)
- **Database:** SQLite (Persistence)
- **Tunneling:** Ngrok (Remote Access)

---

##  Getting Started

### 1. Install Dependencies

pip install -r requirements.txt

### 2. Run the Application
Bash
python main.py
Note: Ensure you have replaced the NGROK_TOKEN in main.py with your personal token.

### API Documentation
POST /analyze
Uploads a PDF and queues a background analysis task.

Input: Multipart/form-data (PDF file)

Output: {"task_id": "...", "status": "Queued"}

# GET /status/{task_id}
Retrieves the result of the analysis.

Output: Returns the financial summary or PROCESSING status.

# GET /docs
Interactive Swagger UI for testing all endpoints.

