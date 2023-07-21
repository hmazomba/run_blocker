import os
from dotenv import load_dotenv

load_dotenv()
cohere_api_key= os.getenv('COHERE_API_KEY')

from langchain.llms import Cohere

from langchain.agents import AgentType, initialize_agent, load_tools
from langchain.callbacks import StreamlitCallbackHandler
import streamlit as st
from langchain.tools import DuckDuckGoSearchRun

search_agent = initialize_agent(
        tools=[DuckDuckGoSearchRun(name="Search")],
        llm=Cohere(cohere_api_key=cohere_api_key, verbose=True),
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        handle_parsing_errors=True,
)

if prompt := st.chat_input():
    st.chat_message("user").write(prompt)
    with st.chat_message("assistant"):
        st_callback = StreamlitCallbackHandler(st.container())
        response = search_agent.run(prompt, callbacks=[st_callback])
        st.write(response)