from agentic_chatbot_backend import chatbot
from langchain_core.messages import SystemMessage, HumanMessage, BaseMessage
from dotenv import load_dotenv
import streamlit as st

st.title('Agentic Chatbot With LangGraph')

thread_id=1
CONFIG = {'configurable':{'thread_id':thread_id}}


if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []


for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])
        


user_input = st.chat_input('Type here')
#st.write('User input:',user_input)

if user_input:
    st.session_state['message_history'].append({'role':'user','content':user_input})
    with st.chat_message('user'):
        st.text(user_input)

    #response = chatbot.invoke({'messages':[HumanMessage(content=user_input)]}, config=CONFIG)
    #ai_message = response['messages'][-1].content
    #st.session_state['message_history'].append({'role':'assistant','content':ai_message})
    #with st.chat_message('assistant'):
        #st.text(ai_message)

        
    with st.chat_message('assistant'):

        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(
                {'messages':[HumanMessage(content=user_input)]},
                config= {'configurable':{'thread_id':thread_id}},
                stream_mode='messages'
            )
        )

    st.session_state['message_history'].append({'role':'assistant','content':ai_message})



