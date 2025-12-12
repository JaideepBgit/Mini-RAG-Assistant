import os
from typing import List
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

class DocumentProcessor:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
    
    def load_pdf(self, file_path: str) -> str:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    
    def load_text(self, file_path: str) -> str:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def process_document(self, file_path: str) -> List[Document]:
        file_ext = os.path.splitext(file_path)[1].lower()
        if file_ext == '.pdf':
            text = self.load_pdf(file_path)
        elif file_ext == '.txt':
            text = self.load_text(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_ext}")
        
        chunks = self.text_splitter.split_text(text)
        documents = []
        filename = os.path.basename(file_path)
        
        for i, chunk in enumerate(chunks):
            doc = Document(
                page_content=chunk,
                metadata={
                    "source": filename,
                    "chunk_id": i,
                    "total_chunks": len(chunks)
                }
            )
            documents.append(doc)
        return documents
    
    def process_multiple_documents(self, file_paths: List[str]) -> List[Document]:
        all_documents = []
        for file_path in file_paths:
            docs = self.process_document(file_path)
            all_documents.extend(docs)
        return all_documents

