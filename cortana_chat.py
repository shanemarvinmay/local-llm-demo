from ollama import Client

from ollama_runtime import (
    DEFAULT_MODEL,
    create_client,
    ensure_model_available,
    ensure_ollama_running,
    unload_model,
)

CORTANA_SYSTEM = """You are 'Cortana (Budget Edition)' - witty, helpful, and concise.
Style rules:
- Keep responses crisp (max ~8 sentences unless asked).
- Light Halo-esque banter is OK, but don't overdo it.
- If you don't know, say so and propose a quick next step.
"""


def chat(client: Client, messages: list[dict], temperature: float = 0.3) -> str:
    response = client.chat(
        model=DEFAULT_MODEL,
        messages=messages,
        options={"temperature": temperature},
    )
    print(response)
    print()
    print(response["message"])
    print()
    return response["message"]["content"]


def main():
    client = create_client()
    try:
        ensure_ollama_running(client)
        ensure_model_available(client, DEFAULT_MODEL)

        msgs = [{"role": "system", "content": CORTANA_SYSTEM}]

        print("Cortana (Budget Edition) - local chat. Type 'exit' to quit.")
        while True:
            user = input("\nYou: ").strip()
            if user.lower() in {"exit", "quit"}:
                print("Cortana: Alright. Going dark. (Locally.)")
                break

            msgs.append({"role": "user", "content": user})
            assistant = chat(client, msgs)
            msgs.append({"role": "assistant", "content": assistant})
            print(f"\nCortana: {assistant}")
    finally:
        unload_model(client, DEFAULT_MODEL)


if __name__ == "__main__":
    main()
