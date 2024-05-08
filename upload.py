
import argparse
import os
import openai
import json
import weaviate
from rag_files.indexing import Index
from rag_files.data_preprocess import Data_Processing
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
import warnings
warnings.filterwarnings("ignore")
weaviate_api_key = os.getenv('WEAVIATE_API_KEY')
weaviate_url = os.getenv('WEAVIATE_URL')
openai_api_key = os.getenv('OPENAI_API_KEY')
openai.api_key = openai_api_key


def upload_and_index(pdf_path):
    text = Index.get_pdf_text(pdf_path)
    cleaned_text = Data_Processing.clean_documents(text)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=4000, chunk_overlap=0.25)
    chunks = text_splitter.split_documents(cleaned_text)

    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
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
    for doc in chunks:
        # Embed text chunk
        response = openai.Embedding.create(input=doc.page_content,model="text-embedding-ada-002")
        embedding = response['data'][0]['embedding']  # Get the embedding vector
        # Add text and its embedding to Weaviate
        client.data_object.create(
            data_object={"content": doc.page_content},
            vector=embedding,
            class_name="Document"
        )

    response = client.data_object.get(class_name="Document", with_vector=True)
    with open("index_data.json","w") as f:
        json.dump(response, f, indent=2)



def main():
    parser = argparse.ArgumentParser(description="Upload and index PDF documents.")
    parser.add_argument("--pdf_file", type=str, required=True, help="Path to the PDF file to index")
    args = parser.parse_args()

    # Index the specified PDF file
    Index.index_pdf(args.pdf_file)
    
if __name__ == "__main__":
    main()
    
