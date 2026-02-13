# Open Interpreter Codebase Analysis

## Overview
Open Interpreter is a Python library that enables Large Language Models (LLMs) to execute code locally. The project is organized into several key modules with clear separation of concerns.

## Project Structure

```
interpreter/
├── __init__.py                    # Main entry point, exports OpenInterpreter
├── core/                          # Core functionality
│   ├── core.py                    # OpenInterpreter main class
│   ├── async_core.py              # AsyncInterpreter for server/WebSocket
│   ├── respond.py                 # Main response loop
│   ├── default_system_message.py # Default system prompt
│   ├── llm/                       # Language Model integration
│   │   ├── llm.py                 # LLM wrapper class
│   │   ├── run_text_llm.py        # Text-only LLM execution
│   │   ├── run_tool_calling_llm.py # Tool-calling LLM execution
│   │   └── utils/                 # LLM utilities
│   ├── computer/                  # Computer control capabilities
│   │   ├── computer.py            # Main Computer class
│   │   ├── terminal/              # Terminal and language execution
│   │   │   ├── terminal.py        # Terminal class
│   │   │   └── languages/         # Language executors
│   │   │       ├── python.py      # Python executor
│   │   │       ├── javascript.py  # JavaScript executor
│   │   │       ├── shell.py       # Shell/Bash executor
│   │   │       ├── jupyter_language.py
│   │   │       └── ...            # Other language executors
│   │   ├── mouse.py               # Mouse control
│   │   ├── keyboard.py            # Keyboard control
│   │   ├── vision.py              # Computer vision
│   │   ├── browser.py             # Browser automation
│   │   ├── files.py               # File operations
│   │   └── ...                    # Other system capabilities
│   └── utils/                     # Core utilities
├── terminal_interface/            # CLI interface
│   ├── terminal_interface.py      # Main terminal UI
│   ├── magic_commands.py          # CLI magic commands
│   ├── profiles/                  # Configuration profiles
│   └── utils/                     # Terminal utilities
└── computer_use/                  # Computer use tools (for OS mode)
    ├── loop.py                    # Main loop for OS mode
    └── tools/                     # Tool implementations
```

## Key Components

### 1. OpenInterpreter Class (interpreter/core/core.py)
The main class that orchestrates everything:
- **chat()** - Main chat method (supports streaming)
- **_respond_and_store()** - Handles the response loop
- **computer** - Access to computer capabilities
- **llm** - Access to language model

### 2. LLM Module (interpreter/core/llm/)
Uses **LiteLLM** for unified API across providers:
- Supports 100+ LLM providers (OpenAI, Anthropic, Azure, local models, etc.)
- Auto-detects vision and function-calling capabilities
- Handles message formatting and token management

### 3. Computer Module (interpreter/core/computer/)
Provides system capabilities:
- **terminal** - Code execution in multiple languages
- **mouse/keyboard** - Input automation
- **vision** - Screen capture and OCR
- **browser** - Browser automation
- **files** - File operations
- **calendar, contacts, mail, sms** - Productivity apps
- **skills** - Custom skill definitions

### 4. Response Loop (interpreter/core/respond.py)
The main loop that:
1. Renders system message with capabilities
2. Sends messages to LLM
3. Receives code blocks
4. Executes code via terminal
5. Returns output to LLM
6. Repeats until task complete

## Supported Language Executors
Located in `interpreter/core/computer/terminal/languages/`:
- Python (`python.py`)
- JavaScript (`javascript.py`)
- Shell/Bash (`shell.py`)
- Jupyter (`jupyter_language.py`)
- AppleScript (`applescript.py`)
- PowerShell (`powershell.py`)
- HTML (`html.py`)
- Java (`java.py`)
- R (`r.py`)
- React (`react.py`)
- Ruby (`ruby.py`)
- Subprocess (`subprocess_language.py`)

## Message Protocol (LMC Messages)
The system uses LMC (Language Model Computer) messages format:
```python
{
    "role": "user" | "assistant" | "computer",
    "type": "message" | "code" | "console",
    "format": "output" | "active_line" | "image",
    "content": "..."
}
```

## Execution Flow
1. User sends message via `interpreter.chat()`
2. Message added to conversation history
3. `respond()` function builds system message with capabilities
4. LLM processes messages and returns code blocks
5. Code is extracted and sent to appropriate language executor
6. Output is captured and returned to LLM
7. Process repeats until task completion

## Key Entry Points
- **CLI**: `interpreter` command → `interpreter/terminal_interface/start_terminal_interface.py`
- **Python API**: `from interpreter import interpreter`
- **Server Mode**: `AsyncInterpreter` class for WebSocket/FastAPI

## Configuration
- Profiles in YAML format: `interpreter/terminal_interface/profiles/defaults/`
- Default profile: `default.yaml`
- Environment variables and command-line arguments

## Dependencies (key packages)
- **litellm** - Unified LLM API
- **pyautogui** - GUI automation
- **anthropic** - Anthropic API
- **selenium** - Browser automation
- **fastapi/uvicorn** - Server mode
- **rich** - Terminal formatting

## Development Notes
- Uses Poetry for package management
- Version: 0.4.3
- Python 3.9-3.12
- Optional extras: os, safe, local, server

## Next Steps for Development
1. Identify specific feature/modification requirements
2. Locate relevant module (core, terminal_interface, computer_use)
3. Make changes following the existing patterns
4. Test with different LLM providers and configurations
