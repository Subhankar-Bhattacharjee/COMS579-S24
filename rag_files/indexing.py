from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
import weaviate
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import pdf
from langchain_community.vectorstores import Weaviate
from rag_files.pdf_load import PDFLoader
from rag_files.data_preprocess import Data_Processing
import os
from dotenv import load_dotenv,find_dotenv
load_dotenv(find_dotenv())

class Index:
    # Function to load and index PDF file
    def index_pdf(pdf_path):
        if(PDFLoader.load_pdf(pdf_path)):
            loader = DirectoryLoader('./pdfs', glob="**/*.pdf")
            data = loader.load()
            print(data)
        
        #filter text
        cleaned_data = Data_Processing.clean_documents(data)
        
        # Split text into chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=0.25)
        docs = text_splitter.split_documents(cleaned_data)
        print(docs)
    
        # Initialize embeddings
        embeddings = OpenAIEmbeddings()

        # Connect to Weaviate
        api_key = os.getenv('WEAVIATE_API_KEY')
        WEAVIATE_URL = os.getenv('WEAVIATE_URL')
        openai_api_key = os.getenv('OPENAI_API_KEY')
        auth_config = weaviate.AuthApiKey(api_key=api_key)

        WEAVIATE_URL = os.getenv('WEAVIATE_URL')
        client = weaviate.Client(
            url=WEAVIATE_URL,
            additional_headers={"X-OpenAI-Api-Key": openai_api_key},
            auth_client_secret=auth_config
        )
        #Define input structure and ensure schema is present
        schema = {
            "classes": [
                {
                    "class": "Document",
                    "description": "Documents for indexing",
                    "vectorizer": "text2vec-openai",
                    "moduleConfig": {"text2vec-openai": {"model": "ada", "type": "text"}},
                    "properties": [
                        {
                            "dataType": ["text"],
                            "description": "The content of the paragraph",
                            "moduleConfig": {
                                "text2vec-openai": {
                                    "skip": False,
                                    "vectorizePropertyName": False,
                                }
                            },
                            "name": "content",
                        },
                    ],
                },
            ]
        }
        client.schema.delete_all()
        client.schema.create(schema)

        # Load text into the vector store
        vectorstore = Weaviate(client, "Document", "content", attributes=["source"])
        text_meta_pair = [(doc.page_content, doc.metadata) for doc in docs]
        texts, meta = list(zip(*text_meta_pair))
        vectorstore.add_texts(texts, meta)

        print("PDF indexed successfully.")

        return client, vectorstore
