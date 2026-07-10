from agentic_chatbot_backend import chatbot
from langchain_core.messages import SystemMessage,HumanMessage,AIMessage,AnyMessage


CONFIG = {'configurable':{'thread_id':'thread1'}}

#response = chatbot.invoke({'messages':[HumanMessage(content='Generate a blog about python')]},config=CONFIG)

#print(response['messages'][-1].content)


for message_chunk, metadata in chatbot.stream(
    {'messages':[HumanMessage(content='Generate a blog about Langgraph')]},
    config=CONFIG,
    stream_mode= 'messages'):

    if message_chunk.content:
        print(message_chunk.content, end=" ", flush=True)

