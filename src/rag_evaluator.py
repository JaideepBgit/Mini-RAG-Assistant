import re
import numpy as np
from typing import List, Dict, Tuple, Optional
from langchain_core.documents import Document


class RAGEvaluator:
    
    def __init__(self, llm_client=None):
        self.llm_client = llm_client
    
    def precision_at_k(
        self, 
        retrieved_docs: List[Tuple[Document, float]], 
        relevant_doc_ids: List[str],
        k: int = 3
    ) -> float:
        if not retrieved_docs or k <= 0:
            return 0.0
        
        top_k_docs = retrieved_docs[:k]
        relevant_count = 0
        
        for doc, _ in top_k_docs:
            doc_id = doc.metadata.get('source', '') + str(doc.metadata.get('chunk_id', ''))
            if doc_id in relevant_doc_ids or doc.metadata.get('source', '') in relevant_doc_ids:
                relevant_count += 1
        
        return relevant_count / min(k, len(top_k_docs))
    
    def recall_at_k(
        self,
        retrieved_docs: List[Tuple[Document, float]],
        relevant_doc_ids: List[str],
        k: int = 5
    ) -> float:
        if not relevant_doc_ids or not retrieved_docs:
            return 0.0
        
        top_k_docs = retrieved_docs[:k]
        retrieved_relevant = 0
        
        for doc, _ in top_k_docs:
            doc_id = doc.metadata.get('source', '') + str(doc.metadata.get('chunk_id', ''))
            if doc_id in relevant_doc_ids or doc.metadata.get('source', '') in relevant_doc_ids:
                retrieved_relevant += 1
        
        return retrieved_relevant / len(relevant_doc_ids)
    
    def mean_reciprocal_rank(
        self,
        retrieved_docs: List[Tuple[Document, float]],
        relevant_doc_ids: List[str]
    ) -> float:
        if not retrieved_docs or not relevant_doc_ids:
            return 0.0
        
        for rank, (doc, _) in enumerate(retrieved_docs, 1):
            doc_id = doc.metadata.get('source', '') + str(doc.metadata.get('chunk_id', ''))
            if doc_id in relevant_doc_ids or doc.metadata.get('source', '') in relevant_doc_ids:
                return 1.0 / rank
        
        return 0.0
    
    def grounding_accuracy(
        self,
        answer: str,
        retrieved_docs: List[Tuple[Document, float]],
        use_llm: bool = True
    ) -> Dict[str, float]:
        if not retrieved_docs or not answer:
            return {'grounding_score': 0.0, 'method': 'empty'}
        
        # Method 1: LLM-based evaluation (most accurate)
        if use_llm and self.llm_client:
            return self._llm_grounding_check(answer, retrieved_docs)
        
        return self._keyword_grounding_check(answer, retrieved_docs)
    
    def _llm_grounding_check(
        self,
        answer: str,
        retrieved_docs: List[Tuple[Document, float]]
    ) -> Dict[str, float]:
        context = "\n\n".join([doc.page_content for doc, _ in retrieved_docs])
        
        prompt = f"""Evaluate if the ANSWER is supported by the CONTEXT. Rate on a scale of 0-100.

CONTEXT:
{context}

ANSWER:
{answer}

Respond with ONLY a number between 0-100.

Score:"""
        
        try:
            if hasattr(self.llm_client, 'invoke'):
                response = self.llm_client.invoke(prompt)
                numbers = re.findall(r'\d+', str(response))
                if numbers:
                    score = int(numbers[0])
                    return {'grounding_score': min(max(score, 0), 100) / 100, 'method': 'llm'}
            elif hasattr(self.llm_client, 'chat'):
                response = self.llm_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0,
                    max_tokens=10
                )
                text = response.choices[0].message.content
                numbers = re.findall(r'\d+', text)
                if numbers:
                    score = int(numbers[0])
                    return {'grounding_score': min(max(score, 0), 100) / 100, 'method': 'llm'}
        except:
            pass
        
        return self._keyword_grounding_check(answer, retrieved_docs)
    
    def _keyword_grounding_check(
        self,
        answer: str,
        retrieved_docs: List[Tuple[Document, float]]
    ) -> Dict[str, float]:
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                     'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been'}
        
        answer_words = set(re.findall(r'\b\w+\b', answer.lower()))
        answer_words = answer_words - stop_words
        
        if not answer_words:
            return {'grounding_score': 0.0, 'method': 'keyword'}
        
        context_text = " ".join([doc.page_content.lower() for doc, _ in retrieved_docs])
        context_words = set(re.findall(r'\b\w+\b', context_text))
        
        overlap = len(answer_words & context_words)
        score = overlap / len(answer_words)
        
        return {'grounding_score': score, 'method': 'keyword'}
    
    def answer_relevancy(
        self,
        question: str,
        answer: str,
        use_llm: bool = True
    ) -> Dict[str, float]:
        if not question or not answer:
            return {'relevancy_score': 0.0, 'method': 'empty'}
        
        if use_llm and self.llm_client:
            return self._llm_relevancy_check(question, answer)
        
        return self._keyword_relevancy_check(question, answer)
    
    def _llm_relevancy_check(
        self,
        question: str,
        answer: str
    ) -> Dict[str, float]:
        prompt = f"""Rate how well the ANSWER addresses the QUESTION on a scale of 0-100.

QUESTION:
{question}

ANSWER:
{answer}

Respond with ONLY a number between 0-100.

Score:"""
        
        try:
            if hasattr(self.llm_client, 'invoke'):
                response = self.llm_client.invoke(prompt)
                numbers = re.findall(r'\d+', str(response))
                if numbers:
                    score = int(numbers[0])
                    return {'relevancy_score': min(max(score, 0), 100) / 100, 'method': 'llm'}
            elif hasattr(self.llm_client, 'chat'):
                response = self.llm_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0,
                    max_tokens=10
                )
                text = response.choices[0].message.content
                numbers = re.findall(r'\d+', text)
                if numbers:
                    score = int(numbers[0])
                    return {'relevancy_score': min(max(score, 0), 100) / 100, 'method': 'llm'}
        except:
            pass
        
        return self._keyword_relevancy_check(question, answer)
    
    def _keyword_relevancy_check(
        self,
        question: str,
        answer: str
    ) -> Dict[str, float]:
        question_words = set(re.findall(r'\b\w+\b', question.lower()))
        answer_words = set(re.findall(r'\b\w+\b', answer.lower()))
        
        if not question_words:
            return {'relevancy_score': 0.0, 'method': 'keyword'}
        
        overlap = len(question_words & answer_words)
        score = overlap / len(question_words)
        
        return {'relevancy_score': min(score, 1.0), 'method': 'keyword'}
    
    def evaluate_full(
        self,
        question: str,
        answer: str,
        retrieved_docs: List[Tuple[Document, float]],
        relevant_doc_ids: Optional[List[str]] = None,
        k: int = 3
    ) -> Dict:
        results = {
            'grounding': self.grounding_accuracy(answer, retrieved_docs, use_llm=True),
            'relevancy': self.answer_relevancy(question, answer, use_llm=True),
            'num_retrieved': len(retrieved_docs),
            'avg_retrieval_score': np.mean([1/(1+score) for _, score in retrieved_docs]) if retrieved_docs else 0.0
        }
        
        if relevant_doc_ids:
            results['precision_at_k'] = self.precision_at_k(retrieved_docs, relevant_doc_ids, k)
            results['recall_at_k'] = self.recall_at_k(retrieved_docs, relevant_doc_ids, k)
            results['mrr'] = self.mean_reciprocal_rank(retrieved_docs, relevant_doc_ids)
        
        return results
