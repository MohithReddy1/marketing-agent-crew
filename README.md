# 🤖 Multi-Agent Content Engine

[![Python Version](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Framework-CrewAI-red.svg)](https://github.com/crewAIInc/crewAI)
[![LLM Platform](https://img.shields.io/badge/LLM-Google%20AI%20Studio-orange.svg)](https://ai.google.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An automated content marketing factory driven by a sequential crew of specialized AI agents. This application transforms any raw topic, engineering insight, or article link into highly optimized, platform-specific copy tailored for **X (Twitter)**, **LinkedIn**, and **Instagram** instantly via a clean, unified web dashboard.

---

## 🚀 Features

- **Multi-Agent Collaboration:** Harnesses an isolated, specialized workforce (Researcher $\rightarrow$ Copywriter $\rightarrow$ Editor) working sequentially instead of a single generalist LLM prompt.
- **High-Performance Cost Efficiency:** Built natively using the **Gemini 3.1 Flash-Lite** core engine, providing high per-minute request limits (15 RPM) and rapid inference with 0$ overhead.
- **Production-Ready Web UI:** Powered by Streamlit to offer users a frictionless, responsive dashboard completely divorced from the terminal environment.
- **Copy-Paste Optimized Outputs:** Generates specialized layouts out of the box—including five-part X threads with conversion hooks, inline professional bulleted arrays for LinkedIn, and clean, punchy multi-tag descriptions for Instagram.

---

## ⚙️ How It Works

The engine uses a strict sequential execution assembly line model where data flows smoothly downstream, with each agent's output serving as the foundational context for the next task:

```text
  [ User Input Topic ]
           │
           ▼
┌──────────────────────────────┐
│  1. Lead Content Researcher  │ ──► Extracts Top 3 Takeaways & Target Audience
└──────────────────────────────┘
           │
           ▼
┌──────────────────────────────┐
│  2. Social Media Copywriter  │ ──► Structures hooks, X Threads, & platform copy
└──────────────────────────────┘
           │
           ▼
┌──────────────────────────────┐
│    3. Chief Brand Editor     │ ──► Audits sentence flow, formatting, & line breaks
└──────────────────────────────┘
           │
           ▼
 [ Live Streamlit UI Display ]

```

### 🕵️‍♂️ Agent Workflow Deep-Dive

* **The Lead Content Researcher** ingests your topic raw, parsing out fluff, verifying objective logical arguments, and classifying the primary target buyer persona or developer group.
* **The Social Media Copywriter** steps in, accepting the researcher's breakdown as mandatory constraints, adapting voice frameworks, building engagement hooks, and implementing specific distribution angles for individual channels.
* **The Chief Brand Editor** performs structural quality control, scrubbing alignment bugs, fine-tuning line breaks for optimal scannability, and ensuring execution blocks meet modern corporate publishing standards.

---

### 🛠️ Tech Stack

* **Orchestration Framework:** `CrewAI` (Role-based agent design, automated cross-task memory handoffs)
* **Core Intelligence Engine:** `Google Gemini 3.1 Flash-Lite` (Advanced multimodal text processing, highly optimized cost-to-performance scaling profile)
* **Storefront Web Framework:** `Streamlit` (Sleek reactive Python dashboard state rendering)
* **Environment State Security:** `Python Dotenv` (Isolated credential safeguarding)

---

### 📦 Setup and Local Installation

#### Prerequisites
- Python 3.12+ installed on an environment terminal path.
- A valid Google AI Studio API Key.

#### 1. Clone the Repository
```bash
git clone [https://github.com/MohithReddy1/marketing-agent-crew](https://github.com/MohithReddy1/marketing-agent-crew)
cd marketing-agent-crew
```
### 🔑 2. Configure Your Environment Secrets
Create a `.env` file directly within the root project directory:

```env
GEMINI_API_KEY=your_secret_google_ai_studio_api_key_here
```
### 📦 3. Install Target Dependencies
Automatically build and compile the application's virtual container dependencies using the project requirements manifest:

```bash
pip install -r requirements.txt
```
### 🖥️ 4. Boot Up the Dashboard Storefront
Launch the local web server layer directly from your active interpreter environment context:

```bash
python -m streamlit run main.py
```
## 🤝 Contributing & Future Roadmap

This project is fully open-source and free to use! Here is how you can get involved or scale it:

* **Developer Support:** Feel free to fork this repository, open descriptive issues, or submit code optimization pull requests!
* **Custom Enterprise Adaptations:** Looking to add automated live URL scraping or fine-tuned custom enterprise brand voice models? Feel free to reach out or drop a suggestion in the issues tab.

---

*Distributed under the permissive **MIT License**. See the [LICENSE](LICENSE) file for complete rights and liability terms.*
