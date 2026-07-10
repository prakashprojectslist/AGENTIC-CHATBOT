from langgraph.graph import StateGraph,START,END
from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage, BaseMessage
from langgraph.graph.message import add_messages
from typing import TypedDict,Annotated
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3


load_dotenv()

llm = ChatGroq(model="llama-3.3-70b-versatile",temperature=0.7)

class ChatState(TypedDict):

    messages:Annotated[list[BaseMessage], add_messages]


def chat_node(state: ChatState) -> ChatState:
    # Get the messages from the state
    messages = state.get('messages', [])
    
    # Call the LLM with the messages
    response = llm.invoke(messages)
    
    # Append the response to the messages
    messages.append(response)
    
    # Return the updated state
    return {'messages': messages}


conn = sqlite3.connect(database="chatbot.db", check_same_thread=False)
checkpoint = SqliteSaver(conn)

graph = StateGraph(ChatState)

graph.add_node('chat_node',chat_node)
graph.add_edge(START,'chat_node')
graph.add_edge('chat_node',END)

chatbot = graph.compile(checkpointer=checkpoint)


def get_all_threads():
    all_threads = set()
    for ckpt in checkpoint.list(None):
        all_threads.add(ckpt.config['configurable']['thread_id'])

    return list(all_threads)


CONFIG = {'configurable':{'thread_id':'thread_id'}}

response = chatbot.invoke({
    "messages":[HumanMessage(content='My Name is Prakash')]},
     config=CONFIG
    
    )

