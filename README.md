
# 🐋 Whale-LLM-Companion

A sleek, animated desktop AI assistant and focus companion powered by local LLMs via **Ollama**. The Whale sits on your desktop, provides an interface for local AI interactions, and monitors active windows to nudge you back to productivity when you drift into distraction apps.

## ✨ Key Features

* **Animated UI:** A frameless, transparent companion that lives on top of your workspace.
* **Local AI Brain:** Powered by **Ollama**, ensuring your data stays private and your assistant works offline.
* **Focus Monitoring:** Intelligently detects visible "distraction" windows (like Steam, Discord, or games) and nudges you to stay on task.
* **Drag & Drop:** Easily move the whale anywhere on your screen.
* **Rich Text Experience:** Full Markdown support for AI responses, including code blocks, bold text, and lists.
* **Non-Blocking Logic:** Built with multi-threading to ensure the UI stays responsive while the AI generates answers.

## 🛠️ Tech Stack

* **Language:** Python 3.10+
* **Framework:** PyQt6
* **LLM Interface:** Ollama API
* **Processing:** Threaded I/O for API calls

## 🚀 Getting Started

### 1. Prerequisites
Ensure you have **Ollama** installed and a model pulled:

ollama pull gemma4:e4b

### 2. Installation
Clone the repository and install the required Python dependencies to handle the UI, network requests, and markdown rendering:
```bash
pip install PyQt6 requests markdown
python whale_assistant.py
```
3.  **Interaction:** 
    *   **Left Click** the whale to toggle the chat interface.
    *   **Click & Drag** to move the whale to any position on your screen.
    *   **Chat:** Type your query into the input field and press **Enter** to get a response from your local LLM[cite: 1].

## ⚙️ Configuration
You can customize the behavior of your assistant directly in the `whale_assistant.py` file:
```python
# List the .exe names of applications you consider distractions
DISTRACTIONS = ["steam.exe", "discord.exe", "chrome.exe"]

# Specify which Ollama model you want to use
MODEL_NAME = "gemma4:e4b"