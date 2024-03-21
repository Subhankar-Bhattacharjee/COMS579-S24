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
- Text Filtering:
  ```def clean_text(text):
  pattern = (
            r'\bPage \d+\b'  # 'Page X' patterns
            r'|\b\d{1,2}/\d{1,2}/\d{4}\b'  # Dates in 'MM/DD/YYYY' format
            r'|\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'  # Email addresses
            r'|https?://\S+|www\.\S+'  # URLs
            r'|\b\d+\b'  # Digits/numbers
            r'|\n\nEmail:'  # The pattern to remove "\n\nEmail:"
            r'|\n\nPage No'  # The pattern to remove "\n\nPage No"
            r'|\s:\s'  # Colons with spaces around them
            r'|:$'  # Colons at the end of lines
        )
        text = re.sub(pattern, '', text, flags=re.IGNORECASE)
        return text```
- Split text into chunks: 
``` text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=25)
    docs = text_splitter.split_documents(cleaned_data)```
- To embed chunks: `index, nodes = indexing.get_index()`


