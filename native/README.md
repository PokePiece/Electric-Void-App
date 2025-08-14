# Human_AGI

A modular architecture for an artificial general intelligence (AGI) system written in C++ with Qt, Python, and embedded memory systems.  
This project defines an extensible structure for cognitive simulation, memory management, and intelligent interaction via API bridges.

## 🧠 Architecture Overview

Human_AGI uses a **multi-language, multi-process** architecture:

- **C++ Core (Qt GUI)**: Main control loop, decision system, and physical simulation interface.
- **Python Server (Flask)**: Hosts dynamic AI routines and memory logic.
- **ChromaDB (Python)**: Embeds and stores vectorized representations of memory for retrieval.

C++ ↔ Flask (Python) ↔ ChromaDB

## ✅ Features

- Modular, component-based AGI design
- Separation of C++ logic and Python cognition
- Python `VoidAGI` server for dynamic logic and memory access
- ChromaDB-backed `retrievememory.py` for vector memory embedding + retrieval
- REST API between systems (`chat` route)
- Easily extensible toward cloud integration or local-only systems

## 📁 Directory Structure

/Human_AGI
├── Brain/ # Core AGI logic in C++
│ ├── VoidBrain.cpp # Main bridge to Python
│ └── ...
├── Python/
│ ├── VoidAGI.py # Flask server exposing the AI interface
│ └── retrievememory.py # Chroma memory manager
├── Vision/ # Visual processing components
├── Language/ # Language interface modules
├── HumanAGI.pro # Qt project file
└── main.cpp # Entry point


## ⚙️ Requirements

### C++

- Qt 6.0+ (e.g., Qt 6.9.1)
- C++17 compatible compiler (e.g., `mingw32-g++`)
- `qmake`, `mingw32-make`

### Python

- Python 3.10+
- `flask`
- `chromadb`
- `sentence-transformers`

Install Python dependencies:
```bash
pip install flask chromadb sentence-transformers
```
## 🔨 Build Instructions

C++ Qt Side

``` bash qmake HumanAGI.pro
mingw32-make
```
Python Server
```bash

cd Python
python VoidAGI.py
```
Make sure this Flask server is running in the background when launching the C++ executable.

## 🧠 Memory: ChromaDB
We use ChromaDB for embedding and retrieval of conversation or sensor history.

store_memory(text) — stores embedded content

retrieve_similar(text) — gets semantically related items from memory

Stored memory will be returned alongside AI responses for contextual grounding.

## 🧪 Example Flow
User types message in C++ GUI.

C++ → sends to Flask /chat route.

Flask stores message in Chroma, retrieves similar context.

AI logic executes.

Response + memory → back to C++ for UI output.

## 🚧 Future Work
Background Python server boot via C++

Cloud sync and multi-agent communication

Lisp/Prolog interfaces for meta-reasoning

File/video/image embeddings via Chroma

Autonomy and feedback reinforcement loop