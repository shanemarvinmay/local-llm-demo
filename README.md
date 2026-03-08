# local-llm-demo - Cortana (Budget Edition)

Run a local LLM with Ollama, benchmark latency and rough throughput, and chat with a lightweight "Cortana (Budget Edition)" persona.

## What this repo includes

- `bench.py`: Simple benchmark against Ollama using the Python SDK.
- `cortana_chat.py`: Interactive local chat loop with a system persona.
- `ollama_runtime.py`: Shared runtime helpers (service check/start + model check/pull).
- `prompts/`: Example prompts for coding, summarizing, and extraction.
- `requirements.txt`: Python dependency list (`ollama`).

## Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com/) installed (CLI in your PATH)

Both scripts use a fixed model: `deepseek-r1:14b`.
If it is not present locally, the scripts auto-pull it on first run.

## Quickstart

1. Create and activate a virtual environment.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

On macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies.

```bash
pip install -r requirements.txt
```

## Run the benchmark

```bash
python bench.py --prompt "Write a Python function to dedupe a list while preserving order."
```

Optional arguments:

- `--runs` (default: `3`)
- `--system` (default: `You are a helpful assistant.`)

The benchmark prints:

- Per-run latency
- Approximate tokens/second
- p50 and "p95-ish" latency across runs

## Run Cortana chat

```bash
python cortana_chat.py
```

Type `exit` or `quit` to stop the session.

## Prompt files

Sample prompt starters are provided in:

- `prompts/01_coding.txt`
- `prompts/02_summarize.txt`
- `prompts/03_extract.txt`

## Troubleshooting

- `Could not connect to Ollama at http://localhost:11434`:
  - Start Ollama manually with `ollama serve`, or rerun and let the script try best-effort auto-start.
- `Failed to pull model 'deepseek-r1:14b'`:
  - Check internet access and disk space, then run `ollama pull deepseek-r1:14b` manually.
- Slow responses:
  - Close other heavy workloads on your machine.

## Notes

- Throughput uses a rough token estimate (`~4 chars/token`) for quick comparisons.
- Calls run through the local Ollama service at `http://localhost:11434` via the Ollama Python SDK.