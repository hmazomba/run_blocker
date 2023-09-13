from langchain.agents import Tool
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.callbacks.streaming_stdout_final_only import (
    FinalStreamingStdOutCallbackHandler,
)
import os
from dotenv import load_dotenv
from langchain.llms import Cohere
from langchain.tools import DuckDuckGoSearchRun
#Playwright
from langchain.agents.agent_toolkits import PlayWrightBrowserToolkit
from langchain.tools.playwright.utils import (
    create_async_playwright_browser,
    create_sync_playwright_browser,  # A synchronous browser is available, though it isn't compatible with jupyter.
)

#Python Tools
from langchain.agents.agent_toolkits import create_python_agent
from langchain.tools.python.tool import PythonREPLTool
from langchain.python import PythonREPL


#Files ToolKit
from langchain.tools.file_management import (
    ReadFileTool,
    CopyFileTool,
    DeleteFileTool,
    MoveFileTool,
    WriteFileTool,
    ListDirectoryTool,
)
from langchain.agents.agent_toolkits import FileManagementToolkit
from tempfile import TemporaryDirectory

# We'll make a temporary directory to avoid clutter
working_directory = TemporaryDirectory()

load_dotenv()

async_browser = create_async_playwright_browser()
scrape_toolkit = PlayWrightBrowserToolkit.from_browser(async_browser=async_browser)
scraping_tools = scrape_toolkit.get_tools()

cohere_api_key= os.getenv('COHERE_API_KEY')
llm = Cohere(cohere_api_key=cohere_api_key)

async_browser = create_async_playwright_browser()
browser_toolkit = PlayWrightBrowserToolkit.from_browser(async_browser=async_browser)
browser_tools = browser_toolkit.get_tools()

DuckDuckGoSearch = DuckDuckGoSearchRun()
PythonTool =PythonREPLTool()

files_tools = FileManagementToolkit(
    root_dir=str(working_directory.name),
    selected_tools=["read_file", "write_file", "list_directory"],
).get_tools()
read_tool, write_tool, list_tool = files_tools

tools = [
    Tool(
        name="DuckDuckGo",
        func=DuckDuckGoSearch.run,
        description="useful for when you need to answer questions about current events",
    ),
    Tool(
        name="Read directory",
        func=read_tool.run,
        description="Read files within a directory",
    ),
    Tool(
        name="Write directory",
        func=write_tool.run,
        description="Write files to a directory",
    ),
]
agent = initialize_agent(
    tools, llm,  verbose=False
)
agent.run(
    "It's 2023 now. How many years ago did Konrad Adenauer become Chancellor of Germany."
)