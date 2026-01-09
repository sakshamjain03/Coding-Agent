# DataEconomy – Multi-Agent Coding Framework

A fully automated multi-agent system that converts natural-language software specifications into complete working projects using a deterministic agent pipeline.

The framework supports local LLMs via **Ollama** and cloud LLMs via **OpenRouter** and **Groq**.

---

## Features

- **Sequential Agent Pipeline:** Controller → Requirements → Coding → Review → Documentation → QA → Deployment → UI  
- **Fully Offline Mode:** Uses local LLMs via Ollama  
- **Cloud Support:** Integrated with OpenRouter or Groq  
- **Automatic File Extraction:** Uses robust file markers to parse output  
- **Automatic Unit-Test Execution:** Validates code integrity automatically  
- **Streamlit UI Interface:** Easy-to-use frontend  
- **Deterministic Bounded Review Loop:** Prevents infinite loops during code review  
- **Safe Termination:** Includes runaway protection mechanisms  

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