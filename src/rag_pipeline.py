import numpy as np
from typing import List, Dict, Tuple, Optional
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import openai
from .rag_evaluator import RAGEvaluator

class RAGPipeline:
    def __init__(self, openai_api_key: str, model: str = "gpt-4o-mini"):
        self.llm = ChatOpenAI(
            openai_api_key=openai_api_key,
            model=model,
            temperature=0
        )
        self.api_key = openai_api_key
        self.model_name = model
        self.openai_client = openai.OpenAI(api_key=openai_api_key)
        
        self.rag_prompt = ChatPromptTemplate.from_template("""
Answer the question using only the provided context.

Context:
{context}

Question: {question}

Answer:
""")
        
        self.confidence_prompt = ChatPromptTemplate.from_template("""
Rate the confidence level on a scale of 0-100.

Context:
{context}

Question: {question}

Answer: {answer}

Provide ONLY a number between 0-100.

Score:
""")
    
    def format_documents(self, docs: List[Tuple[Document, float]]) -> str:
        formatted = []
        for i, (doc, score) in enumerate(docs, 1):
            source = doc.metadata.get('source', 'Unknown')
            content = doc.page_content
            formatted.append(f"[Source {i}: {source}]\n{content}\n")
        return "\n".join(formatted)
    
    def generate_answer(self, question: str, retrieved_docs: List[Tuple[Document, float]]) -> str:
        if not retrieved_docs:
            return "I don't have enough information to answer this question."
        
        context = self.format_documents(retrieved_docs)
        chain = self.rag_prompt | self.llm | StrOutputParser()
        answer = chain.invoke({
            "context": context,
            "question": question
        })
        return answer
    
    def calculate_confidence(self, question: str, answer: str, retrieved_docs: List[Tuple[Document, float]]) -> int:
        context = self.format_documents(retrieved_docs)
        confidence_score = 50
        
        try:
            chain = self.confidence_prompt | self.llm | StrOutputParser()
            score_str = chain.invoke({
                "context": context,
                "question": question,
                "answer": answer
            })
            score = int(''.join(filter(str.isdigit, score_str)))
            confidence_score = min(max(score, 0), 100)
        except:
            confidence_score = 50
        
        return confidence_score
    
    def query(self, question: str, retrieved_docs: List[Tuple[Document, float]]) -> Dict:
        answer = self.generate_answer(question, retrieved_docs)
        confidence = self.calculate_confidence(question, answer, retrieved_docs)
        
        sources = []
        for doc, score in retrieved_docs:
            content = doc.page_content
            if len(content) > 500:
                content = content[:500] + "..."
            
            sources.append({
                "source": doc.metadata.get('source', 'Unknown'),
                "chunk_id": doc.metadata.get('chunk_id', 0),
                "content": content,
                "relevance_score": float(1 / (1 + score))
            })
        
        return {
            "answer": answer,
            "confidence": confidence,
            "sources": sources,
            "num_sources": len(sources)
        }

