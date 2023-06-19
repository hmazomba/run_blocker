from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import GPT4All
from langchain.chains import RetrievalQA

# Step 1: Load the PDF Document
loader = PyPDFLoader("eCommerce Product Requirements Documentation V1 (1).pdf")
documents = loader.load_and_split()

# Step 2: Text Splitting
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=64)
texts = text_splitter.split_documents(documents)

# Step 3: Creating Embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Step 4: Vector Store
db = Chroma.from_documents(texts, embeddings, persist_directory="db")

# Step 5: Load the gpt4all Model
model_path = "./ggml-gpt4all-j-v1.3-groovy.bin"
llm = GPT4All(model=model_path, n_ctx=1000, backend="gptj", verbose=False)

# Step 6: Create the Question-Answering Chain
qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=db.as_retriever(search_kwargs={"k": 3}),
    return_source_documents=True,
    verbose=False,
)

# Step 7: Ask Questions
res = qa("How much is the dividend per share during 2022? Extract it from the text.")
print(res["result"])
