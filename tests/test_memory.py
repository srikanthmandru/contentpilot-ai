from src.memory.conversation_memory import (
    add_user_message,
    add_ai_message,
    get_recent_context,
)


def test_add_user_message():
    state = {"messages": []}

    result = add_user_message(state, "Hello")

    assert result["messages"][0]["role"] == "user"
    assert result["messages"][0]["content"] == "Hello"


def test_add_ai_message():
    state = {"messages": []}

    result = add_ai_message(state, "Hi there")

    assert result["messages"][0]["role"] == "assistant"
    assert result["messages"][0]["content"] == "Hi there"


def test_get_recent_context():
    state = {
        "memory_summary": "User is building ContentPilot AI.",
        "messages": [
            {"role": "user", "content": "Create blog"},
            {"role": "assistant", "content": "Done"},
        ],
    }

    context = get_recent_context(state)

    assert "Conversation summary" in context
    assert "Create blog" in context
