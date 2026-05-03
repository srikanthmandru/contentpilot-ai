from src.core.config import settings
from src.integrations.llm_client import get_llm


def add_user_message(state, message: str):
    messages = state.get("messages", [])
    messages.append({"role": "user", "content": message})
    return {**state, "messages": messages}


def add_ai_message(state, message: str):
    messages = state.get("messages", [])
    messages.append({"role": "assistant", "content": message})
    return {**state, "messages": messages}


def get_recent_context(state):
    messages = state.get("messages", [])
    recent = messages[-settings.MAX_RECENT_MESSAGES :]
    summary = state.get("memory_summary", "")

    context_parts = []

    if summary:
        context_parts.append(f"Conversation summary:\n{summary}")

    if recent:
        recent_text = "\n".join(f"{msg['role']}: {msg['content']}" for msg in recent)
        context_parts.append(f"Recent messages:\n{recent_text}")

    return "\n\n".join(context_parts)


def should_summarize(state):
    messages = state.get("messages", [])
    return len(messages) >= settings.MEMORY_SUMMARY_TRIGGER


def summarize_conversation(state):
    if not should_summarize(state):
        return state

    llm = get_llm(temperature=0)

    existing_summary = state.get("memory_summary", "")
    messages = state.get("messages", [])

    old_messages = messages[: -settings.MAX_RECENT_MESSAGES]
    recent_messages = messages[-settings.MAX_RECENT_MESSAGES :]

    old_message_text = "\n".join(
        f"{msg['role']}: {msg['content']}" for msg in old_messages
    )

    prompt = f"""
You are a conversation memory summarizer.

Update the running summary using the older conversation messages.

Existing summary:
{existing_summary}

Older messages:
{old_message_text}

Create a concise memory summary that preserves:
- User goals
- Project decisions
- Current implementation status
- Important technical choices
- Pending next steps

Do not include unnecessary details.
"""

    result = llm.invoke(prompt)

    return {
        **state,
        "memory_summary": result.content,
        "messages": recent_messages,
    }
