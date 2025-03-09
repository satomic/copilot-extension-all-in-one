from flask import Flask, jsonify, request
from asgiref.wsgi import WsgiToAsgi
from actions import Actions
import sys, os, json

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

import utils.github_utils as github_utils
from utils.log_utils import *

logger = configure_logger(with_date_folder=False)
logger.info('-----------------Starting-----------------')

flask_app = Flask(__name__)
app = WsgiToAsgi(flask_app)

@flask_app.post("/")
def stream():
    github_handler = github_utils.GitHubHandler(request)
    if not github_handler.verify_github_signature():
        return jsonify({"error": "Request must be from GitHub"}), 403

    user_login = github_handler.get_user_login()
    logger.info(f"User login: {user_login}")

    x_github_token = request.headers["x-github-token"]
    payload = request.get_json()

    request_data = request.data.decode('utf-8') if isinstance(request.data, bytes) else request.data
    logger.info(json.dumps(json.loads(request_data), indent=4, ensure_ascii=False))

    action = Actions(x_github_token)
    
    if payload.get("messages") and payload["messages"]:
        last_message = payload["messages"][-1]
        content = last_message.get("content", "").strip()
        
        copilot_references = last_message.get("copilot_references", [])
        references_file = ""
        references_selection = ""
        if copilot_references:
            for reference in copilot_references:
                if reference.get("type") == "client.file":
                    references_file = references_file + reference.get("data", {}).get("content", "") + "\n\n"
                if reference.get("type") == "client.selection":
                    references_selection = references_selection + reference.get("data", {}).get("content", "") + "\n\n"

        if last_message.get("role") == "user":
            # Check for help command (case insensitive)
            if content.lower() == "help":
                logger.info("help: Showing help information")
                return action.help(), {"Content-Type": "text/event-stream"}
                
            # Map prefixes to action functions
            prefix_map = {
                "cmd:": action.execute_command,
                "ollama:": action.ollama,
                "qwen:": action.qwen,
                "deepseek:": action.deepseek
            }
            
            for prefix, handler in prefix_map.items():
                if content.startswith(prefix):
                    action_name = prefix[:-1]
                    message = content[len(prefix):].strip()
                    if prefix != "cmd:":
                        if references_selection:
                            message = f"{message}\n\nreferences_selection content:{references_selection}"
                        if references_file:
                            message = f"{message}\n\nreferences_file content:{references_file}"
                    payload["messages"][-1]["content"] = message
                    logger.info(f"{action_name}: {payload['messages'][-1]['content']}")
                    return handler(payload["messages"]), {"Content-Type": "text/event-stream"}
            
            # Default to copilot
            logger.info(f"copilot: {content}")
            return action.copilot(payload["messages"]), {"Content-Type": "text/event-stream"}
    
    logger.info("No messages to process.")
    return jsonify({"error": "No messages to process."}), 400
