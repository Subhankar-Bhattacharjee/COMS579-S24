import os
import openai
import weaviate
import json
import os
import openai
import weaviate
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import pdf
from rag_files.pdf_load import PDFLoader
from rag_files.data_preprocess import Data_Processing
from dotenv import load_dotenv,find_dotenv
load_dotenv(find_dotenv())

# Connect to Weaviate
weaviate_api_key = os.getenv('WEAVIATE_API_KEY')
weaviate_url = os.getenv('WEAVIATE_URL')
openai_api_key = os.getenv('OPENAI_API_KEY')
# Assuming `openai_api_key` is your OpenAI API key
openai.api_key = openai_api_key

class Index:

    def get_embedding(text):
        response = openai.Embedding.create(
            input=text,
            model="text-embedding-ada-002"  # Choose an appropriate model for your task
        )
        embedding = response['data'][0]['embedding']  # Get the embedding vector
        return embedding

    def index_pdf(pdf_path):
        if(PDFLoader.load_pdf(pdf_path)):
            print (pdf_path, "Uploaded Successfully!!\n")
            loader = DirectoryLoader('./pdfs', glob="**/*.pdf")
            data = loader.load()
            print("\nOriginal text: \n", data)
        
        # Clean text
        cleaned_data = Data_Processing.clean_documents(data)
        # Split text into chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=4000, chunk_overlap=0.25)
        docs = text_splitter.split_documents(cleaned_data)
        print("\nAfter Filtering text: \n", docs)
        # Initialize OpenAI Embeddings
        embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
        # Connect to Weaviate
        auth_config = weaviate.AuthApiKey(api_key=weaviate_api_key)
        client = weaviate.Client(url=weaviate_url, auth_client_secret=auth_config)
        # Ensure schema is present
        schema = {
            "classes": [
                {
                    "class": "Document",
                    "description": "A class to store documents",
                    "properties": [
                        {"name": "content", "dataType": ["text"], "description": "The content of the document"},
                    ],
                    "vectorIndexType": "hnsw",
                    "vectorizer": "none",  # We'll provide our own vectors
                },
            ]
        }
        client.schema.delete_all()
        client.schema.create(schema)

        # Process each document chunk
        for doc in docs:
            # Embed text chunk
            response = openai.Embedding.create(input=doc.page_content,model="text-embedding-ada-002")
            embedding = response['data'][0]['embedding']  # Get the embedding vector
            # Add text and its embedding to Weaviate
            client.data_object.create(
                data_object={"content": doc.page_content},
                vector=embedding,
                class_name="Document"
            )
        
        print("Indexed Successfully!!")
        response = client.data_object.get(class_name="Document", with_vector=True)
        with open("index_data.json","w") as f:
            json.dump(response, f, indent=2)
        print("Response", response)
