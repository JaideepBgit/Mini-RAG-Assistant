import os
import streamlit as st
from dotenv import load_dotenv
from src.document_processor import DocumentProcessor
from src.vector_store import VectorStoreManager as OpenAIVectorStore
from src.vector_store_ollama import VectorStoreManager as OllamaVectorStore
from src.rag_pipeline import RAGPipeline as OpenAIRAGPipeline
from src.rag_pipeline_ollama import RAGPipeline as OllamaRAGPipeline
from src.auto_loader import DocumentAutoLoader

load_dotenv()

st.set_page_config(
    page_title="Mini RAG Assistant",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header { font-size: 2.5rem; font-weight: bold; color: #1f77b4; margin-bottom: 0.5rem; }
    .sub-header { font-size: 1.2rem; color: #666; margin-bottom: 2rem; }
    .confidence-high { color: #28a745; font-weight: bold; }
    .confidence-medium { color: #ffc107; font-weight: bold; }
    .confidence-low { color: #dc3545; font-weight: bold; }
    .source-box { 
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); 
        border-left: 5px solid #1f77b4; 
        padding: 1.25rem; 
        margin: 1rem 0; 
        border-radius: 8px; 
        color: #2c3e50;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .source-box:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.12);
    }
    .source-header {
        font-size: 1.1rem;
        font-weight: 600;
        color: #1f77b4;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .source-meta {
        display: inline-block;
        background-color: rgba(31, 119, 180, 0.1);
        color: #1f77b4;
        padding: 0.2rem 0.6rem;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 500;
    }
    .relevance-badge {
        display: inline-block;
        background-color: #d4edda;
        color: #155724;
        padding: 0.25rem 0.7rem;
        border-radius: 12px;
        font-size: 0.9rem;
        font-weight: 600;
        border: 1px solid #c3e6cb;
    }
    .source-content {
        margin-top: 0.75rem;
        padding: 0.75rem;
        background-color: white;
        border-radius: 6px;
        line-height: 1.7;
        color: #34495e;
        font-size: 0.95rem;
        border: 1px solid #e9ecef;
    }
    .provider-badge { background-color: #1f77b4; color: #fff; padding: 0.3rem 0.6rem; border-radius: 4px; font-size: 0.9rem; margin-left: 0.5rem; }
    .ollama-badge { background-color: #000; }
    .openai-badge { background-color: #10a37f; }
</style>
""", unsafe_allow_html=True)

if 'vector_store_manager' not in st.session_state:
    st.session_state.vector_store_manager = None
if 'rag_pipeline' not in st.session_state:
    st.session_state.rag_pipeline = None
if 'documents_loaded' not in st.session_state:
    st.session_state.documents_loaded = {}
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'auto_loaded' not in st.session_state:
    st.session_state.auto_loaded = {}
if 'current_provider' not in st.session_state:
    st.session_state.current_provider = None

def get_vector_store_path(provider: str) -> str:
    return f"vector_store_{provider}"

def initialize_components(provider: str, api_key: str = None, model_name: str = None):
    if st.session_state.current_provider != provider:
        st.session_state.auto_loaded[provider] = False
        st.session_state.chat_history = []
        
    if st.session_state.current_provider != provider or st.session_state.vector_store_manager is None:
        if provider == "openai":
            if not api_key:
                raise ValueError("OpenAI API key required")
            openai_model = model_name or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
            embedding_model = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
            st.session_state.vector_store_manager = OpenAIVectorStore(api_key, embedding_model=embedding_model)
            st.session_state.rag_pipeline = OpenAIRAGPipeline(api_key, model=openai_model)
        else:
            st.session_state.vector_store_manager = OllamaVectorStore()
            st.session_state.rag_pipeline = OllamaRAGPipeline(model=model_name or "qwen2.5:0.5b")
        st.session_state.current_provider = provider

def auto_load_documents(provider: str):
    if not st.session_state.auto_loaded.get(provider, False):
        vector_store_path = get_vector_store_path(provider)
        metadata_file = f"{vector_store_path}/processed_files.json"
        auto_loader = DocumentAutoLoader(docs_folder="docs", metadata_file=metadata_file)
        vector_store_exists = os.path.exists(f"{vector_store_path}/faiss_index")
        
        if vector_store_exists:
            try:
                st.session_state.vector_store_manager.load(f"{vector_store_path}/faiss_index")
                st.session_state.documents_loaded[provider] = True
                unprocessed = auto_loader.get_unprocessed_files()
                
                if unprocessed:
                    with st.spinner(f"Processing {len(unprocessed)} new documents..."):
                        processor = DocumentProcessor()
                        documents = processor.process_multiple_documents(unprocessed)
                        st.session_state.vector_store_manager.add_documents(documents)
                        st.session_state.vector_store_manager.save(f"{vector_store_path}/faiss_index")
                        auto_loader.mark_as_processed(unprocessed)
                        st.success(f"Added {len(unprocessed)} new documents")
                
                st.session_state.auto_loaded[provider] = True
            except:
                st.session_state.auto_loaded[provider] = False
        else:
            all_files = auto_loader.get_all_docs_files()
            if all_files:
                with st.spinner(f"Processing {len(all_files)} documents..."):
                    processor = DocumentProcessor()
                    documents = processor.process_multiple_documents(all_files)
                    if documents:
                        st.session_state.vector_store_manager.create_vector_store(documents)
                        st.session_state.vector_store_manager.save(f"{vector_store_path}/faiss_index")
                        st.session_state.documents_loaded[provider] = True
                        auto_loader.mark_as_processed(all_files)
                        st.success(f"Loaded {len(all_files)} documents")
            st.session_state.auto_loaded[provider] = True

def get_confidence_class(confidence: int) -> str:
    if confidence >= 70:
        return "confidence-high"
    elif confidence >= 50:
        return "confidence-medium"
    else:
        return "confidence-low"

def main():
    st.markdown('<div class="main-header">Mini RAG Assistant</div>', unsafe_allow_html=True)
    
    with st.sidebar:
        st.header("Configuration")
        default_provider = os.getenv("LLM_PROVIDER", "ollama").lower()
        provider = st.radio(
            "Select LLM Provider",
            options=["ollama", "openai"],
            index=0 if default_provider == "ollama" else 1
        )
        
        if provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY", "")
            if not api_key:
                api_key = st.text_input("OpenAI API Key", type="password")
                if not api_key:
                    st.error("Please enter your OpenAI API key")
                    st.stop()
            openai_model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
            embedding_model = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
            st.success("OpenAI configured")
            st.info(f"Model: {openai_model}")
            st.info(f"Embedding: {embedding_model}")
            try:
                initialize_components(provider, api_key=api_key, model_name=openai_model)
                auto_load_documents(provider)
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.stop()
            badge_class = "openai-badge"
            badge_text = "OpenAI"
        else:
            model_name = st.text_input(
                "Ollama Model",
                value=os.getenv("OLLAMA_MODEL", "qwen2.5:0.5b")
            )
            try:
                initialize_components(provider, model_name=model_name)
                auto_load_documents(provider)
                st.success("Ollama connected")
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.info("Make sure Ollama is running")
                st.stop()
            badge_class = "ollama-badge"
            badge_text = "Ollama"
        
        st.divider()
        st.header("Document Upload")
        uploaded_files = st.file_uploader(
            "Upload documents (PDF or TXT)",
            type=['pdf', 'txt'],
            accept_multiple_files=True
        )
        
        if uploaded_files:
            if st.button("Process Documents", type="primary"):
                with st.spinner("Processing..."):
                    os.makedirs("uploaded_docs", exist_ok=True)
                    file_paths = []
                    for uploaded_file in uploaded_files:
                        file_path = os.path.join("uploaded_docs", uploaded_file.name)
                        with open(file_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        file_paths.append(file_path)
                    
                    processor = DocumentProcessor()
                    documents = processor.process_multiple_documents(file_paths)
                    
                    vector_store_path = get_vector_store_path(provider)
                    if st.session_state.documents_loaded.get(provider, False):
                        st.session_state.vector_store_manager.add_documents(documents)
                    else:
                        st.session_state.vector_store_manager.create_vector_store(documents)
                        st.session_state.documents_loaded[provider] = True
                    
                    st.session_state.vector_store_manager.save(f"{vector_store_path}/faiss_index")
                    st.success(f"Processed {len(uploaded_files)} documents into {len(documents)} chunks")
        
        st.divider()
        st.header("Document Management")
        
        if st.button("Reprocess Docs Folder"):
            with st.spinner("Reprocessing all documents..."):
                try:
                    vector_store_path = get_vector_store_path(provider)
                    metadata_file = f"{vector_store_path}/processed_files.json"
                    
                    if os.path.exists(metadata_file):
                        os.remove(metadata_file)
                    
                    auto_loader = DocumentAutoLoader(docs_folder="docs", metadata_file=metadata_file)
                    all_files = auto_loader.get_all_docs_files()
                    
                    if all_files:
                        processor = DocumentProcessor()
                        documents = processor.process_multiple_documents(all_files)
                        
                        st.session_state.vector_store_manager.create_vector_store(documents)
                        st.session_state.vector_store_manager.save(f"{vector_store_path}/faiss_index")
                        st.session_state.documents_loaded[provider] = True
                        
                        auto_loader.mark_as_processed(all_files)
                        
                        st.success(f"Reprocessed {len(all_files)} documents into {len(documents)} chunks")
                        st.rerun()
                    else:
                        st.warning("No documents found in docs folder")
                except Exception as e:
                    st.error(f"Error reprocessing documents: {str(e)}")
        
        st.divider()
        num_results = st.slider("Sources to retrieve", 1, 10, 4)
        
        if st.session_state.vector_store_manager:
            stats = st.session_state.vector_store_manager.get_stats()
            if stats['status'] == 'initialized':
                st.metric("Status", "Ready")
                st.metric("Vectors", stats['num_vectors'])
    
    st.markdown(f'<div class="sub-header">Ask questions about your documents <span class="provider-badge {badge_class}">{badge_text}</span></div>', unsafe_allow_html=True)
    
    if not st.session_state.documents_loaded.get(provider, False):
        st.info("Upload documents or add files to the 'docs' folder")
    else:
        st.header("Ask Questions")
        query = st.text_input("Your question:", placeholder="e.g., What is the vacation policy?", key="query_input")
        col1, col2 = st.columns([1, 5])
        with col1:
            search_button = st.button("Ask", type="primary")
        with col2:
            if st.button("Clear"):
                st.session_state.chat_history = []
                st.rerun()
        
        if search_button and query:
            with st.spinner("Searching..."):
                try:
                    retrieved_docs = st.session_state.vector_store_manager.similarity_search(query, k=num_results)
                    result = st.session_state.rag_pipeline.query(query, retrieved_docs)
                    st.session_state.chat_history.append({"question": query, "result": result})
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        
        if st.session_state.chat_history:
            st.divider()
            for chat in reversed(st.session_state.chat_history):
                with st.container():
                    st.markdown(f"**Question:** {chat['question']}")
                    st.markdown("**Answer:**")
                    st.write(chat['result']['answer'])
                    
                    confidence = chat['result']['confidence']
                    confidence_class = get_confidence_class(confidence)
                    st.markdown(
                        f"**Confidence:** <span class='{confidence_class}'>{confidence}%</span>",
                        unsafe_allow_html=True
                    )
                    
                    with st.expander(f"📚 View {len(chat['result'].get('sources', []))} Sources", expanded=False):
                        sources = chat['result'].get('sources', [])
                        if sources:
                            for j, source in enumerate(sources, 1):
                                source_name = source.get('source', 'Unknown')
                                chunk_id = source.get('chunk_id', 0)
                                relevance = source.get('relevance_score', 0)
                                content = source.get('content', 'No content available')
                                
                                st.markdown(f"""
                                <div class="source-box">
                                    <div class="source-header">
                                        <span>📄</span>
                                        <span>Source {j}: {source_name}</span>
                                        <span class="source-meta">Chunk {chunk_id}</span>
                                    </div>
                                    <div style="margin: 0.5rem 0;">
                                        <span class="relevance-badge">✓ Relevance: {relevance:.1%}</span>
                                    </div>
                                    <div class="source-content">
                                        {content}
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
                        else:
                            st.warning("⚠️ No sources were retrieved for this answer.")
                    st.divider()
        else:
            st.info("Ask a question to get started!")

if __name__ == "__main__":
    main()
