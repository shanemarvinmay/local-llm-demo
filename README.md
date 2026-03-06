# local-llm-demo - Cortana (Budget Edition)

Run a local LLM with Ollama, benchmark latency and rough throughput, and chat with a lightweight "Cortana (Budget Edition)" persona.

## What this repo includes

- `bench.py`: Simple benchmark against Ollama's chat API.
- `cortana_chat.py`: Interactive local chat loop with a system persona.
- `prompts/`: Example prompts for coding, summarizing, and extraction.
- `requirements.txt`: Python dependency list (`requests`).

## Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com/) installed and running
- At least one local model pulled in Ollama (examples below use `qwen2.5:14b`)

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

3. Pull a model in Ollama (one-time).

```bash
ollama pull qwen2.5:14b
```

## Run the benchmark

```bash
python bench.py --model qwen2.5:14b --prompt "Write a Python function to dedupe a list while preserving order."
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
python cortana_chat.py --model qwen2.5:14b
```

Type `exit` or `quit` to stop the session.

## Prompt files

Sample prompt starters are provided in:

- `prompts/01_coding.txt`
- `prompts/02_summarize.txt`
- `prompts/03_extract.txt`

## Troubleshooting

- `Connection refused` to `localhost:11434`:
  - Start Ollama and confirm it is running.
- `model not found`:
  - Pull the model first (for example, `ollama pull qwen2.5:14b`).
- Slow responses:
  - Use a smaller model or reduce concurrent workloads.

## Notes

- Throughput uses a rough token estimate (`~4 chars/token`) for quick comparisons.
- All calls are local to your machine via `http://localhost:11434/api/chat`.
