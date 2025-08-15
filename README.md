# 🌌 Void System — The Electric Void

The **Void System** is a multi-layered cloud intelligence platform designed for modular, distributed reasoning and intelligent function execution. Built with a **Python core** and a **lightweight JavaScript/Electron runtime** for visualization and orchestration, the Void integrates multiple subsystems into a cohesive environment for AI-assisted cognition, automation, and system control.

At its core, the Void is **model-agnostic**, extensible, and capable of dynamic routing, memory management, continuous strategic reasoning, and modular tool invocation. It is designed to serve as both a **centralized intelligence backend** and an interactive, autonomous runtime for long-term AI system development.

* * *

## 🧩 System Architecture

The Void consists of several interconnected modules:

### ☁️ Void — The Cloud Intelligence Structure

A Python-based FastAPI backend serving as the **central router** for intelligent behavior. Handles inference requests, routes them to appropriate models or tools, and manages lightweight memory. Supports external LLM integrations, API calls, and token usage tracking.

**Core Capabilities**:

- Intelligent routing layer for prompt handling and role/task delegation.
    
- External model integration (TogetherAI, OpenAI, local models).
    
- Modular tool invocation (search, code execution, math, etc.).
    
- Memory tracking and token logging.
    
- Secure API key management via `.env`.
    

* * *

### 🌀 Deep Void — Continuous Strategic Cognition

A **real-time autonomous reasoning system** designed for long-term AGI/AI development support. Operates as an always-on loop for knowledge retrieval, argumentation, and synthesis.

**Core Capabilities**:

- Intent-driven knowledge parsing with embedding similarity.
    
- Pro/con reasoning and balanced arbitration.
    
- Persistent memory via Supabase.
    
- Multi-perspective deliberation using large models.
    
- CLI and API runtime modes.
    

* * *

### 🌍 Void Intelligence Earth — Local AI Assistant

A locally hosted **GPT-2–based assistant** for chat-like interaction, tone/style customization, and rapid prototyping. Runs entirely offline with optional GPU acceleration.

**Core Capabilities**:

- Text-based conversational interface.
    
- Adjustable tone and style profiles.
    
- Lightweight dependency footprint.
    
- Fully customizable parameters for output generation.
    

* * *

### ⚙️ Void Metal — Core System OS

A **sub-modular operating system** for managing root-level communication, logging, and orchestration between subsystems. Ensures operational integrity and synchronized message passing across the Void network.

* * *

### 🧠 Neuroscript Extension

A functional automation layer incorporating:

- **Google Search Automation**.
    
- **Ethical web-scraping** utilities.
    
- **Neurophysiological analysis suite** (via `neurokit2`).
    
- **Local PyTorch model** for decoding biosignal data.
    

* * *

## 🚀 Installation & Setup

### 1\. Clone the Repository

`git clone https://github.com/your-repo/void-system.gitcd void-system`

### 2\. Python Virtual Environment

`python -m venv .venvsource .venv/bin/activate # Windows: .venv\Scripts\Activate.ps1pip install -r requirements.txt`

### 3\. Environment Variables

Create a `.env` file:

`TOGETHER_API_KEY=your_together_api_keySUPABASE_URL=your_supabase_urlSUPABASE_KEY=your_supabase_key`

### 4\. JavaScript Runtime

From the `/electron` directory:

`npm installnpm start`

* * *

## 🖥 Running the System

### Start the Python Core (Void + Deep Void)

`uvicorn main:app --reload`

### Launch the Electron UI

`npm start`

* * *

## 📡 API Endpoints (Void Core)

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | `/chat` | Routes prompt through intelligent core |
| GET | `/usage-stats` | Total token usage |
| GET | `/daily-tokens` | Token usage for today |
| POST | `/reset-memory` | Clears conversation memory |
| GET | `/okcheck` | Health check |

* * *

## 🔐 Security

- API keys stored in `.env`.
    
- CORS restricted to approved origins.
    
- Planned: JWT authentication, route-level access control, persistent memory encryption.
    

* * *

## 🛠 Dependencies (Core)

- `fastapi`
    
- `transformers`
    
- `torch`
    
- `sentence-transformers`
    
- `supabase`
    
- `neurokit2`
    
- `python-dotenv`
    
- `uvicorn`
    
- Electron (for frontend runtime)
    

* * *

## 📜 License

Internal development system. Not licensed for public redistribution.

* * *

## 👨‍💻 Author

**Dillon Carey**  
Director of Personal AI Systems  
https://dilloncarey.com
