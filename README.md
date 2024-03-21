# RAG - NLP Project for spring 2024 - COMS-579
TEAM Members: 

- Subhankar Bhattacharjee
- Koushik Howlader
- Md Asif Mahmod Tusher Siddique


## Video demo link

[Video Demo](https://www.youtube.com/)

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
  ```def load_pdf(file_path):
        if file_path.lower().endswith(".pdf"):
            # Remove all existing PDF files in the ./pdfs directory
            existing_pdfs = glob.glob("./pdfs/*.pdf")
            for pdf in existing_pdfs:
                os.remove(pdf)

            # Copy the new PDF file to the ./pdfs directory
            shutil.copy(file_path, "./pdfs")
            return True
        else:
            return False```
- To ingest: `clean_text = TextCleaner(doc.text).clean()`
- To make chunks:
  ```Settings.text_splitter = SentenceSplitter(
       separator=" ", chunk_size=200, chunk_overlap=50,
       paragraph_separator="\n\n\n",
       secondary_chunking_regex="[^,.;。]+[,.;。]?",
       tokenizer=tiktoken.encoding_for_model(self.model_name).encode)```
- To embed chunks: `index, nodes = indexing.get_index()`


