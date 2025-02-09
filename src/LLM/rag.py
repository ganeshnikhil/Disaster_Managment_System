# app.py
#import streamlit as st
import os
import logging
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_community.vectorstores import Chroma
from chromadb.config import Settings
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.retrievers.multi_query import MultiQueryRetriever
import ollama


# Configure logging
logging.basicConfig(level=logging.INFO)

# Constants
DOC_PATH = "./Data/disaster_data.pdf"
MODEL_NAME = "llama3.2"
EMBEDDING_MODEL = "nomic-embed-text"
VECTOR_STORE_NAME = "simple-rag"
PERSIST_DIRECTORY = "./Data/chroma_db"

def ingest_pdf(doc_path):
    """Load PDF documents."""
    if os.path.exists(doc_path):
        try:
            loader = PyPDFLoader(file_path=doc_path)
            pages = []
            for page in loader.lazy_load():
                pages.append(page)
            # Attempt to load the PDF
            # loader = UnstructuredPDFLoader(file_path=doc_path , mode="elements")
            # data = loader.load()
            logging.info("PDF loaded successfully.")
            return pages
        except Exception as e:
            logging.error(f"Error loading PDF: {e}")
            return None
    else:
        logging.error(f"PDF file not found at path: {doc_path}")
        return None


def split_documents(documents):
    """Split documents into smaller chunks."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=300)
    chunks = text_splitter.split_documents(documents)
    logging.info(f"Documents split into {len(chunks)} chunks.")
    return chunks

@st.cache_resource
def load_vector_db():
    """Load or create the vector database."""
    #ollama.pull(EMBEDDING_MODEL)

    embedding = OllamaEmbeddings(model=EMBEDDING_MODEL)

    if os.path.exists(PERSIST_DIRECTORY):
        vector_db = Chroma(
            embedding_function=embedding,
            collection_name=VECTOR_STORE_NAME,
            persist_directory=PERSIST_DIRECTORY,
        )
        logging.info("Loaded existing vector database.")
    else:
        # Load and process the PDF document
        data = ingest_pdf(DOC_PATH)
        if data is None:
            logging.error("Failed to load the document.")
            return None

        # Split the documents into chunks
        chunks = split_documents(data)

        vector_db = Chroma.from_documents(
            documents=chunks,
            embedding=embedding,
            collection_name=VECTOR_STORE_NAME,
            persist_directory=PERSIST_DIRECTORY,
        )
        vector_db.persist()
        logging.info("Vector database created and persisted.")
    return vector_db


def create_retriever(vector_db, llm):
    """Create a multi-query retriever."""
    QUERY_PROMPT = PromptTemplate(
        input_variables=["question"],
        template="""You are an AI language model assistant. Your task is to generate exact four precise questions.
different versions of the given user question . By generating multiple perspectives on the user question.
Provide only the questions, separated by newlines, with no extra spaces or blank lines, without any introduction or explanation.
Original question: {question}""",
    )

    retriever = MultiQueryRetriever.from_llm(
        vector_db.as_retriever(), llm, prompt=QUERY_PROMPT
    )
    logging.info("Retriever created.")
    return retriever


def create_chain(retriever, llm):
    """Create the chain with preserved syntax."""
    # RAG prompt
    template = """You are an AI language model.
Use the provided CONTEXT below . I want you to think step by step to answer the QUERY. 
Provide a clear , precise and step by step Answer. Never Mention about provided Document source or  CONTEXT , it's your knowledge Base. 
If the CONTEXT lacks the facts to answer, return {{NONE}}.
    
CONTEXT:
{context}

QUERY: {question}
ANSWER: """
    prompt = ChatPromptTemplate.from_template(template)

    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    logging.info("Chain created with preserved syntax.")
    return chain

def main(user_input):
    try:
        # Check if the language model is initialized in session state
        if "llm" not in st.session_state:
            # Initialize the language model only once
            st.session_state.llm = ChatOllama(model=MODEL_NAME)
            logging.info(f"Language model {MODEL_NAME} initialized.")
        
        llm = st.session_state.llm

        # Check if the vector database is loaded from session state
        if "vector_db" not in st.session_state:
            logging.info("Loading vector database for the first time...")
            vector_db = load_vector_db()
            if vector_db is None:
                logging.error("Failed to load or create the vector database.")
                return
            st.session_state.vector_db = vector_db
        else:
            vector_db = st.session_state.vector_db
            logging.info("Loaded vector database from session state.")

        # Create the retriever
        retriever = create_retriever(vector_db, llm)

        # Create the chain
        chain = create_chain(retriever, llm)

        # Get the response
        response = chain.invoke(input=user_input)
        logging.info(f"Response generated: {response}")

        # Output the response
        return response

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    user_input = "What are the impacts of disaster?"
    print(main(user_input))  # Simulate running the main function


