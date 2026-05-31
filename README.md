# AI Code Generator

A lightweight autonomous agent that uses the Gemini API to execute development tasks and run tools from a Python CLI.

## Overview

This project provides a small framework for building an LLM-driven tool executor. It sends user prompts to Gemini with a system prompt and parses JSON-formatted actions from the assistant to run:

- `python(code)` to execute inline Python
- `terminal(command)` to run shell commands
- `write_file(filename, content)` to write files

## Files

- `main.py` — main CLI loop that sends user input to Gemini, parses responses, and executes tool actions.
- `system_prompt.py` — system prompt with tool definitions and agent behavior.
- `tools.py` — tool implementations and dispatch helpers.
- `config.py` — OpenAI/Gemini client setup using environment variables.

## Setup

1. Install Python 3.10+.
2. Create and activate a virtual environment (recommended):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Install dependencies:

```powershell
pip install openai python-dotenv
```

4. Create a `.env` file in the project root with your Gemini API key:

```text
GEMINI_API_KEY=your_api_key_here
```

## Usage

Run the CLI:

```powershell
python main.py
```

Then enter instructions for the agent. To exit, type `exit` or `quit`.

## Notes

- The assistant response must be valid JSON with a `goal` and `actions` array.
- Tool calls are executed directly from the parsed JSON payload.
- This project is intended as a minimal prototype for tool-enabled LLM workflows.

## License

MIT
