import re

class Data_Processing:
    def clean_text(text):
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
        return text
    
    def clean_documents(documents):
        for doc in documents:
            doc.page_content = Data_Processing.clean_text(doc.page_content)
        return documents
