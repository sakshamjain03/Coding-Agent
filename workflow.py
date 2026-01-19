from typing import Dict, Any, Optional, List
from autogen import GroupChat, GroupChatManager, Agent
from utils.logger import setup_logger, log_agent_action, log_error_with_context

logger = setup_logger()


class WorkflowOrchestrator:
    
    def __init__(self, agents: Dict[str, Any], max_review_iterations: int = 5, progress_callback=None):
        self.agents = agents
        self.max_review_iterations = max_review_iterations
        self.review_iteration_count = 0
        self.progress_callback = progress_callback
        
        logger.info("WorkflowOrchestrator initialized")
        log_agent_action(
            logger,
            "System",
            "Configuration",
            f"Max review iterations: {max_review_iterations}"
        )
    
    def create_group_chat(self) -> GroupChat:
        agents_list = [
            self.agents["Controller_agent"],
            self.agents["Requirements_Agent"],
            self.agents["coding_agent"],
            self.agents["review_agent"],
            self.agents["Documentation_Agent"],
            self.agents["QA_Agent"],
            self.agents["Deployment_agent"],
            self.agents["UI_agent"],
        ]
        
        groupchat = GroupChat(
            agents=agents_list,
            messages=[],
            max_round=50,
        )
        
        logger.info(f"GroupChat created with {len(agents_list)} agents")
        return groupchat
    
    def create_manager(self, groupchat: GroupChat, llm_config: Dict[str, Any]) -> GroupChatManager:
        return GroupChatManager(groupchat=groupchat, llm_config=llm_config)
    
    def initiate_workflow(self, user_request: str) -> Dict[str, Any]:
        try:
            if not user_request or not user_request.strip():
                logger.error("Empty user request received")
                return {
                    "status": "error",
                    "error": "User request cannot be empty",
                    "review_iterations": 0,
                }
            
            logger.info("=" * 80)
            logger.info("WORKFLOW INITIATED")
            logger.info("=" * 80)
            log_agent_action(logger, "User", "Request", user_request[:100])
            
            from agents import get_llm_config
            llm_config = get_llm_config()
            
            groupchat = self.create_group_chat()
            manager = self.create_manager(groupchat, llm_config)
            for agent in self.agents.values():
                agent._oai_manager = manager
                
            logger.info("Starting agent conversation...")
            
            # self.agents["Controller_agent"].initiate_chat(
            #     manager,
            #     message=user_request,
            # )
            system_context = f"""
            You are Controller_agent in a multi-agent software factory.

            Rules:
            - Always produce files using:
            ===BEGIN_FILE:filename===
            <content>
            ===END_FILE===

            - Never respond empty.
            - Instruct next agent clearly.

            User Request:
            {user_request}
            """
            groupchat.messages.append({
                "role": "system",
                "content": system_context
            })
            groupchat.messages.append({
                "role": "assistant",
                "content": "Controller_agent: Requirements_Agent must generate requirements.md based on the user request."
            })
            
            pipeline = [
                "Requirements_Agent",
                "coding_agent",
                "review_agent",
                "Documentation_Agent",
                "QA_Agent",
                "Deployment_agent",
                "UI_agent",
            ]

            i = 0
            while i < len(pipeline):
                if i > 40:
                    raise RuntimeError("Workflow runaway detected — terminating safely.")
                role = pipeline[i]

                agent = self.agents[role]
                logger.info(f"Executing: {agent.name}")                
                if self.progress_callback:
                    self.progress_callback(role, "running")
                chat_history = [
                    {"role": m.get("role", "assistant"), "content": m.get("content", "")}
                    for m in groupchat.messages
                ]
                reply = agent.generate_reply(chat_history)
                logger.info(f"{agent.name} reply length: {len(str(reply)) if reply else 0}")
                if not reply or not str(reply).strip():
                    reply = "I will now generate the required files as instructed."

                if self.progress_callback:
                    self.progress_callback(role, "completed")
                if not reply or not str(reply).strip():
                    raise RuntimeError(f"{agent.name} produced empty output")
                groupchat.messages.append({
                    "role": "assistant",
                    "content": reply
                })
                if role == "review_agent" and "FIX_REQUIRED" in reply:
                    self.review_iteration_count += 1
                    if self.review_iteration_count < self.max_review_iterations:
                        pipeline.insert(i + 1, "coding_agent")
                    else:
                        logger.warning("Review limit reached — forcing approval")
                i += 1

            
            logger.info("=" * 80)
            logger.info("WORKFLOW COMPLETED - Extracting generated files...")
            logger.info("=" * 80)
            
            import re
            import os
            
            workspace_path = os.path.abspath("workspace")
            os.makedirs(workspace_path, exist_ok=True)
            
            files_extracted = 0
            for msg in groupchat.messages:
                content = msg.get("content", "")
                agent_name = msg.get("role", "assistant")
                
                file_pattern = r'===BEGIN_FILE:([^\s]+)===\s*\n(.*?)\n===END_FILE==='
                matches = re.findall(file_pattern, content, re.DOTALL)
                
                for filename, file_content in matches:
                    try:
                        filename = filename.strip()
                        
                        file_content = file_content.strip()
                        filepath = os.path.join(workspace_path, filename)
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(file_content)
                        
                        logger.info(f"[{agent_name}] Extracted file: {filename} ({len(file_content)} chars)")
                        files_extracted += 1
                    except Exception as e:
                        logger.warning(f"[{agent_name}] Failed to extract {filename}: {str(e)}")
            
            logger.info(f"Extracted {files_extracted} files to workspace (no code execution)")
            
            if files_extracted == 0:
                logger.warning("No files were extracted from agent responses!")
                logger.warning("Check if agents are following the expected code generation format.")
                logger.debug(f"Total messages: {len(groupchat.messages)}")
                for i, msg in enumerate(groupchat.messages):
                    if '```python' in msg.get("content", ""):
                        logger.debug(f"Message {i} from {msg.get('name', 'unknown')} contains Python code")
            
            test_results = None
            try:
                from utils.test_executor import run_tests_in_workspace
                logger.info("=" * 80)
                logger.info("EXECUTING TESTS")
                logger.info("=" * 80)
                test_results = run_tests_in_workspace(workspace_path)
                logger.info(f"Test execution completed: {test_results.get('status')}")
                logger.info(f"Total tests: {test_results.get('total_tests', 0)}, "
                           f"Passed: {test_results.get('total_passed', 0)}, "
                           f"Failed: {test_results.get('total_failed', 0)}, "
                           f"Errors: {test_results.get('total_errors', 0)}")
            except Exception as e:
                logger.warning(f"Test execution failed: {str(e)}")
                test_results = {
                    'status': 'error',
                    'message': f'Failed to execute tests: {str(e)}',
                    'total_tests': 0,
                    'total_passed': 0,
                    'total_failed': 0,
                    'total_errors': 0,
                    'test_results': []
                }
            
            return {
                "status": "success",
                "total_messages": len(groupchat.messages),
                "review_iterations": self.review_iteration_count,
                "files_extracted": files_extracted,
                "messages": groupchat.messages,
                "test_results": test_results,
            }
            
        except KeyboardInterrupt:
            logger.warning("Workflow interrupted by user")
            return {
                "status": "error",
                "error": "Workflow was interrupted by user",
                "review_iterations": self.review_iteration_count,
            }
        except TimeoutError as e:
            log_error_with_context(logger, e, "Workflow timeout")
            return {
                "status": "error",
                "error": f"Workflow timed out: {str(e)}",
                "review_iterations": self.review_iteration_count,
            }
        except ValueError as e:
            log_error_with_context(logger, e, "Invalid configuration")
            return {
                "status": "error",
                "error": f"Configuration error: {str(e)}",
                "review_iterations": self.review_iteration_count,
            }
        except ConnectionError as e:
            log_error_with_context(logger, e, "Network connection failed")
            return {
                "status": "error",
                "error": f"Connection error: {str(e)}. Please check your internet connection.",
                "review_iterations": self.review_iteration_count,
            }
        except Exception as e:
            log_error_with_context(logger, e, "Workflow execution failed")
            error_type = type(e).__name__
            return {
                "status": "error",
                "error": f"{error_type}: {str(e)}",
                "review_iterations": self.review_iteration_count,
            }


def run_workflow(user_request: str, agents: Dict[str, Any], progress_callback=None) -> Dict[str, Any]:
    orchestrator = WorkflowOrchestrator(agents, max_review_iterations=5, progress_callback=progress_callback)
    return orchestrator.initiate_workflow(user_request)