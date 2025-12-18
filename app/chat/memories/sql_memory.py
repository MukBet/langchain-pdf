from langchain.memory import ConversationBufferMemory
from app.chat.memories.histories.sql_history import SQLMessageHistory
from app.chat.memories.histories.list_chat_history import ListChatHistory
    
def build_memory(chat_args):
    return ConversationBufferMemory(
        chat_memory = ListChatHistory(
            conversation_id=chat_args.conversation_id
        ),
        return_messages=True,
        memory_key="chat_history",
        output_key="answer"
    )
