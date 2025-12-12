import numpy as np
from typing import List, Dict, Tuple, Optional
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import openai
from .rag_evaluator import RAGEvaluator
from .text_highlighter import TextHighlighter

class RAGPipeline:
    def __init__(self, openai_api_key: str, model: str = "gpt-4o-mini", embedding_model: str = "text-embedding-3-small"):
        self.llm = ChatOpenAI(
            openai_api_key=openai_api_key,
            model=model,
            temperature=0
        )
        self.api_key = openai_api_key
        self.model_name = model
        self.embedding_model = embedding_model
        self.openai_client = openai.OpenAI(api_key=openai_api_key)
        
        self.highlighter = TextHighlighter(embedding_function=self._get_embeddings)
        
        self.rag_prompt = ChatPromptTemplate.from_template("""
Answer the question using only the provided context. You must cite sources for every claim you make.

{conversation_history}

Context:
{context}

Question: {question}

Instructions:
- If conversation history is provided above, use it to understand what "it", "that", "them" or other pronouns refer to
- If the current question is a follow-up (like "how do I request it?"), interpret "it" based on the previous conversation
- Answer using ONLY information from the context above
- For each statement or fact, cite the source number in brackets like [Source 1] or [Source 2]
- If multiple sources support a claim, cite all of them like [Source 1, Source 3]
- If the context doesn't contain enough information, clearly state that
- Be specific and cite sources after each relevant sentence

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
    
    def _get_embeddings(self, texts: List[str]) -> List[np.ndarray]:
        try:
            response = self.openai_client.embeddings.create(
                input=texts,
                model=self.embedding_model
            )
            return [np.array(item.embedding) for item in response.data]
        except:
            return [np.zeros(1536) for _ in texts]
    
    def format_documents(self, docs: List[Tuple[Document, float]]) -> str:
        formatted = []
        for i, (doc, score) in enumerate(docs, 1):
            source = doc.metadata.get('source', 'Unknown')
            content = doc.page_content
            formatted.append(f"[Source {i}: {source}]\n{content}\n")
        return "\n".join(formatted)
    
    def generate_answer(self, question: str, retrieved_docs: List[Tuple[Document, float]], conversation_history: Optional[List[Dict]] = None) -> str:
        if not retrieved_docs:
            return "I don't have enough information to answer this question."
        
        context = self.format_documents(retrieved_docs)
        
        history_text = ""
        if conversation_history:
            history_text = "Previous conversation:\n"
            for i, chat in enumerate(conversation_history, 1):
                history_text += f"Q{i}: {chat['question']}\nA{i}: {chat['answer']}\n\n"
        
        chain = self.rag_prompt | self.llm | StrOutputParser()
        answer = chain.invoke({
            "context": context,
            "question": question,
            "conversation_history": history_text
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
    
    def query(self, question: str, retrieved_docs: List[Tuple[Document, float]], enable_highlighting: bool = True, conversation_history: Optional[List[Dict]] = None) -> Dict:
        answer = self.generate_answer(question, retrieved_docs, conversation_history)
        confidence = self.calculate_confidence(question, answer, retrieved_docs)
        
        sources = []
        for doc, score in retrieved_docs:
            content = doc.page_content
            
            display_content = content if len(content) <= 500 else content[:500] + "..."
            
            if enable_highlighting:
                display_content = self.highlighter.highlight_text(display_content, answer)
            
            sources.append({
                "source": doc.metadata.get('source', 'Unknown'),
                "chunk_id": doc.metadata.get('chunk_id', 0),
                "content": display_content,
                "relevance_score": float(1 / (1 + score))
            })
        
        return {
            "answer": answer,
            "confidence": confidence,
            "sources": sources,
            "num_sources": len(sources),
            "highlight_legend": self.highlighter.get_highlight_legend() if enable_highlighting else ""
        }

