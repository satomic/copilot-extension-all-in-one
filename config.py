import os

# GitHub
VERIFY_GITHUB = os.getenv("VERIFY_GITHUB", "False")
COPILOT_API_URL = os.getenv("COPILOT_API_URL", "https://api.githubcopilot.com/chat/completions")
COPILOT_PERSONALIZATION = "You are a cute little cat 🐱 who likes to act cute. You always use emoji to end your answer, for example 💗"

# Ollama
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434/api/chat")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")

# Qwen
QWEN_API_KEY = os.getenv("QWEN_API_KEY")
QWEN_API_URL = os.getenv("QWEN_API_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions")
QWEN_MODEL = os.getenv("QWEN_MODEL", "qwen-plus")

# DeepSeek
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_API_URL = os.getenv("DEEPSEEK_API_URL", "https://api.deepseek.com/chat/completions")
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

# Command Executor
CMD_EXECUTOR = os.getenv("CMD_EXECUTOR", "cmd.exe")