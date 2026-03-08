from pathlib import Path
from ollama import Client
from ollama_runtime import (
    DEFAULT_MODEL,
    create_client,
    ensure_model_available,
    ensure_ollama_running,
    unload_model,
)

total_tokens = 0

def chat(client: Client, prompt: str, system: str | None = None, temperature: float = 0.2) -> str:
    global total_tokens
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    response = client.chat(
        model=DEFAULT_MODEL,
        messages=messages,
        think=True,
        options={"temperature": temperature},
    )
    total_tokens += response.prompt_eval_count + response.eval_count    
    return response["message"]["content"]


def main():
    # Setting up LLM
    client = create_client()
    try:
        ensure_ollama_running(client)
        ensure_model_available(client, DEFAULT_MODEL)
        # Loading prompts
        prompts_dir = Path("prompts")
        prompt_files = sorted(prompts_dir.glob("*.txt"))
        if not prompt_files:
            raise SystemExit(f"No prompt files found in: {prompts_dir.resolve()}")

        print(f"Model: {DEFAULT_MODEL}")
        system_description = "You are a helpful assistant."
        print("----")

        for i, prompt_file in enumerate(prompt_files, start=1):
            prompt = prompt_file.read_text(encoding="utf-8").strip()
            if not prompt:
                print(f"Prompt {i}: {prompt_file.name} skipped (empty file)")
                continue

            resp = chat(client, prompt, system=system_description)

            print(f"Prompt {i}: {prompt_file.name}")

            # TODO: Remov
            print(prompt, '\n')
            print('LLM Response:')
            print(resp, '\n')
            print('~' * 100)
            break

        # Creating report on token usage
        if total_tokens == 0:
            raise SystemExit("No non-empty prompts were found to run.")

        print("----")
        print(f"Total output tokens: {total_tokens}")
        anthropic_cost = round(15 * total_tokens / 1_000_000, 2)
        openai_cost = round(8.75 * total_tokens / 1_000_000, 2)
        print(f"anthropic_cost: ${anthropic_cost} \t openai_cost: ${openai_cost}")
        print("Cost: $0 per request (Look at that amazing savings!)")
        print("----")
    finally:
        unload_model(client, DEFAULT_MODEL)


if __name__ == "__main__":
    main()
