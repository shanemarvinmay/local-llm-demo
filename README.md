# local-llm-demo

Small local-Ollama demos for two common workflows:

- running a directory of prompt files and comparing rough token costs
- chatting with a lightweight "Cortana (Budget Edition)" persona

## What is in this repo

- `bench.py`: Runs every `.txt` file in `prompts/` against a local Ollama model.
- `cortana_chat.py`: Starts an interactive local chat session.
- `ollama_runtime.py`: Shared Ollama startup, model-check, and cleanup helpers.
- `prompts/`: Example prompts for coding, summarizing, and extraction.

## Requirements

- Python 3.10+
- [Ollama](https://ollama.com/) installed and available on your PATH

Both scripts use fixed defaults:

- Model: `deepseek-r1:14b`
- Host: `http://localhost:11434`

## Quickstart

Create and activate a virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

On macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install the dependency:

```bash
pip install -r requirements.txt
```

## Run the prompt demo

This runs each `.txt` file in `prompts/` and prints the prompt, model output, and a rough token/cost summary.

```bash
python bench.py
```

`bench.py` always reads `.txt` files from `prompts/` and uses the built-in system prompt.

## Run the chat demo

```bash
python cortana_chat.py
```

Type `exit` or `quit` to stop. `Ctrl+C` and `Ctrl+D` also exit cleanly.

## First-run behavior

- If Ollama is not already running, the scripts try a best-effort `ollama serve`.
- If the configured model is not installed locally, the scripts try to pull it automatically.
- After the script exits, it makes a best-effort attempt to stop the active model process.

## Prompt files

Included examples:

- `prompts/01_coding.txt`
- `prompts/02_summarize.txt`
- `prompts/03_extract.txt`

Add your own `.txt` files to `prompts/` to include them in the run.

## Troubleshooting

`Could not connect to Ollama at http://localhost:11434`

- Start Ollama manually with `ollama serve`
- Confirm the service is listening on the same host as `OLLAMA_HOST`

`Ollama service is not reachable and the 'ollama' CLI was not found in PATH`

- Install Ollama
- Restart your shell so the `ollama` command is available

`Failed to pull model ...`

- Check internet access
- Check free disk space
- Try `ollama pull <model>` manually

Very slow responses or model load failures

- `deepseek-r1:14b` is a large default model
- If you need a different model, change `DEFAULT_MODEL` in `ollama_runtime.py`

## Notes

- The cost output in `bench.py` is only a rough comparison, not billing-grade accounting.
- Token counts come from Ollama response metadata when available.
- This project currently has no automated test suite; verification is limited to static checks and manual runs against a local Ollama instance.
