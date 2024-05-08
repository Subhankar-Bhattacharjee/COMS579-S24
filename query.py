
import warnings
# To suppress all warnings
warnings.filterwarnings("ignore")
import argparse
from rag_files.results import results
from rag_files.indexing import Index
from rag_files.data_preprocess import Data_Processing
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader
import openai
import warnings


def answer_maker(question):
    parser = argparse.ArgumentParser(description="Retrieve answers from indexed PDF documents.")
    parser.add_argument("--question", type=str, required=True, help="Enter your question")
    args = parser.parse_args()
    directory_path = './pdf'
    Index.index_pdfs(directory_path)
    answer = results.query_documents(args.question,top_k=5)
    return answer


def main():
    parser = argparse.ArgumentParser(description="Retrieve answers from indexed PDF documents.")
    parser.add_argument("--question", type=str, required=True, help="Enter your question")
    args = parser.parse_args()
    
    directory_path = './pdf'
    Index.index_pdfs(directory_path)
    answer = results.query_documents(args.question,top_k=5)
    print("Question:", args.question)
    print("Response:", answer)

if __name__ == "__main__":
    main()



