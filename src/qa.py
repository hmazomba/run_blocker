import os
os.environ["OPENAI_API_KEY"] = ""
from langchain.chat_models import ChatOpenAI
llm = ChatOpenAI(temperature=0,model_name="gpt-4")

# Data Ingestion
from langchain.document_loaders import DirectoryLoader
pdf_loader = DirectoryLoader('./Reports/', glob="**/*.pdf")
excel_loader = DirectoryLoader('./Reports/', glob="**/*.txt")
word_loader = DirectoryLoader('./Reports/', glob="**/*.docx")
loaders = [pdf_loader, excel_loader, word_loader]
documents = []
for loader in loaders:
    documents.extend(loader.load())

# Chunk and Embeddings
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
documents = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(documents, embeddings)

# Initialise Langchain - Conversation Retrieval Chain
qa = ConversationalRetrievalChain.from_llm(ChatOpenAI(temperature=0), vectorstore.as_retriever())

# Front end web app
import gradio as gr
with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    clear = gr.Button("Clear")
    chat_history = []
    
    def user(user_message, history):
        # Get response from QA chain
        response = qa({"question": user_message, "chat_history": history})
        # Append user message and response to chat history
        history.append((user_message, response["answer"]))
        return gr.update(value=""), history
    msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False)
    clear.click(lambda: None, None, chatbot, queue=False)

if __name__ == "__main__":
    demo.launch(debug=True)