import os
from typing import List, Tuple
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

class VectorStoreManager:
    def __init__(self, openai_api_key: str, persist_directory: str = "vector_store", embedding_model: str = "text-embedding-3-small"):
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=openai_api_key,
            model=embedding_model
        )
        self.persist_directory = persist_directory
        self.vector_store = None
        self.embedding_model = embedding_model
        os.makedirs(persist_directory, exist_ok=True)
    
    def create_vector_store(self, documents: List[Document]) -> FAISS:
        if not documents:
            raise ValueError("No documents provided")
        self.vector_store = FAISS.from_documents(documents, self.embeddings)
        return self.vector_store
    
    def add_documents(self, documents: List[Document]):
        if self.vector_store is None:
            raise ValueError("Vector store not initialized")
        self.vector_store.add_documents(documents)
    
    def similarity_search(self, query: str, k: int = 4) -> List[Tuple[Document, float]]:
        if self.vector_store is None:
            raise ValueError("Vector store not initialized")
        return self.vector_store.similarity_search_with_score(query, k=k)
    
    def save(self, index_name: str = "faiss_index"):
        if self.vector_store is None:
            raise ValueError("No vector store to save")
        index_path = os.path.join(self.persist_directory, index_name)
        self.vector_store.save_local(index_path)
    
    def load(self, index_name: str = "faiss_index") -> FAISS:
        index_path = os.path.join(self.persist_directory, index_name)
        if not os.path.exists(index_path):
            raise FileNotFoundError(f"No saved index found at {index_path}")
        self.vector_store = FAISS.load_local(
            index_path, 
            self.embeddings,
            allow_dangerous_deserialization=True
        )
        return self.vector_store
    
    def get_stats(self) -> dict:
        if self.vector_store is None:
            return {"status": "not_initialized"}
        return {
            "status": "initialized",
            "num_vectors": self.vector_store.index.ntotal,
            "dimension": self.vector_store.index.d
        }

