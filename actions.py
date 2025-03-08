import httpx
import json
import subprocess
import config


class Actions():

    def __init__(self, x_github_token):
        self.x_github_token = x_github_token
        self.messages = []

    def copilot(self, messages):
        self.messages = messages
        self.messages.insert(
            0,
            {
                "role": "system",
                "content": config.COPILOT_PERSONALIZATION,
            },
        )
        headers = {
            "Authorization": f"Bearer {self.x_github_token}",
            "Content-Type": "application/json",
        }
        data = {
            "messages": self.messages, 
            "stream": True
        }
        with httpx.stream(
            "POST",
            config.COPILOT_API_URL,
            headers=headers,
            json=data,
        ) as response:
            for chunk in response.iter_lines():
                if chunk:
                    yield f"{chunk}\n\n"

    def ollama(self, messages):
        self.messages = messages
        data = {
            "model": config.OLLAMA_MODEL,
            "messages": self.messages, 
            "stream": True
        }
        with httpx.stream(
            "POST",
            config.OLLAMA_API_URL,
            json=data,
            timeout=120.0,
        ) as response:
            for chunk in response.iter_lines():
                if chunk:
                    try:
                        # Parse the JSON chunk
                        json_chunk = json.loads(chunk)
                        content = json_chunk.get("message", {}).get("content", "")
                        print(content)
                        done = json_chunk.get("done", False)
                        
                        # Format in OpenAI compatible format with 'choices' field
                        if done:
                            # Final message when stream is complete
                            data_dict = {
                                "choices": [{
                                    "finish_reason": "stop",
                                    "index": 0,
                                    "delta": {}
                                }]
                            }
                        else:
                            # Stream content format
                            data_dict = {
                                "choices": [{
                                    "delta": {"content": content},
                                    "index": 0
                                }]
                            }
                        
                        # Convert to JSON and yield in SSE format
                        yield f"data: {json.dumps(data_dict)}\n\n"
                    except json.JSONDecodeError:
                        # In case of malformed JSON
                        continue

    def execute_command(self, messages):
        self.messages = messages
        # Get the last prompt from messages list
        if not self.messages or len(self.messages) == 0:
            error_msg = "No messages found."
            yield self._format_response(error_msg, is_error=True)
            return
            
        last_message = self.messages[-1]
        if last_message.get("role") != "user":
            error_msg = "Last message is not from user."
            yield self._format_response(error_msg, is_error=True)
            return
        
        # Get the command to execute
        command = last_message.get("content", "").strip()
        
        # Begin response with command echo and opening code block
        yield self._format_response(f"Executing command: {command}\n\n```\n")
        
        try:
            # Execute the command through cmd.exe
            process = subprocess.Popen(
                [config.CMD_EXECUTOR, command] if config.CMD_EXECUTOR != 'cmd.exe' else [config.CMD_EXECUTOR, '/c', command],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Stream stdout in real-time
            for line in process.stdout:
                yield self._format_response(line)
                
            # Get any remaining stderr
            stderr = process.stderr.read()
            if stderr:
                yield self._format_response(f"\nErrors:\n{stderr}")
                
            # Wait for process to complete
            process.wait()
            
            # Send completion message and close code block
            yield self._format_response(f"\nCommand completed with exit code: {process.returncode}\n")
            
            # Send stop message
            yield self._format_stop_response()
            
        except Exception as e:
            # Close the code block even on error
            error_msg = f"Error executing command: {str(e)}\n```"
            yield self._format_response(error_msg, is_error=True)
            yield self._format_stop_response()
    
    def _format_response(self, content, is_error=False):
        """Format response in the expected structure for Copilot"""
        if is_error:
            content = f"ERROR: {content}"
            
        data_dict = {
            "choices": [{
                "delta": {"content": content},
                "index": 0
            }]
        }
        return f"data: {json.dumps(data_dict)}\n\n"
    
    def _format_stop_response(self):
        """Format the final stop message"""
        data_dict = {
            "choices": [{
                "finish_reason": "stop",
                "index": 0,
                "delta": {}
            }]
        }
        return f"data: {json.dumps(data_dict)}\n\n"

    # https://help.aliyun.com/zh/model-studio/developer-reference/use-qwen-by-calling-api#d059267ec7867
    def qwen(self, messages):
        self.messages = messages
        headers = {
            "Authorization": f"Bearer {config.QWEN_API_KEY}",
            "Content-Type": "application/json",
        }
        data = {
            "model": config.QWEN_MODEL,
            "messages": self.messages, 
            "stream": True
        }
        try:
            with httpx.stream(
                "POST",
                config.QWEN_API_URL,
                headers=headers,
                json=data,
            ) as response:
                if response.status_code == 401:
                    error_msg = "Qwen API request failed: Unauthorized 401, please check whether API_KEY is valid."
                    yield self._format_response(error_msg, is_error=True)
                    yield self._format_stop_response()
                    return

                response.raise_for_status()

                for chunk in response.iter_lines():
                    if chunk:
                        yield f"{chunk}\n\n"

        except httpx.HTTPError as e:
            error_msg = f"Qwen API request exception: {str(e)}"
            yield self._format_response(error_msg, is_error=True)
            yield self._format_stop_response()

