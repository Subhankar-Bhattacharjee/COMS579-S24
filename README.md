# COMS-579: RAG-NLP Project for spring 2024
Team Members: 

- Subhankar Bhattacharjee
- Koushik Howlader
- Md Asif Mahmod Tusher Siddique


## Video demo link
## Milestone 1:
[Video Demo](https://youtu.be/sCZBrKGQPTI?si=z4Xz5aWG-kGNguUM)

## Milestone 2:
[Video Demo](https://youtu.be/DySFGW9kANo)

## Milestone 2:
[Video Demo] https://youtu.be/SF8oIdZY2Zc

### Technology Used:
- LangChain
- Weaviate

### Tasks has been done:
- Upload a single PDF to `pdfs` directory
- Text Filtering
- Split text into chunks
- Embed text chunk using `OpenAIEmbeddings()`
- Add embedding text to Weaviate
- Save response from vector database into .json file
- Upload multiple PDF , Text Filtering, Indexing
- query from command line
- rank list of the documents matches
- generate an answer based on the top rank documents found

### Installation:

`pip install -r requirements.txt`

#### Create a .env file in the root directory, then add your key:
- `OPENAI_API_KEY=openai_api _key`
- `WEAVIATE_URL=weaviate_url`
- `WEAVIATE_API_KEY=weaviate_api_key`

### Command-line Usage

- To run the app in Gradio UI: `python gradio_ui.py`
- To view the project in huggingface: https://huggingface.co/spaces/asifsiddique64/docseek
- To upload a PDF: `python upload.py --pdf_file=example.pdf`
- Answer generation via command line: `python query.py --question="What is BERT?"`

## Step By Step Tasks Explanation:
- Add PDF to pdfs directory:
  Go to `rag_files/pdf_load.py` and find the `load_pdf()` function.
- Text Filtering:
  Go to `rag_files/data_preprocess.py` and find the `clean_text()` function.
- Split text into chunks:
  go to the `rag_files/indexing.py` and find
  ```text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=25)```
  ```docs = text_splitter.split_documents(cleaned_data)```
- Initialize OpenAI Embeddings:
  go to the `rag_files/indexing.py` and find `OpenAIEmbeddings()`
- Embed text chunk:
  go to the `rag_files/indexing.py` and find `openai.Embedding.create()`
- Add text and its embedding to Weaviate:
  go to the `rag_files/indexing.py` and find `client.data_object.create()`
- Save response from vector database into .json file:
   go to the `rag_files/indexing.py` and find `client.data_object.get()`
- run from command prompt: `python query.py --question="What is BERT?"`
- index two sample files from directory named 'pdf'
- index the file by processing `rag_files/indexing.py`
- rank the documents on query search from `rag_files/results.py`
- returns the answers based on top rank document
  


