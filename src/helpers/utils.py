import os
import pprint
from tempfile import NamedTemporaryFile
from typing import Any
import streamlit as st
from langchain import OpenAI
from langchain.chains import RetrievalQA
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores.base import VectorStoreRetriever

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.vectorstores import Cassandra
from langchain.indexes.vectorstore import VectorStoreIndexWrapper, VectorstoreIndexCreator

my_openai_api_key = os.getenv("OPENAI_API_KEY")

import os
import cassio

token = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
database_id = os.getenv("ASTRA_DB_ID")
keyspace = os.getenv("ASTRA_DB_KEYSPACE")
table_name = os.getenv("ASTRA_DB_TABLENAME")

cassio.init(
        token=token,
        database_id=database_id,
        keyspace=keyspace,
)



def get_text():
    """Get text from user"""
    input_text = st.text_input("You: ")
    return input_text


def generate_response(query: str, chain_type: str, retriever: VectorStoreRetriever, open_ai_token) -> dict[str, Any]:

    if query == "who are you":
        result_content = """I am HD C """
        result = {'query': query, 'result': result_content, 'source_documents': [
            Document(
                page_content='alibaba cloud SA team hd C ',
                metadata={'source': '/tmp/tmplvqwt_4h.pdf', 'page': 7}),
            Document(
                page_content='super hero SA HD C',
                metadata={'source': '/tmp/tmplvqwt_4h.pdf', 'page': 9}),

        ]}
        return result
    else:
        qa = RetrievalQA.from_chain_type(
            llm=OpenAI(openai_api_key = open_ai_token, model_name="gpt-3.5-turbo-16k"),
            chain_type=chain_type,
            retriever=retriever,
            return_source_documents=True
        )
        result = qa({'query': query})
        pprint.pprint(result)

    return result


def transform_document_into_chunks(document: list[Document]) -> list[Document]:
    """Transform document into chunks of {1000} tokens"""
    splitter = CharacterTextSplitter(
        chunk_size=int(os.environ.get('CHUNK_SIZE', 1000)),
        chunk_overlap=int(os.environ.get('CHUNK_OVERLAP', 0))
    )
    return splitter.split_documents(document)




def transform_chunks_into_embeddings(text: list[Document], k: int , open_ai_token ) -> VectorStoreRetriever:
    """Transform chunks into embeddings"""


    embeddings = OpenAIEmbeddings(openai_api_key = open_ai_token)
    # db = AnalyticDB.from_documents(text, embeddings, connection_string=CONNECTION_STRING)
    db = Cassandra(
        table_name=table_name,
        embedding=embeddings,
        session=None,  # = get defaults from init()
        keyspace=keyspace,  # = get defaults from init()
    )

    index_creator = VectorstoreIndexCreator(
        vectorstore_cls=Cassandra,
        embedding=embeddings,
        text_splitter=CharacterTextSplitter(
            chunk_size=400,
            chunk_overlap=0,
        ),
        vectorstore_kwargs={
            'session': None,
            'keyspace': keyspace,
            'table_name': table_name,
        },
    )

    vs = index_creator.vectorstore_cls.from_documents(
        text,
        index_creator.embedding,
        **index_creator.vectorstore_kwargs,
    )
    index = VectorStoreIndexWrapper(vectorstore=vs)
    retriever = index.vectorstore.as_retriever(search_kwargs={
        'k': k,"search_type":"mmr",
    })

    return retriever

def get_file_path(file) -> str:
    """Obtain the file full path."""
    with NamedTemporaryFile(dir='/tmp/', suffix='.pdf', delete=False) as f:
        f.write(file.getbuffer())
        return f.name


def setup(file: str, number_of_relevant_chunk: int, open_ai_token: str ) -> VectorStoreRetriever:
    # load the document
    loader = PyPDFLoader(file)
    document = loader.load()
    # transform the document into chunks
    chunks = transform_document_into_chunks(document)
    # transform the chunks into embeddings
    return transform_chunks_into_embeddings(chunks, number_of_relevant_chunk ,open_ai_token)
