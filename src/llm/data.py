from typing import List
import os
# import chromadb
import pandas as pd
import json
from langchain.document_loaders import PyPDFLoader
from dotenv import load_dotenv
import re
# from transformers import StoppingCriteria, StoppingCriteriaList
# from transformers import TextStreamer
import nltk
# from nltk.corpus import stopwords
from collections import Counter
import time
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
import re
# nltk.download('stopwords')


# def get_most_frequent_words(book_content, num_words=10):
    
#     words = book_content.split()

#     stop_words = set(stopwords.words('english'))
#     words = [word.lower() for word in words if word.lower() not in stop_words]

#     word_freq = Counter(words)

#     most_frequent_words = word_freq.most_common(num_words)

#     return most_frequent_words


class Prompt:
    def __init__(self):
        document = SinglePDFLoader('regulations_data/raw/Regulations.pdf', clean=False)[2:]
        self.document = merge_context(document)
        self.history = {'system': [], 'user': []}
        self.history_str = ''
    def get_prompt(self, input):
        prompt = f"""
                Act as an AI Agent that speaks Arabic fluently. 
                Use This Document to Answer Questions between brackets:
                <context>
                [{self.document}]
                </context>
                I want you to be respectful and answer based on the context given to you which is a regulations for the non profit sector. 
                You should be friendly, helpful and your name is صانع. 
                Your mission is answer NPO representative and help them.
                Your Answer Should be Actual and refernecing to the number of the Articles you used to provide such accurate answer.

                <history>
                {self.get_history()}
                </history>

                <question>
                {input}
                </question>

                If you cannot find an answer ask the user to rephrase the question.
                answer:
                """
        return prompt

    def add_history(self, input, answer):
        self.history['user'].append(input)
        self.history['system'].append(answer)
  
            
        
    def get_history(self):
        if not self.history['user'] or not self.history['system']:
            return self.history_str
        template = """
        <question>
        [input]
        </question>
        <answer>
        [answer]
        </answer>
        """    
        new = template.replace('[input]',self.history['user'][-1])
        new = new.replace('[answer]',self.history['system'][-1])
        self.history_str = self.history_str + f'\n {new}'
        return (print(self.history_str), self.history_str)[1]
    
    
    
    # import openai

def clean_text(text):
    # Remove URLs, non-alphanumeric characters, forward slashes, backslashes, except dashes, underscores, asterisks, and percent signs
    cleaned_text = re.sub(r'https?://\S+|www\.\S+|[^a-zA-Z0-9\s\-_*%]', '', text)
    return cleaned_text

def PDFDirectoryLoader(path: str, clean=True):
    """
    Load PDF documents from a directory and extract their content.

    This method takes a path to a directory containing PDF files and loads the contents of each PDF document found within the directory.
    The PDF contents are extracted using the PyPDFLoader utility, and the extracted text is collected into a list of documents.

    Parameters:
    - path (str): The path to the directory containing PDF files to be loaded.

    Returns:
    A list of documents.

    Each document is loaded from a separate PDF file found within the specified directory.

    Note: The method assumes that PyPDFLoader, which is not shown in the provided code snippet, is used to extract text from PDF files.
    Additionally, a message '>>>a File was loaded<<<' is printed for each successfully loaded file.
    """
    
    documents_list = []
    files =  os.listdir(path)
    for file in files:
        loader = PyPDFLoader(os.path.join(path, file))
        documents = loader.load()
        documents_list.extend(documents)
        print('>>>a File was loaded<<<')
        
    filtered_list = []
    for doc in documents_list:
        if not doc.page_content=='':
            if clean:
                doc.page_content = clean_text(doc.page_content)
            filtered_list.append(doc)
    print('>>>Removed empty pages<<<')
    return filtered_list



def SinglePDFLoader(file: str, clean=True):
    """
    Load a single PDF file and split it into multiple documents, each representing a single page.

    This method takes a single PDF file and uses the PyPDFLoader utility to load and split the PDF content into multiple documents.
    Each document corresponds to a single page from the provided PDF file.

    Parameters:
    - file (str): The path to the PDF file to be loaded and split.

    Returns:
    - A list of documents, where each document is representing the content of a single page from the PDF file.

    Note: The method prints the message '>>>a File was loaded<<<' to indicate that the file has been successfully loaded and split.
    """
    
    loader = PyPDFLoader(file, )
    # Load and split the document into multiple documents, each document represent a single page. 
    documents = loader.load()
    print('>>>a PDF File was loaded<<<')
    
    filtered_list = []
    for doc in documents:
        if not doc.page_content=='':
            if clean:
                doc.page_content = clean_text(doc.page_content)
            filtered_list.append(doc)
    print('>>>Removed empty pages<<<')
    return filtered_list



def merge_context(docs):
    full_context = ""
    for doc in docs: 
        full_context=full_context +' '+doc.page_content
    print(">>>Successfully Merged Documents<<<")
    return full_context


def paragraph_splitter(dir):
    full_text = ''
    files = [file for file in os.listdir(dir) if file.split('.')[-1] == 'txt'] # Azure usually store temp files, and we only need text files 
    for file in files:
        with open(os.path.join(dir, file)) as f:
            text = f.read()
        full_text += '\n\n' + text
    
    return full_text.split('\n\n')

def preprocess_generated_text(text:str, last_prompt_word='SUMMARY:'):
    return text.split(last_prompt_word)[-1].replace('[/INST]', '').replace('</s>', '').replace('```','').replace('=','').replace('#','').replace('---', '')

    


def standardize_text(text):
  """
  Standardizes the formatting of a given text string.

  Args:
    text: A string containing the text to be standardized.

  Returns:
    A string with standardized formatting.
  """

  # Lowercase text
  # text = text.lower()

  # Remove leading and trailing whitespace
  text = text.strip()

  # Fix whitespace inconsistencies
  text = re.sub(r"\s+", " ", text)
  # text = re.sub(r'[ \t]+', ' ', text)
  # Replace multiple new lines with two new lines
  # text = re.sub(r'\n\s*\n', '\n\n', text) 


  # Apply sentence casing
  # text = text.replace("\n", " ")
  # text = re.sub(r"[.?!]\s+", ". ", text)
  # text = text.capitalize()

  # Fix common typos
  text = text.replace(" ' ", "'")
  text = text.replace(" n't ", "n't ")

  # Remove unnecessary punctuation
  text = re.sub(r"[^\w\s\.\,\?\!'\-]", "", text)

  return text

def clean_text_heavy(text):
    # Remove special characters (excluding period, new lines, and tabs) and keep numbers
    text = re.sub(r'[^a-zA-Z0-9.\s\n\t:\/]', ' ', text)
    text = standardize_text(text)
    return text