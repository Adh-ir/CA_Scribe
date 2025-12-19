# SAICA Scribe 🤖

**AI-Powered Competency Documentation Assistant for SAICA Trainees.**

Developed by **[Adhir Singh](https://github.com/Adh-ir)**.

SAICA Scribe helps you map your daily audit activities to the SAICA Competency Framework (2025 Training Plan) using advanced AI (Google Gemini 1.5 Pro/Flash or Groq Llama 3).

## 🚀 Features

*   **Smart Mapping**: Analyzes your input and matches it against the *entire* SAICA 2025 Training Plan.
*   **Dual Engine**: Choose between **Google Gemini** (High Accuracy, Recommended) or **Groq** (High Speed).
*   **Privacy First (BYOK)**: Bring Your Own Key. Your API keys are stored locally on your machine (`.env`) and never shared.
*   **Premium Web UI**: sleek, modern interface for easy reporting.

## 🛠️ Quick Start

### Prerequisites
*   Python 3.10 or higher.

### Installation & Run

1.  **Download** this repository (Code -> Download ZIP) and extract it.
2.  **No installation required!** Just double-click the launcher script for your OS:

    *   🍎 **Mac User?**
        Double-click `Run_SAICA_Scribe.command`.
        *(Note: First time might require Right-Click -> Open if MacOS warns about developers)*

    *   🪟 **Windows User?**
        Double-click `Run_SAICA_Scribe.bat`.

3.  The application will automatically set itself up and open in your browser at `http://localhost:8000`.

### First Time Setup
The app will guide you through a one-time setup wizard:
1.  It will ask you to choose an AI provider (Gemini recommended).
2.  It provides direct links to generate your **Free API Keys**.
3.  Paste the key into the app, and you are ready to go!

## 💡 Usage Tips
*   **Be Specific**: Mention the *Client*, *Task*, and *Outcome*.
*   **Targeting**: Use the helper button or type `COMPETENCY: [Name] EVIDENCE: [Desc]` to force a specific mapping.

---
*Made with ❤️ by [Adhir Singh](https://github.com/Adh-ir)*
