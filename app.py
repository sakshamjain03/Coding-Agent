import os
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

import streamlit as st
from pathlib import Path
from typing import Dict, Any

from agents import create_all_agents
from workflow import run_workflow
from utils.logger import setup_logger

# ================== CONFIG ==================
st.set_page_config(
    page_title="AI Software Team",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

logger = setup_logger()
WORKSPACE_DIR = "workspace"


# ================== HELPERS ==================
def cleanup_pycache():
    if os.path.exists(WORKSPACE_DIR):
        import shutil
        pycache = Path(WORKSPACE_DIR) / "__pycache__"
        if pycache.exists():
            try:
                shutil.rmtree(pycache)
            except Exception:
                pass


def clear_workspace():
    import shutil
    if os.path.exists(WORKSPACE_DIR):
        shutil.rmtree(WORKSPACE_DIR)
    os.makedirs(WORKSPACE_DIR, exist_ok=True)
    st.success("Workspace cleared successfully.")


def is_token_limit_error(msg: str) -> bool:
    if not msg:
        return False
    msg = msg.lower()
    return any(
        k in msg
        for k in [
            "rate limit",
            "token",
            "tokens per day",
            "429",
            "limit reached",
            "rate_limit_exceeded",
        ]
    )

def display_test_results(test_results: Dict[str, Any]):
    if not test_results:
        st.info("No test results available.")
        return

    st.subheader("🧪 Test Execution Results")

    status = test_results.get("status", "unknown")
    if status in ["passed", "success"]:
        st.success("All tests executed successfully.")
    else:
        st.error("Some tests failed or encountered errors.")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Tests", test_results.get("total_tests", 0))
    c2.metric("Passed", test_results.get("total_passed", 0))
    c3.metric("Failed", test_results.get("total_failed", 0))
    c4.metric("Errors", test_results.get("total_errors", 0))

    for idx, item in enumerate(test_results.get("test_results", []), start=1):
        with st.expander(f"Test File {idx}: {item.get('file', 'unknown')}"):
            st.code(item.get("output", ""), language="text")


def display_workspace_artifacts():
    cleanup_pycache()
    if not os.path.exists(WORKSPACE_DIR):
        st.info("No generated files yet.")
        return

    files = list(Path(WORKSPACE_DIR).glob("*"))

    groups = {
        "📄 Core Code": ["main.py"],
        "🧪 Tests": ["test_main.py"],
        "📘 Documentation": ["README.md", "requirements.md"],
        "🚀 Deployment": ["Dockerfile", "run.sh"],
        "🎨 UI": ["app_ui.py"],
    }

    for title, names in groups.items():
        matched = [f for f in files if f.name in names]
        if matched:
            st.subheader(title)
            for f in matched:
                expanded = f.name.lower() == "readme.md"
                with st.expander(f.name, expanded=expanded):
                    st.code(f.read_text(encoding="utf-8"), language="text")


def launch_generated_ui_section():
    ui_path = os.path.join(WORKSPACE_DIR, "app_ui.py")

    st.subheader("🎨 Preview the Generated Application")

    if not os.path.exists(ui_path):
        st.info("No UI was generated for this project.")
        return

    st.success("A Streamlit UI was generated specifically for your application.")

    st.markdown(
        """
You can run this UI **locally** using the command below.
"""
    )

    st.code(f"streamlit run {ui_path}", language="bash")

    st.caption(
        "Auto-launch works only on local machines. "
        "Streamlit Cloud does not allow starting nested apps."
    )


# ================== SIDEBAR ==================
with st.sidebar:
    st.title("⚙️ Controls")

    st.markdown(
        """
🧹 **Workspace Reset (Recommended)**

To avoid file conflicts:
- Clear workspace **before starting**
- Clear workspace **after finishing**
"""
    )

    if st.button("🗑️ Clear Workspace"):
        clear_workspace()

    st.divider()
    st.markdown(
        """
**Author:** Saksham Jain  
**Purpose:** Learning & demonstration  
**Not for monetization**
"""
    )


# ================== UI ==================
cleanup_pycache()

tabs = st.tabs(
    ["🏠 Introduction", "📘 Project Knowledge", "🛠️ Build Application"]
)

# ---------------- INTRO ----------------
with tabs[0]:
    st.title("🤖 Your AI Software Engineering Team")

    st.markdown(
        """
### Turn ideas into complete software projects

This system simulates a **real software engineering team** powered by AI.

You describe **what you want to build**, and the team:
- Plans requirements
- Writes production Python code
- Reviews quality & security
- Generates tests
- Creates documentation
- Prepares deployment files
- Builds a UI
"""
    )

    st.info(
        """
📌 **Project Note**

Created by **Saksham Jain** for **learning and exploration** of
multi-agent systems and software workflows.

This project is **not intended for commercial or monetization use**.
"""
    )

    st.subheader("👥 Meet Your AI Team")

    st.markdown(
        """
- **AI Product Manager**
- **Requirements Analyst**
- **Software Engineer**
- **Code Reviewer**
- **QA Engineer**
- **DevOps Engineer**
- **UI Engineer**

Each agent has **one clear responsibility**, mirroring real teams.
"""
    )


# ---------------- KNOWLEDGE ----------------
with tabs[1]:
    st.title("📘 Architecture & Key Decisions")

    with st.expander("Why a Sequential Workflow?", expanded=True):
        st.markdown(
            """
Software development is **dependency-driven**.

You cannot:
- Test code before it exists
- Review code without requirements
- Document unstable logic

A sequential pipeline ensures:
- Deterministic execution
- Predictable quality
- Controlled review loops
- Production-style discipline
"""
        )

    st.subheader("🏗️ Workflow")

    st.code(
        """
User Input
 ↓
Controller Agent
 ↓
Requirements Agent → requirements.md
 ↓
Coding Agent → main.py
 ↓
Review Agent
 ├─ FIX_REQUIRED → Coding Agent
 └─ APPROVED
 ↓
Documentation Agent → README.md
 ↓
QA Agent → test_main.py
 ↓
Deployment Agent → Dockerfile, run.sh
 ↓
UI Agent → app_ui.py
 ↓
Workspace + Test Execution
""",
        language="text",
    )


# ---------------- APP ----------------
with tabs[2]:
    st.title("🛠️ Build Your Application")

    st.markdown(
        """
Describe **what you want to build** in plain English.

You do **not** need to specify:
- Libraries
- Architecture
- Design patterns
"""
    )

    st.markdown("**Try an example:**")
    c1, c2, c3 = st.columns(3)
    if c1.button("LRU Cache"):
        st.session_state.user_request = (
            "Build a Python LRU Cache with unit tests."
        )
    if c2.button("Todo App"):
        st.session_state.user_request = (
            "Create a Python command-line todo application."
        )
    if c3.button("File Manager"):
        st.session_state.user_request = (
            "Build a Python tool to manage files and folders."
        )

    user_request = st.text_area(
        "Your application description:",
        height=160,
        value=st.session_state.get("user_request", ""),
        placeholder="Example: Build a Python module implementing an LRU Cache.",
    )

    if st.button("🚀 Launch AI Team") and user_request.strip():
        progress_container = st.empty()
        agent_log_container = st.container()

        AGENT_ORDER = [
            "Controller_agent",
            "Requirements_Agent",
            "coding_agent",
            "review_agent",
            "Documentation_Agent",
            "QA_Agent",
            "Deployment_agent",
            "UI_agent",
        ]

        agent_status = {a: "pending" for a in AGENT_ORDER}

        def progress_callback(agent_name: str, state: str):
            agent_status[agent_name] = state

            with progress_container:
                st.subheader("🔄 Live Execution Status")

                for agent in AGENT_ORDER:
                    status = agent_status[agent]
                    if status == "completed":
                        st.success(f"✅ {agent.replace('_', ' ')} completed")
                    elif status == "running":
                        st.info(f"⏳ {agent.replace('_', ' ')} running")
                    else:
                        st.write(f"• {agent.replace('_', ' ')} pending")

        with st.spinner("AI team is working..."):
            agents = create_all_agents()
            result = run_workflow(
                user_request,
                agents,
                progress_callback=progress_callback
            )
            st.session_state.workflow_result = result
            st.rerun()
            
    if "workflow_result" in st.session_state:
        res = st.session_state.workflow_result

        if res["status"] == "success":
            st.success("Your project is ready.")
            display_test_results(res.get("test_results"))
        else:
            msg = res.get("error", "Unknown error.")
            if is_token_limit_error(msg):
                st.warning(
                    """
⚠️ **Free-Tier AI Limit Reached**

This demo runs on **free-tier LLM access**.

Your request exceeded the allowed usage.
You can:
- Retry later
- Use a smaller request
- Run locally with Ollama
"""
                )
            else:
                st.error(msg)

    st.divider()
    st.header("📂 Generated Project Files")
    display_workspace_artifacts()   
    st.divider()
    launch_generated_ui_section()