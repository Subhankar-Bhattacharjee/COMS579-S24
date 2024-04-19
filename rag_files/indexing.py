# Suppress warnings
import warnings
warnings.filterwarnings("ignore")
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
import weaviate
#from weaviate.tools import DataLoader, DirectoryLoader
from transformers import AutoTokenizer, AutoModel
import torch
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re
import os
import PyPDF2
import json
from transformers import AutoTokenizer, AutoModel
import warnings
warnings.filterwarnings("ignore")
from dotenv import load_dotenv,find_dotenv
load_dotenv(find_dotenv())
warnings.filterwarnings("ignore")
# Connect to Weaviate
weaviate_api_key = os.getenv('WEAVIATE_API_KEY')
weaviate_url = os.getenv('WEAVIATE_URL')
openai_api_key = os.getenv('OPENAI_API_KEY')
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

    def get_pdf_text(file_path):
        text = ""
        with open(file_path, "rb") as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() or ""  # Ensure non-None concatenation
        return text

    def embed_text(text):
        # Load your model and tokenizer
        tokenizer = AutoTokenizer.from_pretrained('distilbert-base-uncased')
        model = AutoModel.from_pretrained('distilbert-base-uncased')
        inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True)
        with torch.no_grad():
            outputs = model(**inputs)
        # Using mean of last hidden state as embedding
        return outputs.last_hidden_state.mean(dim=1).squeeze().tolist()


    def index_pdfs(directory_path):
        client = weaviate.Client(url=weaviate_url, auth_client_secret=weaviate.AuthApiKey(api_key=weaviate_api_key))

        # Define and create schema in Weaviate
        schema = {
            "classes": [
                {
                    "class": "Document",
                    "description": "A class to store text documents with embeddings and source information",
                    "properties": [
                        {"name": "content", "dataType": ["text"], "description": "The content of the document"},
                        {"name": "pdfName", "dataType": ["string"], "description": "The name of the source PDF file"}
                    ]
                }
            ]
        }
        client.schema.delete_all()
        client.schema.create(schema)

        # Load PDFs from the directory and index them
        count=0
        for filename in os.listdir(directory_path):
            if filename.endswith('.pdf'):
                file_path = os.path.join(directory_path, filename)
                count=count+1
                with open(file_path, "rb") as file:
                    text = ""
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        text += page.extract_text() or ""  # Ensure non-None concatenation
                pdf_text = text
                clean_data = Data_Processing.clean_text(pdf_text)
                response = openai.Embedding.create(input=clean_data,model="text-embedding-ada-002")
                embedding = response['data'][0]['embedding'] 
                
                
                # Index the cleaned text and its embedding into Weaviate
                client.data_object.create(
                    data_object={"content": clean_data, "pdfName": filename},
                    vector=embedding,
                    class_name="Document"
                )
        
        
        response = client.data_object.get(class_name="Document", with_vector=True)
        # with open("index_data.json","w") as f:
        #     json.dump(response, f, indent=2)
        # #print("Response", response)

        print(str(count) + " PDFs Indexed Successfully!!")
