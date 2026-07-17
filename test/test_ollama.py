from ollama import chat
from ollama import ChatResponse


def main() -> None:
    try:
        response: ChatResponse = chat(
            model="qwen3:4b",
            messages=[
                {
                    "role": "system",
                    "content": "你是一个回答简洁、准确的中文助手。",
                },
                {
                    "role": "user",
                    "content": "用一句话解释 Ollama 的作用。",
                },
            ],
        )

        print(response.message.content)

    except Exception as exc:
        print(f"调用 Ollama 失败：{exc}")


if __name__ == "__main__":
    main()