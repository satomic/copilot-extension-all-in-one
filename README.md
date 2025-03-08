# GitHub Copilot Extensions Python

This project provides extension capabilities for GitHub Copilot, enabling you to add custom functionalities beyond the standard Copilot features, such as executing command line instructions, interacting with local or third-party AI models, and more.

## Features

This extension supports the following key features:

1. **Native GitHub Copilot Support**: Direct interaction with GitHub Copilot for responses
2. **Command Line Execution**: Execute operating system commands using special prefixes
3. **Ollama Integration**: Connect to local Ollama models for conversations
4. **Alibaba Cloud Qwen Integration**: Utilize Alibaba Cloud's Qwen AI model

## Installation and Setup

### Prerequisites

- Python 3.11 or higher
- Valid GitHub Copilot account and Token
- (Optional) [Local Ollama installation](https://ollama.com/)
- (Optional) Alibaba Cloud Qwen API Key

### Installation Steps

1. Install required dependencies:

    ```bash
    python -m pip install -r requirements.txt
    ```

2. Configure environment variables (if using Qwen):

    ```bash
    set QWEN_API_KEY=your_api_key_here
    ```

3. Start the service:

    ```bash
    uvicorn main:app --reload
    ```

## Usage

The extension differentiates between features using different command prefixes:

### Default Mode (GitHub Copilot)

Simply input your question to get a response from GitHub Copilot:

```
How can I implement a simple HTTP server in Python?
```

### Command Execution Mode

Use the `cmd:` prefix to execute operating system commands:

```
cmd: dir
cmd: python --version
cmd: git status
```

### Ollama Mode

Use the `ollama:` prefix to access your local Ollama model:

```
ollama: Please explain the basic principles of quantum computing
```

### Qwen Mode

Use the `qwen:` prefix to access the Alibaba Cloud Qwen model:

```
qwen: Write a poem about artificial intelligence
```

## Configuration Options

You can modify the following configurations in the `config.py` file:

- **GitHub Settings**:
  - `VERIFY_GITHUB`: Whether to verify GitHub request signatures
  - `GITHUB_API_URL`: GitHub Copilot API endpoint

- **Ollama Settings**:
  - `OLLAMA_API_URL`: Ollama API endpoint
  - `OLLAMA_MODEL`: Ollama model name to use

- **Qwen Settings**:
  - `QWEN_API_URL`: Qwen API endpoint
  - `QWEN_MODEL`: Qwen model version to use

- **Command Execution Settings**:
  - `CMD_EXECUTOR`: Command line executor (default is `cmd.exe`)

## Advanced Features

### File References or Selected Content

When referencing files or selected code segments in your message, this content is automatically included in the request, enabling AI models to provide more targeted responses based on the context.

### Response Streaming

All models support streaming responses, allowing you to see AI-generated content in real-time.

## Frequently Asked Questions

1. **Q: How do I connect after starting the service?**  
   A: The service starts by default on localhost:8000 and can be accessed via HTTP POST requests.

2. **Q: How do I change the Ollama model?**  
   A: Modify the `OLLAMA_MODEL` parameter in the `config.py` file.

3. **Q: How do I handle API access limitations?**  
   A: For third-party services like Qwen, make sure to follow their API usage limits and rate requirements.

## Extension Development

To add new AI model integrations, add new handler methods in `actions.py` and register new prefixes in the `prefix_map` in `main.py`.

