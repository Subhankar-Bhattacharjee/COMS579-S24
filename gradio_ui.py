import gradio as gr
import warnings
from upload import upload_and_index
import query
warnings.filterwarnings("ignore")

from rag_files.results import results
from rag_files.indexing import Index

def answer_question(question):
    directory_path = './pdf'
    Index.index_pdfs(directory_path)
    answer = results.query_documents(question, top_k=5)
    return answer

def indexing_pdf(file_path):
    Index.index_pdf(file_path.name)
    return "File indexed successfully."

css = """
body { font-family: Arial, sans-serif; }
input, textarea, button { margin: 10px; }
button { background-color: #4CAF50; color: white; border: none; padding: 10px 20px; }
textarea, input[type="file"] { background-color: #f0f0f0; color: #333; border: none; padding: 10px; }
"""

with gr.Blocks(css=css) as demo:
    gr.Markdown("# DocSeek: Interactive Document Explorer")
    #gr.Markdown("![Logo](logo.pngDocSeek.png)")  # Add your logo URL here
    with gr.Row():
        with gr.Column():
            pdf_input = gr.File(label="Upload PDF")
            pdf_output = gr.Textbox(label="Indexing Status", interactive=False)
            pdf_button = gr.Button("Index PDF")
        with gr.Column():
            question_input = gr.Textbox(label="Enter your question", placeholder="Type your question here...")
            answer_output = gr.Textbox(label="Answer", interactive=False)
            question_button = gr.Button("Get Answer")

    question_button.click(answer_question, inputs=question_input, outputs=answer_output)
    pdf_button.click(indexing_pdf, inputs=pdf_input, outputs=pdf_output)

demo.launch()
