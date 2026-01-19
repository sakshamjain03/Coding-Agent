# Multi-Agent Coding Framework

A fully automated multi-agent system that converts natural-language software specifications into complete working projects using a deterministic agent pipeline.

The framework supports local LLMs via **Ollama** and cloud LLMs via **OpenRouter** and **Groq**.

---

## 🚀 Project Status

- ✅ Stable (Deterministic sequential workflow)
- 🧪 Tested (Auto-generated unit tests executed)
- 🎓 Educational Project (Learning-focused, non-commercial)
- ☁️ Hosted on Streamlit Community Cloud (Free Tier)
- ⚠️ Subject to free-tier LLM rate and token limits

**Author:** Saksham Jain


## Features

- **Sequential Agent Pipeline:** Controller → Requirements → Coding → Review → Documentation → QA → Deployment → UI  
- **Fully Offline Mode:** Uses local LLMs via Ollama  
- **Cloud Support:** Integrated with OpenRouter or Groq  
- **Automatic File Extraction:** Uses robust file markers to parse output  
- **Automatic Unit-Test Execution:** Validates code integrity automatically  
- **Streamlit UI Interface:** Easy-to-use frontend  
- **Deterministic Bounded Review Loop:** Prevents infinite loops during code review  
- **Safe Termination:** Includes runaway protection mechanisms  

## Live Demo

This project is hosted on **Streamlit Community Cloud (Free Tier)**.

🔗 **Live Application:**  
> [Coding Agent Team by Saksham Jain](https://coding-agent-by-saksham.streamlit.app/)

> ⚠️ **Note:**  
> This deployment uses free-tier LLM access. If token or rate limits are exceeded, the workflow may terminate early with a friendly error message.

---
## Installation

### 1. Clone Repository

```bash
git clone https://github.com/sakshamjain03/DataEconomy-Coding-Agent.git
cd DataEconomy-Coding-Agent
```

2. Create Virtual Environment
```python -m venv venv
source venv/bin/activate 
venv\Scripts\activate         
```
3. Install Dependencies
```
pip install -r requirements.txt
```
## LLM Setup
Choose one backend.

# Option A — Local Ollama (Recommended)
Install Ollama:

```curl -fsSL https://ollama.com/install.sh | sh
Pull model:
ollama pull llama3:8b
Ollama runs automatically on:
```
```
http://localhost:11434/v1
No API key required.
```

Option B — OpenRouter
Create an account and get an API key:

https://openrouter.ai

Option C — Groq
Create an account and get an API key:

https://console.groq.com

Environment Configuration
Copy the environment template:

```
cp .env.example .env
```
Edit .env and add the API key for your chosen backend.

Selecting Backend
Open agents.py. You will find three get_llm_config() implementations.

Only one backend must be active at a time.

Ollama Configuration
```
def get_llm_config():
return {
    "config_list": [{
        "model": "llama3:8b",
        "api_key": "ollama",
        "base_url": "http://localhost:11434/v1",
        "api_type": "openai"
    }],
    "temperature": 0.3,
    "timeout": 120,
}
```
For OpenRouter or Groq, comment out the Ollama block and uncomment the respective provider block.

Run the App
```
streamlit run app.py
```
#Why a Sequential Multi-Agent Workflow Was Chosen
This framework uses a sequential pipeline architecture instead of a free-form group-chat model to ensure correctness, reliability, and production-grade output.
Each agent depends strictly on the output of the previous stage:
Requirements → Coding → Review → Documentation → Testing → Deployment → UI
This guarantees that:
Code is never written without finalized requirements.
Tests, documentation, and deployment scripts are generated only after approved code.
Invalid or partial artifacts are eliminated.
A controlled review feedback loop allows the Review Agent to send work back to the Coding Agent only when necessary, with a bounded retry limit to prevent infinite loops.
We initially tested autonomous group-chat and dynamic speaker-selection approaches. These resulted in:
Out-of-order execution
Missing or empty artifacts
API-specific role mismatches and instability
The sequential architecture eliminated these failure modes while providing:
Deterministic execution
Easy debugging and traceability
Predictable cost and performance
Clean separation of responsibilities per agent
This design mirrors real-world software development pipelines and ensures the system produces consistent, review-validated, deployment-ready outputs.

## Agents Overview

Each agent represents a real-world software development role. Agents operate **sequentially**, not autonomously, to ensure correctness.

### 🧭 Controller Agent
- Entry point of the system
- Interprets the user request
- Enforces workflow rules and file-output contracts
- Orchestrates downstream agents

### 📋 Requirements Agent
- Converts natural-language input into structured requirements
- Outputs `requirements.md`
- Defines functional, non-functional, and edge-case requirements

### 💻 Coding Agent
- Generates production-ready Python code
- Outputs `main.py`
- Uses only built-in Python libraries
- Implements all approved requirements

### 🔍 Review Agent
- Reviews code for correctness, security, and efficiency
- Either:
  - **APPROVES** the code, or
  - Issues **FIX_REQUIRED**, triggering a controlled re-iteration
- Enforces dependency and safety constraints

### 📄 Documentation Agent
- Generates comprehensive project documentation
- Outputs `README.md`
- Explains architecture, usage, and code structure

### 🧪 QA Agent
- Generates unit tests
- Outputs `test_main.py`
- Tests real code paths, edge cases, and error handling
- Tests are executed automatically

### 🚀 Deployment Agent
- Generates deployment artifacts
- Outputs `Dockerfile` and `run.sh`
- Keeps configuration minimal and portable

### 🎨 UI Agent
- Generates a Streamlit UI
- Outputs `app_ui.py`
- Provides a simple interface to interact with the generated project

Architecture
```
graph TD
    A[Controller Agent] --> B[Requirements Agent]
    B --> C[Coding Agent]
    C --> D[Review Agent]
    D -- FIX_REQUIRED --> C
    D -- APPROVED --> E[Documentation Agent]
    E --> F[QA Agent]
    F --> G[Deployment Agent]
    G --> H[UI Agent]
```

## File Structure
```
project-root/
├── app.py # Main Streamlit application
├── workflow.py # Sequential multi-agent orchestrator
├── agents.py # Agent definitions and LLM configuration
├── utils/
│ ├── logger.py # Centralized logging
│ └── test_executor.py # Automated test runner
├── workspace/ # Generated project artifacts
│ ├── requirements.md
│ ├── main.py
│ ├── test_main.py
│ ├── README.md
│ ├── Dockerfile
│ └── app_ui.py
├── requirements.txt
├── .env.example
└── README.md
```

- Uses free-tier LLM access (rate/token limits apply)
- Long prompts may exceed token limits
- Not intended for production deployment
- Generated code quality depends on LLM output
- Streamlit Cloud limits execution time and resources

If a token limit is exceeded, the system will:
- Stop execution safely
- Display a clear error message
- Preserve all already-generated artifacts

## Project Intent
This project was created by **Saksham Jain** as a **learning and exploration exercise** in:
- Multi-agent system design
- LLM orchestration
- Deterministic AI workflows
- Tooling around automated software generation

This project is **not intended for monetization** or commercial use.

---

## Acknowledgements
- AutoGen (Microsoft)
- Streamlit
- Ollama
- OpenRouter
- Groq
