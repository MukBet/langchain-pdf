from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.callbacks.base import BaseCallbackHandler
from dotenv import load_dotenv
from queue import Empty, Queue
from threading import Thread

load_dotenv()  # Load environment variables from .env file

class StreamingHandler(BaseCallbackHandler):
  def __init__(self, queue: Queue):
    self.queue = queue

  def on_llm_new_token(self, token, **kwargs):
    #print(token)
    self.queue.put(token) # token єто частичка ответа ИИ, слово, слова... фраза от всего ответа. Тут будет пачка єтих токенов\ответов
  
  def on_llm_end(self, response, **kwargs):
    self.queue.put(None) # сигнал что ответ закончен

  def on_llm_error(self, error, **kwargs):
    self.queue.put(None) # сигнал что ответ закончен

chat = ChatOpenAI(
  streaming=True
)

prompt = ChatPromptTemplate.from_messages([
  ("human", "{content}")
])
# chain = LLMChain(llm=chat, prompt=prompt)

# output = chain.stream(input={"content":"Tell me a joke"})
# for out in output:
#   print(out)


# messages = prompt.format_messages(content="Hello, how are you? answer ass I said joke")

# output = chat.stream(messages)
# for out in output:
#   print(out.content)

class StreamableChain:
  def stream(self, input):
    queue = Queue()
    handler = StreamingHandler(queue)

    def task():
      self(input, callbacks=[handler])

    Thread(target=task).start()

    while True:
      token = queue.get()
      if token is None:
        break
      yield token

class StreamableChain(StreamableChain, LLMChain):
  pass

chain = StreamableChain(llm=chat, prompt=prompt)

print(chain('Tell me a joke'))

for output in chain.stream(input={"content":"Tell me a joke"}):
  print(output)