import re
import numpy as np
from typing import List, Dict, Tuple
from langchain_core.documents import Document
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate

class RAGPipeline:
    def __init__(self, model: str = "qwen2.5:0.5b", base_url: str = "http://localhost:11434"):
        self.llm = Ollama(
            model=model,
            base_url=base_url,
            temperature=0
        )
        self.model_name = model
        self.base_url = base_url
        
        self.rag_prompt = PromptTemplate.from_template("""
You are a helpful AI assistant that answers questions based on the provided context.

Context:
{context}

Question: {question}

Instructions:
1. Answer using ONLY the information from the context above
2. If the context doesn't contain enough information, say so clearly
3. Cite the source document when providing information
4. Be concise and accurate

Answer:
""")
        
        self.confidence_prompt = PromptTemplate.from_template("""
Based on the following context and answer, rate the confidence level on a scale of 0-100.

Context:
{context}

Question: {question}

Answer: {answer}

Provide ONLY a number between 0-100 where:
- 90-100: High confidence, fully supported by context
- 70-89: Good confidence, mostly supported
- 50-69: Moderate confidence, partial support
- 0-49: Low confidence, limited support

Confidence Score (number only):
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
        prompt = self.rag_prompt.format(context=context, question=question)
        answer = self.llm.invoke(prompt)
        return answer.strip()
    
    def calculate_confidence(self, question: str, answer: str, retrieved_docs: List[Tuple[Document, float]]) -> int:
        context = self.format_documents(retrieved_docs)
        confidence_score = 50
        
        try:
            prompt = self.confidence_prompt.format(
                context=context,
                question=question,
                answer=answer
            )
            score_str = self.llm.invoke(prompt)
            numbers = re.findall(r'\d+', score_str)
            if numbers:
                score = int(numbers[0])
                confidence_score = min(max(score, 0), 100)
        except Exception as e:
            # Fallback to default if prompt fails
            confidence_score = 50
        
        return confidence_score
    
    def query(self, question: str, retrieved_docs: List[Tuple[Document, float]]) -> Dict:
        answer = self.generate_answer(question, retrieved_docs)
        confidence = self.calculate_confidence(question, answer, retrieved_docs)
        
        sources = []
        for doc, score in retrieved_docs:
            content = doc.page_content
            # Truncate if too long, but show full content if reasonable
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

