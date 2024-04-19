# Suppress warnings
import warnings
warnings.filterwarnings("ignore")
import re
import openai
import weaviate
from langchain.embeddings.openai import OpenAIEmbeddings
import weaviate
import os
from transformers import AutoTokenizer, AutoModel
import torch
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from langchain.vectorstores.weaviate import Weaviate
from langchain.llms import OpenAI
import weaviate
from langchain.chains import LLMChain
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
import textwrap
from time import monotonic
import tiktoken
from langchain_core.documents import Document
from dotenv import load_dotenv,find_dotenv
load_dotenv(find_dotenv())


def num_tokens_from_string(string: str, encoding_name: str) -> int:    
    encoding = tiktoken.encoding_for_model(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens



def summarize(content):
        #print(content)
        openai_api_key = os.getenv('OPENAI_API_KEY')
        docs = Document(page_content=content, metadata={"source": "local"})
        openai.api_key = openai_api_key
        model_name = "gpt-3.5-turbo"
        llm = ChatOpenAI(temperature=0, openai_api_key=openai_api_key, model_name=model_name)
        prompt_template = """Write a concise summary of the following: {text}"""
        prompt = PromptTemplate(template=prompt_template, input_variables=["text"])
        num_tokens = num_tokens_from_string(content, model_name)
        #print(num_tokens)
        gpt_35_turbo_max_tokens = 4097
        verbose = False

        if num_tokens < gpt_35_turbo_max_tokens:
            chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt, verbose=verbose)
        else:
            chain = load_summarize_chain(llm, chain_type="map_reduce", map_prompt=prompt, combine_prompt=prompt, verbose=verbose)

        summary = chain.run([docs])
        
        return summary

class results:
    weaviate_api_key = os.getenv('WEAVIATE_API_KEY')
    weaviate_url = os.getenv('WEAVIATE_URL')
    openai_api_key = os.getenv('OPENAI_API_KEY')
    openai.api_key = openai_api_key
    auth_config = weaviate.AuthApiKey(api_key=weaviate_api_key)
    client = weaviate.Client(url=weaviate_url, auth_client_secret=auth_config)
    llm = OpenAI(api_key=openai_api_key)

    def query_documents(query, top_k=10):
        weaviate_api_key = os.getenv('WEAVIATE_API_KEY')
        weaviate_url = os.getenv('WEAVIATE_URL')
        openai_api_key = os.getenv('OPENAI_API_KEY')
        auth_config = weaviate.AuthApiKey(api_key=weaviate_api_key)
        client = weaviate.Client(url=weaviate_url, auth_client_secret=weaviate.AuthApiKey(api_key=weaviate_api_key))

        # Use the query parameter instead of a hardcoded query string
        resultset = client.query.get("Document", ["content", "pdfName"]) \
            .with_bm25(query=query) \
            .with_additional("score") \
            .with_limit(top_k) \
            .do()

        # Print results in a formatted manner
        if 'data' in resultset and 'Get' in resultset['data'] and 'Document' in resultset['data']['Get']:
            documents = resultset['data']['Get']['Document']
            rank=1
            for doc in documents:
                content = doc['content']
                pdf_name = doc['pdfName']
                score = doc['_additional']['score']
                print(f"PDF Name: {pdf_name}, Content: {content}, Score: {score}, Rank: {rank}, \n")
                rank+= 1
            
            for doc in documents:
                content = doc['content']
                summary = summarize(content)
                #print("Summary:", summary)
                break
            return summary
        else:
            print("No documents found.")
            return "No relevant answer found"
        








