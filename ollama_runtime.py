import subprocess
import time
from typing import Any

from ollama import Client

DEFAULT_MODEL = "deepseek-r1:14b"
OLLAMA_HOST = "http://localhost:11434"


def create_client() -> Client:
    return Client(host=OLLAMA_HOST)


def _model_names(models_payload: Any) -> set[str]:
    names: set[str] = set()
    if isinstance(models_payload, dict):
        models = models_payload.get("models", [])
    else:
        models = getattr(models_payload, "models", [])

    for item in models:
        if isinstance(item, dict):
            model = item.get("model")
            name = item.get("name")
        else:
            model = getattr(item, "model", None)
            name = getattr(item, "name", None)

        if isinstance(model, str):
            names.add(model)
        if isinstance(name, str):
            names.add(name)
    return names


def ensure_ollama_running(client: Client, retries: int = 10, wait_s: float = 0.5) -> None:
    try:
        client.list()
        return
    except Exception:
        pass

    try:
        subprocess.Popen(
            ["ollama", "serve"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except FileNotFoundError as exc:
        raise RuntimeError(
            "Ollama service is not reachable and the 'ollama' CLI was not found in PATH."
        ) from exc
    except Exception:
        # If startup command fails for any reason, we still run retries below.
        pass

    for _ in range(retries):
        time.sleep(wait_s)
        try:
            client.list()
            return
        except Exception:
            continue

    raise RuntimeError(
        "Could not connect to Ollama at http://localhost:11434. "
        "Please start it with 'ollama serve' and try again."
    )


def ensure_model_available(client: Client, model: str = DEFAULT_MODEL) -> str:
    try:
        current = client.list()
    except Exception as exc:
        raise RuntimeError("Unable to query local Ollama models.") from exc

    if model in _model_names(current):
        return model

    print(f"Model '{model}' not found locally. Pulling it now (one-time)...")
    try:
        client.pull(model=model)
    except Exception as exc:
        raise RuntimeError(
            f"Failed to pull model '{model}'. Check network/disk and try: ollama pull {model}"
        ) from exc
    return model


def unload_model(client: Client, model: str = DEFAULT_MODEL) -> None:
    """Stop a running model process via Ollama CLI."""
    try:
        subprocess.run(
            ["ollama", "stop", model],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
    except Exception:
        # Best-effort cleanup: exiting should not fail if unload is unavailable.
        pass
