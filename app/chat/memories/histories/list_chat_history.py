from langchain_core.chat_history import BaseChatMessageHistory
from langchain.schema import BaseMessage

from app.web.api import (
    get_messages_by_conversation_id,
    add_message_to_conversation,
)


class ListChatHistory(BaseChatMessageHistory):
    def __init__(self, conversation_id: str):
        self.conversation_id = conversation_id

        # КРИТИЧНО: messages — обычный list
        self.messages: list[BaseMessage] = list(
            get_messages_by_conversation_id(conversation_id)
        )

    def add_message(self, message: BaseMessage):
        add_message_to_conversation(
            conversation_id=self.conversation_id,
            role=message.type,
            content=message.content,
        )
        self.messages.append(message)

    def clear(self):
        self.messages.clear()
