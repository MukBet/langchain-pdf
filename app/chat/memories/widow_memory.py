from langchain.memory import ConversationBufferWindowMemory
from app.chat.memories.histories.sql_history import SQLMessageHistory
from app.chat.memories.histories.list_chat_history import ListChatHistory

def window_buffer_memory_builder (chat_args):
  return ConversationBufferWindowMemory(
    memory_key="chat_history",
    output_key="answer",
    return_messages=True,
    chat_memory = ListChatHistory(
        conversation_id=chat_args.conversation_id
    ),
    k=2
  )