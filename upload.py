
import argparse
from rag_files.indexing import Index
import warnings
warnings.filterwarnings("ignore")


def main():
    parser = argparse.ArgumentParser(description="Upload and index PDF documents.")
    parser.add_argument("--pdf_file", type=str, required=True, help="Path to the PDF file to index")
    args = parser.parse_args()

    # Index the specified PDF file
    Index.index_pdf(args.pdf_file)
    # client, vec = Index.index_pdf(args.pdf_file)
    # response = client.data_object.get(class_name="Document", with_vector=True)
    # print("Response", response)

if __name__ == "__main__":
    main()
    