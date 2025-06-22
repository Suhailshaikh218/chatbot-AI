import chainlit as cl
import requests

api_key = "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"
model_name = "mistralai/Mistral-7B-Instruct-v0.2"
base_url="https://generativelanguage.googleapis.com/v1beta/openai"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}",
    "HTTP-Referer": "http://localhost:8000"
}

@cl.on_chat_start
async def start():
    cl.user_session.set("history", [])
    await cl.Message("👋 Welcome! Ask me anything.").send()

@cl.on_message
async def on_message(message: cl.Message):
    print("Message Received:", message.content)

    history = cl.user_session.get("history")
    history.append({"role": "user", "content": message.content})

    payload = {
        "model": model_name,
        "messages": history
    }

    try:
        print("Sending request to OpenRouter...")
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=15
        )
        response.raise_for_status()
        res = response.json()
        print("API Response:", res)

        # Check if message.content exists
        if "choices" in res and res["choices"]:
            message_data = res["choices"][0]["message"]
            if "content" in message_data and message_data["content"]:
                reply = message_data["content"]
                history.append({"role": "assistant", "content": reply})
            else:
                reply = "❌ Assistant returned empty response."
        else:
            reply = f"❌ Unexpected response format: {res}"

    except Exception as e:
        reply = f"❌ Error: {e}"

    await cl.Message(reply).send()
