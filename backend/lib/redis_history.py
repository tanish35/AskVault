from langchain.memory import ConversationBufferMemory
from langchain_community.chat_message_histories import RedisChatMessageHistory
from lib.config import settings


def get_user_memory(user_id: str) -> ConversationBufferMemory:
    redis_url = settings.redis_url
    chat_history = RedisChatMessageHistory(
        session_id=user_id,
        url=redis_url,
    )

    return ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        chat_memory=chat_history,
    )


def get_user_memory_context(memory: ConversationBufferMemory) -> str:
    messages = memory.chat_memory.messages
    history = []
    for msg in messages:
        if msg.type == "human":
            history.append(f"User: {msg.content}")
        else:
            history.append(f"AI: {msg.content}")
    return "\n".join(history[-5:])
