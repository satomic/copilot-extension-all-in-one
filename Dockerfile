FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Environment variables with defaults
ENV VERIFY_GITHUB=False
ENV COPILOT_API_URL=https://api.githubcopilot.com/chat/completions
ENV OLLAMA_API_URL=http://host.docker.internal:11434/api/chat
ENV OLLAMA_MODEL=llama3.2
ENV QWEN_API_URL=https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions
ENV QWEN_MODEL=qwen-plus
ENV DEEPSEEK_API_URL=https://api.deepseek.com/v1/chat/completions
ENV DEEPSEEK_MODEL=deepseek-chat
ENV CMD_EXECUTOR=sh

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]