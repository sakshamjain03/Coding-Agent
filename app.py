import os
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'

import streamlit as st
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

from agents import create_all_agents
from workflow import run_workflow
from utils.logger import setup_logger, log_agent_action

st.set_page_config(
    page_title="Multi Agent Coding Framework",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

logger = setup_logger()
WORKSPACE_DIR = "workspace"


def check_environment():
    return True, ""


def validate_user_input(user_input: str):
    return True, ""


def cleanup_pycache():
    if os.path.exists(WORKSPACE_DIR):
        import shutil
        pycache_path = Path(WORKSPACE_DIR) / "__pycache__"
        if pycache_path.exists() and pycache_path.is_dir():
            try:
                shutil.rmtree(pycache_path)
            except Exception:
                pass


def clear_workspace():
    import shutil
    try:
        if os.path.exists(WORKSPACE_DIR):
            shutil.rmtree(WORKSPACE_DIR)
        os.makedirs(WORKSPACE_DIR, exist_ok=True)
        st.success("Workspace cleared.")
    except Exception as e:
        st.error(str(e))


def display_workspace_artifacts():
    cleanup_pycache()
    if not os.path.exists(WORKSPACE_DIR):
        st.info("No artifacts yet.")
        return

    files = [f for f in Path(WORKSPACE_DIR).glob("*") if f.name != "__pycache__"]
    for f in files:
        with st.expander(f.name):
            st.code(f.read_text(encoding="utf-8"), language="text")
            
def display_test_results(test_results: Dict[str, Any]):
    if not test_results:
        st.info("No test results available.")
        return

    st.subheader("🧪 Test Execution Results")

    status = test_results.get("status", "unknown")
    if status == "success":
        st.success("All tests executed successfully.")
    else:
        st.error("Test execution encountered errors.")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Tests", test_results.get("total_tests", 0))
    col2.metric("Passed", test_results.get("total_passed", 0))
    col3.metric("Failed", test_results.get("total_failed", 0))
    col4.metric("Errors", test_results.get("total_errors", 0))

    details = test_results.get("test_results", [])
    if details:
        st.markdown("### Detailed Output")
        for idx, item in enumerate(details, start=1):
            with st.expander(f"Test {idx}: {item.get('name', 'Unnamed Test')}"):
                st.code(item.get("output", ""), language="text")


def main():
    cleanup_pycache()
    st.title("🤖 AutoGen - Multi Agent Coding Framework")

    with st.sidebar:
        st.success("Environment validation disabled")
        if st.button("🗑️ Clear Workspace"):
            clear_workspace()
            if 'workflow_result' in st.session_state:
                del st.session_state['workflow_result']
            st.rerun()

    user_request = st.text_area("Describe the application you want to build:", height=150)

    if st.button("🚀 Launch Team") and user_request.strip():
        with st.spinner("Running workflow..."):
            agents = create_all_agents()
            result = run_workflow(user_request, agents)
            st.session_state['workflow_result'] = result
            st.rerun()

    if 'workflow_result' in st.session_state:
        res = st.session_state['workflow_result']
        if res['status'] == 'success':
            st.success("Workflow completed successfully.")
            display_test_results(res.get("test_results"))
        else:
            st.error(res.get("error"))


    st.header("📦 Generated Artifacts")
    display_workspace_artifacts()


if __name__ == "__main__":
    main()