import re
from typing import List, Tuple
import numpy as np


class TextHighlighter:

    def __init__(self, embedding_function=None):
        self.embedding_function = embedding_function

    def _extract_keywords(self, query: str) -> List[str]:
        stop_words = {
            "what",
            "is",
            "the",
            "a",
            "an",
            "how",
            "why",
            "when",
            "where",
            "who",
            "which",
            "can",
            "could",
            "would",
            "should",
            "do",
            "does",
            "are",
            "was",
            "were",
            "been",
            "be",
            "have",
            "has",
            "had",
            "to",
            "of",
            "in",
            "on",
            "at",
            "for",
            "with",
            "about",
            "as",
            "by",
        }

        words = re.findall(r"\b\w+\b", query.lower())
        keywords = [w for w in words if w not in stop_words and len(w) > 2]
        return keywords

    def _split_into_sentences(self, text: str) -> List[str]:
        sentences = re.split(r"[.!?]+", text)
        return [s.strip() for s in sentences if s.strip()]

    def _calculate_sentence_similarity(
        self, query: str, sentences: List[str]
    ) -> List[float]:
        if not self.embedding_function or not sentences:
            return [0.0] * len(sentences)

        try:
            query_embedding = self.embedding_function([query])[0]
            sentence_embeddings = self.embedding_function(sentences)

            similarities = []
            for sent_emb in sentence_embeddings:
                similarity = np.dot(query_embedding, sent_emb) / (
                    np.linalg.norm(query_embedding) * np.linalg.norm(sent_emb)
                )
                similarities.append(float(similarity))

            return similarities
        except:
            return [0.0] * len(sentences)

    def highlight_text(
        self, text: str, query: str, similarity_threshold: float = 0.5
    ) -> str:
        if not text or not query:
            return text

        text = re.sub(r'\n\s*\n', '\n\n', text)
        text = re.sub(r'[ \t]+', ' ', text)
        text = text.strip()

        keywords = self._extract_keywords(query)

        sentences = self._split_into_sentences(text)

        similarities = self._calculate_sentence_similarity(query, sentences)

        highlighted_text = text

        for sentence, similarity in zip(sentences, similarities):
            if similarity >= similarity_threshold and sentence in highlighted_text:
                intensity = int(255 - (similarity * 100))
                color = f"rgb(144, 238, {intensity})"

                highlighted_sentence = f'<span style="background-color: {color}; padding: 2px 4px; border-radius: 3px; color: #2c3e50; display: inline;" title="Relevance: {similarity:.0%}">{sentence}</span>'
                highlighted_text = highlighted_text.replace(
                    sentence, highlighted_sentence, 1
                )

        for keyword in keywords:
            parts = re.split(r'(<[^>]+>)', highlighted_text)
            
            for i, part in enumerate(parts):
                if not part.startswith('<'):
                    pattern = re.compile(r'\b' + re.escape(keyword) + r'\b', re.IGNORECASE)
                    
                    def replace_func(match):
                        matched_text = match.group(0)
                        return f'<mark style="background-color: #ffeb3b; padding: 2px 4px; border-radius: 3px; font-weight: 600; color: #2c3e50; display: inline;">{matched_text}</mark>'
                    
                    parts[i] = pattern.sub(replace_func, part)
            
            highlighted_text = ''.join(parts)

        return highlighted_text

    def get_highlight_legend(self) -> str:
        return """
        <div style="margin: 10px 0; padding: 10px; background-color: #f8f9fa; border-radius: 5px; font-size: 0.85rem; color: #2c3e50;">
            <strong style="color: #2c3e50;">Highlight Guide:</strong>
            <span style="background-color: #ffeb3b; padding: 2px 6px; margin: 0 5px; border-radius: 3px; font-weight: 600; color: #2c3e50;">Yellow</span> 
            <span style="color: #2c3e50;">= Keywords from the answer</span>
            <span style="background-color: rgb(144, 238, 200); padding: 2px 6px; margin: 0 5px; border-radius: 3px; color: #2c3e50;">Green</span> 
            <span style="color: #2c3e50;">= Content used in the answer</span>
        </div>
        """
