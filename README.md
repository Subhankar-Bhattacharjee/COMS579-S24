# RAG - NLP Project for spring 2024 - COMS-579
TEAM Members: 

- Subhankar Bhattacharjee
- Koushik Howlader
- Md Asif Mahmod Tusher Siddique


## Video demo link

[Video Demo](https://www.youtube.com/)

### Technology Used:
- LangChain
- Weaviate

### Installation

`pip install -r requirements.txt`

#### Create a .env file in the root directory, then add your key:
- `OPENAI_API_KEY=openai_api _key`
- `WEAVIATE_URL=weaviate_url`
- `WEAVIATE_API_KEY=weaviate_api_key`

### Command-line Usage

- To upload a PDF: `python upload.py --pdf_file=example.pdf`

## Step By Step for execution
- Add PDF to pdfs directory:
  Go to `rag_files/pdf_load.py` and find the `load_pdf()` function.
- Text Filtering:
  Go to `rag_files/data_preprocess.py` and find the `clean_text()` function.
- Split text into chunks:
  go to the `rag_files/indexing.py` and find
  ```text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=25)```
  ```docs = text_splitter.split_documents(cleaned_data)```


