# Firebolt AI Chatbot Demo

A reference implementation of a **Retrieval-Augmented Generation (RAG) chatbot** powered by [Chainlit](https://docs.chainlit.io/) for the chat UI, **OpenAI** for the LLM, and **Firebolt** as the analytical database and vector store. It lets you ask questions in everyday language and receive answers backed by SQL queries that run live on Firebolt.

---

## Repository Layout

| Path                         | Purpose                                                                                       |
| ---------------------------- | --------------------------------------------------------------------------------------------- |
| `src/app.py`                 | Chainlit entry-point and main event loop                                                      |
| `src/system_prompt.md`       | **System prompt** that controls the assistant’s personality & abilities – edit here first |
| `src/firebolt_connection.py` | Thin wrapper around the [Firebolt Python SDK](https://pypi.org/project/firebolt-sdk/)         |
| `src/tools/*.py`             | Re-usable Tool classes that the LLM can call (e.g. `QueryTool`, `PlotTool`)                   |


---

## Quick Start (TL;DR)

```bash
# 1. Clone and step inside
git clone https://github.com/your-org/fb_ai_demo.git
cd fb_ai_demo

# 2. Create + activate a virtualenv (Python ≥ 3.9)
python3 -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create a .env file with your credentials (see section 3)
$EDITOR .env

# 5. Launch the app
chainlit run src/app.py --watch
```

---

## 1 – Prerequisites

* **Python 3.9+** – `python3 --version`
* A **Firebolt** account with

  * a database + engine
  * an API key (`ACCOUNT_ID` / `SECRET`)
* An **OpenAI** API key
* macOS / Linux terminal (Windows WSL works too).


If you're not already a Firebolt user,
[sign up on the Firebolt website for $200 in free credits](https://go.firebolt.io/signup)
to get started with any of the Firebolt tutorials.


---

## 2 – Environment Setup

```bash
# Create and activate a fresh venv
python3 -m venv .venv
source .venv/bin/activate

# Upgrade pip + install deps
python -m pip install -U pip
pip install -r requirements.txt

# Verify that the Chainlit installation was successful
chainlit hello  # should open a browser tab
```

---

## 3 – Configuration

Create a `.env` file in the repository root and add the following keys:

```ini
# OpenAI
OPENAI_API_KEY="sk-..."

# Firebolt
FIREBOLT_ACCOUNT_NAME="..."
FIREBOLT_ACCOUNT_ID="..."
FIREBOLT_ACCOUNT_SECRET="..."
FIREBOLT_DATABASE_NAME="..."
FIREBOLT_ENGINE_NAME="..."
```

1. **Save & close** the file—Chainlit will pick it up automatically.
2. **(Optional) Fine-tune behaviour** in `src/system_prompt.md`. For example, tighten the SQL style guide or change the persona from helpful assistant to pedantic mentor.


---

## 4 – Running the App

```bash
chainlit run src/app.py
```
You can pass the `--watch` flag to enable auto-reloading for development.

* Append `--port 8501` to change the default port.
* Logs are written to `logs/chainlit.log` by default; override with the `LOG_LEVEL` env var.

---

## 5 – Asking Good Questions

Try queries like:

* *“How many clicks were driven by each search engine in **Q4 2024**?”*
* *“Refine a query that finds the **top 10 keywords** for Google in that period.”*
* *“Show me a bar chart of clicks per engine.”*

The assistant follows a simple three step flow:

1. Generate a **SQL** statement.
2. Execute it on Firebolt.
3. Optionally call custom tools (e.g. `PlotTool`, `CsvTool`, `ExplainTool`) to visualise the result using [Vega-Lite](https://vega.github.io/vega-lite/).

---


## 6 – Troubleshooting

| Symptom                             | Fix                                                                                     |
| ----------------------------------- | --------------------------------------------------------------------------------------- |
| `chainlit: command not found`       | Did you activate the venv? `source .venv/bin/activate`                                  |
| `401 UNAUTHENTICATED` from Firebolt | Check `FIREBOLT_ACCOUNT_*` vars and that your service account has DB/engine permissions |
| LLM outputs gibberish / empty       | Verify the model name in `.env` matches an available engine                             |
| Cannot bind to port `8000`          | Pass `--port 8500` or kill the process that owns 8000 (`lsof -i :8000`)                 |

---

## 7 – Roadmap & Ideas

* **Streaming** partial LLM responses
* **Explain Plan** tab that shows Firebolt’s query plan
* Plug-in system for domain-specific tools (e.g. Jira, Slack)
* One-click deploy to **Render** / **Fly.io**
* OAuth login to protect prod instances

Questions / ideas? Open an issue or PR—contributions are welcome!
