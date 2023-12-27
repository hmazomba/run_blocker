import os
from dotenv import load_dotenv

load_dotenv()
huggingfacehub_api_key= os.getenv('HUGGINGFACEHUB_API_TOKEN')
cohere_api_key= os.getenv('COHERE_API_KEY')
google_api_key= os.getenv('GOOGLE_API_KEY')

#Load Chain Dependencies
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatLiteLLM
from langchain.prompts.chat import (
    ChatPromptTemplate
)
from langchain.chains import LLMChain
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import CohereEmbeddings, HuggingFaceBgeEmbeddings, GooglePalmEmbeddings, HuggingFaceEmbeddings, GPT4AllEmbeddings

# Load the LLMS
from langchain.llms import LlamaCpp, Cohere, GooglePalm
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler


#Loader Dependencies
from bs4 import BeautifulSoup as Soup

#Load the loaders
from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.document_loaders.recursive_url_loader import RecursiveUrlLoader
from langchain.document_loaders import UnstructuredExcelLoader
from langchain.document_loaders import DirectoryLoader
from langchain.document_loaders import TextLoader
from langchain.document_loaders import UnstructuredWordDocumentLoader

#Load the tools
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.tools import BaseTool
from langchain.utilities import PythonREPL
from langchain.tools import DuckDuckGoSearchRun
from langchain.agents import ZeroShotAgent, Tool, AgentExecutor
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

#Load the agent
from langchain.agents import ZeroShotAgent, Tool, AgentExecutor

google_palm_llm = GooglePalm()
cohere_llm = ChatLiteLLM(model="command-nightly")

tenders_pdf_loader = PyPDFDirectoryLoader("../../data/")


#loader = DirectoryLoader('../', glob="**/*.md", use_multithreading=True)
#txt_loader = DirectoryLoader("../../data/talentlms/", glob="**/*.txt", use_multithreading=True, loader_cls=TextLoader)
#xlsx_loader = DirectoryLoader("../../data/talentlms/", glob="**/*.xlsx", use_multithreading=True, loader_cls=UnstructuredExcelLoader)
pdf_loader = DirectoryLoader("../../data/tenders/", glob="**/*.pdf", use_multithreading=True, loader_cls=PyPDFDirectoryLoader)
#docx_loader = DirectoryLoader("../../data/talentlms/", glob="**/*.docx", use_multithreading=True, loader_cls=UnstructuredWordDocumentLoader)

url = ""
talent_lms_recursive_url_loader = RecursiveUrlLoader(url=url, max_depth=200, extractor=lambda x: Soup(x, "html.parser").text)

loaders = [tenders_pdf_loader]
documents = []
for loader in loaders:
    documents.extend(loader.load())

print(f"Total number of documents: {len(documents)}")