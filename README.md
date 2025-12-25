# CA Scribe 🤖

**AI-Powered Competency Documentation Assistant for SAICA Trainees.**

Developed by **[Adhir Singh](https://github.com/Adh-ir)**.

CA Scribe helps you map your daily audit activities to the SAICA Competency Framework (2025 Training Plan) using advanced AI models.

## 🌐 Try It Now

**[Launch CA Scribe →](https://ca-scribe.streamlit.app)** *(Hosted on Streamlit Cloud)*

## 🚀 Features

*   **Smart Mapping**: Analyzes your input and matches it against the *entire* SAICA 2025 Training Plan.
*   **Multi-Model Support**:
    *   **Google Gemini 2.0 Flash Exp** (Default, High Intelligence).
    *   **GitHub Models (GPT-4o / Mini)** (Strict, Precise).
    *   **Groq (Llama 3)** (Lightning Fast).
*   **Privacy First (BYOK)**: Bring Your Own Key. Your API keys are stored in your session and never shared.
*   **Strict Filtering**: Target a specific competency code (e.g. `COMPETENCY: 1a`) and the system guarantees a single, focused result.

## 🔑 Getting Started

1.  **Open the App**: Visit the link above
2.  **Get an API Key** (free): Follow the in-app guide to get a key from:
    *   [Google AI Studio](https://aistudio.google.com/app/apikey) (Recommended)
    *   [Groq Console](https://console.groq.com/keys) (Fastest)
    *   [GitHub Tokens](https://github.com/settings/tokens) (GPT-4o)
3.  **Paste your key** in the setup wizard and start mapping!

## 💡 Usage Tips

*   **Be Specific**: Mention the *Client*, *Task*, and *Outcome* in your activity.
*   **Targeting**:
    *   **Broad Search**: Just type your activity. The AI finds all relevant matches.
    *   **Specific Target**: Click "Target Competency" button and fill in the template.
    *   *Example*: `COMPETENCY: 1a EVIDENCE: I reconciled the bank statement...` (This guarantees ONLY competency 1a is returned).

## 🛠️ Local Development

If you want to run CA Scribe locally:

```bash
# Clone the repository
git clone https://github.com/Adh-ir/CA_Scribe.git
cd CA_Scribe/code

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Mac/Linux
# or: .venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run streamlit_app.py
```

The app will open at `http://localhost:8501`.

## 📁 Project Structure

```
CA_Scribe/
├── code/
│   ├── streamlit_app.py      # Main Streamlit application
│   ├── config.py             # Configuration settings
│   ├── requirements.txt      # Python dependencies
│   ├── analysis/             # AI mapping logic
│   ├── ingestion/            # Framework data loading
│   ├── reporting/            # Report generation
│   ├── utils/                # Styles and templates
│   └── templates/            # HTML templates (guide)
├── .streamlit/               # Streamlit configuration
└── README.md
```

---
*Made with ❤️ by [Adhir Singh](https://github.com/Adh-ir)*
