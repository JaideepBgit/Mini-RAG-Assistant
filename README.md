Mini RAG Assistant

Problem Statement

This project addresses the challenge faced by consulting firms managing multiple client knowledge repositories. Currently, analysts manually search through internal policies, process manuals, and product guides to find answers, which is slow and error-prone. This RAG Assistant demonstrates how retrieval-augmented generation can automate this process while maintaining accuracy and transparency.

Solution Overview

The Mini RAG Assistant is a lightweight prototype that processes local documents, retrieves relevant information using semantic search, and generates grounded responses with confidence scoring. It supports both cloud-based OpenAI and local Ollama models, giving flexibility in deployment options.

Key Features

Document Processing: Upload and parse PDF and text files into a searchable knowledge base
Semantic Retrieval: Uses FAISS vector database with embedding-based similarity search to find relevant context
Grounded Generation: LLM responses are strictly based on retrieved documents, reducing hallucination
Confidence Scoring: Each answer includes a 0-100 confidence score indicating reliability
Source Citations: Displays retrieved document chunks with relevance scores for transparency
Dual Provider Support: Switch between OpenAI cloud models and local Ollama models
Auto-Loading: Automatically processes documents from the docs folder on startup

Architecture and Design Flow

The system follows a standard RAG pipeline with these components:

1. Document Ingestion: Documents are loaded from uploads or the docs folder, then split into chunks using RecursiveCharacterTextSplitter with 1000 character chunks and 200 character overlap.

2. Embedding and Indexing: Text chunks are converted to vector embeddings using either OpenAI text-embedding-3-small or local all-MiniLM-L6-v2 model. Vectors are stored in FAISS index for fast similarity search.

3. Retrieval: User queries are embedded and compared against the vector store using cosine similarity. Top K most relevant chunks are retrieved with distance scores.

4. Generation: Retrieved context is formatted and passed to the LLM with the user question. The LLM generates an answer using only the provided context.

5. Confidence Scoring: A secondary LLM call evaluates how well the context supports the answer, returning a 0-100 confidence score.

6. Response Display: The answer is shown with confidence score and expandable source citations showing exact text chunks used.

Setup Instructions

Install dependencies:
pip install -r requirements.txt

For OpenAI setup, create a .env file:
LLM_PROVIDER=openai
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4o-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-small

For Ollama setup, install Ollama from ollama.ai, pull a model with ollama pull qwen2.5:0.5b, then create a .env file:
LLM_PROVIDER=ollama
OLLAMA_MODEL=qwen2.5:0.5b

Run the application:
streamlit run app.py

The interface opens at http://localhost:8501

How to Use

Add documents by either uploading files through the sidebar or placing them in the docs folder. The system automatically processes new documents on startup.

Ask questions by typing in the text input and clicking Ask. The system retrieves relevant context, generates an answer, and displays confidence score with source citations.

View sources by expanding the sources section below each answer to see the actual document chunks used, their relevance scores, and source file names.

Switch providers using the radio button in the sidebar. Each provider maintains its own vector store.

Retrieval and Grounding Methodology

Retrieval Accuracy: The system uses FAISS for efficient similarity search with cosine distance. Relevance scores are calculated as 1 divided by 1 plus distance, giving higher scores to more similar chunks. The default retrieval count is 4 chunks but can be adjusted from 1 to 10.

Grounding Transparency: Every answer explicitly shows which document chunks were used. This allows users to verify the information and understand the basis for each response. Source citations include document name, chunk ID, relevance score, and content preview.

Hallucination Reduction: The generation prompt instructs the LLM to answer only using provided context. If information is not in the retrieved chunks, the system states it does not have enough information rather than making up answers.

Confidence Scoring Method

Confidence scores are generated through a secondary LLM evaluation that assesses how well the retrieved context supports the generated answer. The scoring considers:

Coverage: Does the context contain information needed to answer the question
Accuracy: Is the answer faithful to the context without adding unsupported claims
Completeness: Does the answer address all aspects of the question

Scores are interpreted as:
90-100: High confidence, answer fully supported by context
70-89: Good confidence, answer mostly supported with minor gaps
50-69: Moderate confidence, partial support from context
0-49: Low confidence, limited support or potential inaccuracies

Technical Stack

Framework: Streamlit for web interface
Orchestration: LangChain for RAG pipeline components
Vector Store: FAISS for efficient similarity search
Embeddings: OpenAI text-embedding-3-small or local all-MiniLM-L6-v2
LLM: OpenAI GPT-4o-mini or Ollama models like Qwen2.5
Document Processing: PyPDF2 for PDF parsing, RecursiveCharacterTextSplitter for chunking

Project Structure

app.py: Main Streamlit application with UI and workflow logic
src/document_processor.py: Handles PDF and text file parsing and chunking
src/vector_store.py: FAISS vector store management for OpenAI embeddings
src/vector_store_ollama.py: FAISS vector store management for local embeddings
src/rag_pipeline.py: RAG pipeline implementation for OpenAI
src/rag_pipeline_ollama.py: RAG pipeline implementation for Ollama
src/auto_loader.py: Automatic document loading from docs folder
src/rag_evaluator.py: Evaluation metrics including precision at k and grounding accuracy
docs/: Folder for documents to be auto-loaded
requirements.txt: Python dependencies

Example Usage

Sample queries you can try:
What is the vacation leave policy?
How many sick days do employees get?
What is the remote work eligibility?
How do I submit expense claims?
What are the security requirements for handling client data?

Expected output includes:
A natural language answer based on the documents
Confidence score between 0 and 100
List of source documents with relevance scores
Expandable view showing exact text chunks used

Evaluation Metrics

The system includes optional evaluation capabilities in src/rag_evaluator.py:

Precision at K: Measures proportion of relevant documents in top K results
Recall at K: Measures proportion of relevant documents that were retrieved
Mean Reciprocal Rank: Evaluates ranking quality of retrieved documents
Grounding Accuracy: Assesses whether answers are supported by context
Answer Relevancy: Evaluates how well answers address the questions

These metrics can be used to benchmark and improve retrieval quality over time.

Provider Comparison

OpenAI provides high quality responses with fast processing but requires API costs and sends data to the cloud. Setup is simple with just an API key.

Ollama runs completely locally with no costs and full data privacy. Speed depends on your hardware. Quality is good but may not match OpenAI. Requires downloading models which can be several gigabytes.

Troubleshooting

If Ollama is not connecting, ensure Ollama is running with ollama serve and verify your model is installed with ollama list.

If OpenAI returns errors, check your API key in the .env file and verify your account has available credits.

If documents are not loading, confirm files are in the docs folder or uploaded through the UI. Only PDF and TXT formats are supported.

If answers seem incorrect, try increasing the number of retrieved sources in the sidebar settings or reprocess documents using the Reprocess Docs Folder button.

Future Enhancements

Given more time, potential improvements include:

Multi-turn conversation with context retention across questions
Hybrid search combining semantic and keyword matching
Query expansion to improve retrieval for ambiguous questions
Chunk reranking using cross-encoders for better relevance
Support for additional file formats like DOCX and CSV
Batch evaluation mode for testing multiple queries
User feedback collection to improve retrieval over time
Advanced visualization of document relationships and coverage

Conclusion

This prototype demonstrates how RAG systems can transform document search from manual lookup to intelligent question answering. By combining semantic retrieval with grounded generation and confidence scoring, it provides accurate, verifiable answers while maintaining transparency about information sources. The dual provider support shows flexibility in deployment options based on cost, privacy, and quality requirements.
