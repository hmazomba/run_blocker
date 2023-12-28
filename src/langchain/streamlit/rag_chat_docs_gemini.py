from langchain.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader, DirectoryLoader,TextLoader, PyPDFDirectoryLoader, PyPDFLoader, CSVLoader
import streamlit as st
from langchain.callbacks import StreamlitCallbackHandler
import pandas as pd
from langchain.embeddings import HuggingFaceEmbeddings, CohereEmbeddings
import os
from dotenv import load_dotenv
from langchain.chat_models import ChatLiteLLM
import tempfile
from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory
from langchain.embeddings import HuggingFaceEmbeddings, CohereEmbeddings, GooglePalmEmbeddings
from langchain.callbacks.base import BaseCallbackHandler
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain import hub
from langchain.embeddings import GPT4AllEmbeddings
from langchain.vectorstores import Chroma
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.tools import BaseTool
from langchain.utilities import PythonREPL
from langchain.tools import DuckDuckGoSearchRun
from langchain.agents import ZeroShotAgent, Tool, AgentExecutor
from langchain.tools import DuckDuckGoSearchRun
from langchain.tools import DuckDuckGoSearchRun 
from langchain.tools.file_management import (
    ReadFileTool,
    CopyFileTool,
    DeleteFileTool,
    MoveFileTool,
    WriteFileTool,
    ListDirectoryTool,
)
from langchain.tools import ShellTool
from langchain.agents import load_tools


#DuckDuckGo Class
duckduck_search = DuckDuckGoSearchRun()
shell_tool = ShellTool()
#Python REPL Class
python_repl = PythonREPL()

load_dotenv()
google_api_key= os.getenv('GOOGLE_API_KEY')
chat = ChatLiteLLM(model="palm/chat-bison", streaming=True,
    verbose=True,
    callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]))


rag_prompt = hub.pull("rlm/rag-prompt")
# Page title
st.set_page_config(page_title='🦜🔗 Ask the Data App')
st.title('🦜🔗 Ask the Data App')

def configure_retriever(uploaded_files):
    # Read documents
    docs = []
    temp_dir = tempfile.TemporaryDirectory()
    for file in uploaded_files:
        temp_filepath = os.path.join(temp_dir.name, file.name)
        temp_path = temp_dir.name 
        with open(temp_filepath, "wb") as f:
            f.write(file.getvalue())
        pdf_loader = DirectoryLoader(temp_path, glob="**/*.pdf", loader_cls=PyPDFLoader)
        txt_loader = DirectoryLoader(temp_path, glob="**/*.txt", loader_cls=TextLoader)
        csv_loader = DirectoryLoader(temp_path, glob="**/*.csv", loader_cls=CSVLoader)
        loaders = [pdf_loader, txt_loader, csv_loader]
        for loader in loaders:
            docs.extend(loader.load())

    # Split documents
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)

    # Create embeddings and store in vectordb
    embeddings = GooglePalmEmbeddings()
    vectordb = Chroma.from_documents(splits, embeddings)

    # Define retriever
    retriever = vectordb.as_retriever()

    return retriever

uploaded_files = st.sidebar.file_uploader(
    label="Upload PDF files", type=["pdf", "txt", "csv"], accept_multiple_files=True
)

if not uploaded_files:
    st.info("Please upload documents to continue.")
    st.stop()

retriever = configure_retriever(uploaded_files)

qa_chain = RetrievalQA.from_chain_type(
    llm=chat, chain_type="stuff", retriever=retriever, chain_type_kwargs={"prompt": rag_prompt}
)

tools = [
    Tool(
        name="Document Summariser",
        func=qa_chain.run,
        description="Useful for summarising uploaded documents",
    ),
    Tool(
    name="python_repl",
    description="A Python shell. Use this to execute python commands. Input should be a valid python command. If you want to see the output of a value, you should print it out with `print(...)`.",
    func=python_repl.run
    ), 
    Tool(
        name = "DuckDuckGo",
        func=duckduck_search.run,
        description="useful for when you need to answer questions about current events. You should ask targeted questions"
    ), 
    Tool(
    name="shell",
    description="This tool gives you access to a system's shell. Can be used to run shell commands",
    func=shell_tool.run
    )
]
# Construct the agent. We will use the default agent type here.
# See documentation for a full list of options.
agent = initialize_agent(
    tools, chat, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)
# Setup memory for contextual conversation
msgs = StreamlitChatMessageHistory()
memory = ConversationBufferMemory(memory_key="chat_history", chat_memory=msgs, return_messages=True)

if len(msgs.messages) == 0 or st.sidebar.button("Clear message history"):
    msgs.clear()
    msgs.add_ai_message("How can I help you?")

avatars = {"human": "user", "ai": "assistant"}
for msg in msgs.messages:
    st.chat_message(avatars[msg.type]).write(msg.content)

if user_query := st.chat_input(placeholder="What is this article about?"):
    st.chat_message("user").write(user_query)

    with st.chat_message("assistant"):
        retrieval_handler = StreamlitCallbackHandler(st.container())
        response = agent.run(user_query, callbacks=[retrieval_handler])
        st.write(response)