import os
import shutil
import glob

class PDFLoader:
    
    def load_pdf(file_path):
        if file_path.lower().endswith(".pdf"):
            # Remove all existing PDF files in the ./pdfs directory
            existing_pdfs = glob.glob("./pdfs/*.pdf")
            for pdf in existing_pdfs:
                os.remove(pdf)

            # Copy the new PDF file to the ./pdfs directory
            shutil.copy(file_path, "./pdfs")
            return True
        else:
            return False