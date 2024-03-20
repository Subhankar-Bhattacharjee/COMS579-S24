
import os
import shutil
import re

class Data_Processing:
    def clean_text(text):
        # Remove common unwanted patterns (e.g., page numbers, specific keywords)
        text = re.sub(r'\bPage \d+\b', '', text)
        # Add other patterns here as needed
        return text
    
    def clean_documents(documents):
        for doc in documents:
            doc.page_content = Data_Processing.clean_text(doc.page_content)
        return documents