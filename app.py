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
    .main-header { 
        font-size: 2.5rem; 
        font-weight: bold; 
        color: #1f77b4; 
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .sub-header { 
        font-size: 1.2rem; 
        color: #666; 
        margin-bottom: 2rem; 
    }
    .confidence-high { 
        color: #28a745; 
        font-weight: bold; 
        font-size: 1.1rem;
    }
    .confidence-medium { 
        color: #ffc107; 
        font-weight: bold; 
        font-size: 1.1rem;
    }
    .confidence-low { 
        color: #dc3545; 
        font-weight: bold; 
        font-size: 1.1rem;
    }
    .source-box { 
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%); 
        border-left: 6px solid #1f77b4; 
        padding: 1.5rem; 
        margin: 1.2rem 0; 
        border-radius: 12px; 
        color: #2c3e50;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        border: 1px solid #e3e8ef;
    }
    .source-box:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 20px rgba(31, 119, 180, 0.2);
        border-left-color: #0d5aa7;
    }
    .source-header {
        font-size: 1.15rem;
        font-weight: 700;
        color: #1f77b4;
        margin-bottom: 0.8rem;
        display: flex;
        align-items: center;
        gap: 0.6rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e9ecef;
    }
    .source-icon {
        font-size: 1.3rem;
        filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));
    }
    .source-meta {
        display: inline-block;
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        color: #0d47a1;
        padding: 0.3rem 0.8rem;
        border-radius: 16px;
        font-size: 0.85rem;
        font-weight: 600;
        box-shadow: 0 2px 4px rgba(0,0,0,0.08);
        margin-left: auto;
    }
    .relevance-badge {
        display: inline-block;
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        color: #155724;
        padding: 0.35rem 0.9rem;
        border-radius: 16px;
        font-size: 0.95rem;
        font-weight: 700;
        border: 2px solid #b1dfbb;
        box-shadow: 0 2px 6px rgba(21, 87, 36, 0.15);
    }
    .source-content {
        margin-top: 1rem;
        padding: 1rem;
        background-color: #ffffff;
        border-radius: 8px;
        line-height: 1.7;
        color: #2c3e50;
        font-size: 0.95rem;
        border: 1px solid #dee2e6;
        box-shadow: inset 0 1px 3px rgba(0,0,0,0.05);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        white-space: normal;
        word-wrap: break-word;
        text-align: justify;
    }
    .source-content mark,
    .source-content span {
        display: inline;
        white-space: normal;
    }
    .provider-badge { 
        background-color: #1f77b4; 
        color: #fff; 
        padding: 0.4rem 0.8rem; 
        border-radius: 6px; 
        font-size: 0.9rem; 
        margin-left: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        font-weight: 600;
    }
    .ollama-badge { 
        background: linear-gradient(135deg, #000000 0%, #2c2c2c 100%);
    }
    .openai-badge { 
        background: linear-gradient(135deg, #10a37f 0%, #0d8a6a 100%);
    }
    .answer-box {
        background: #ffffff;
        padding: 1rem;
        border-radius: 5px;
        border-left: 3px solid #1f77b4;
        margin: 1rem 0;
        white-space: pre-wrap;
        word-wrap: break-word;
        line-height: 1.6;
    }
    .question-box {
        background: #ffffff;
        padding: 1rem;
        border-radius: 5px;
        border-left: 3px solid #ffc107;
        margin: 0.5rem 0;
        font-weight: 500;
    }
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
        st.header("Search Settings")
        num_results = st.slider("Sources to retrieve", 1, 10, 4)
        enable_highlighting = st.checkbox("Highlight relevant text", value=True, 
                                         help="Highlights parts of sources that were used to generate the answer")
        enable_conversation_context = st.checkbox("Multi-turn conversation", value=False,
                                                  help="Include previous Q&A in context for follow-up questions")
        
        if enable_conversation_context:
            st.success("✓ Multi-turn mode: ON - Follow-up questions will use conversation history")
        else:
            st.info("Multi-turn mode: OFF - Each question is independent")
        
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
                    conversation_history = []
                    enhanced_query = query
                    
                    if enable_conversation_context and st.session_state.chat_history:
                        for chat in st.session_state.chat_history[-3:]:
                            conversation_history.append({
                                "question": chat["question"],
                                "answer": chat["result"]["answer"]
                            })
                        
                        last_question = st.session_state.chat_history[-1]["question"]
                        enhanced_query = f"{last_question} {query}"
                        
                        with st.expander("Debug: Enhanced Query", expanded=False):
                            st.write(f"**Original:** {query}")
                            st.write(f"**Enhanced:** {enhanced_query}")
                            st.write(f"**History items:** {len(conversation_history)}")
                    
                    retrieved_docs = st.session_state.vector_store_manager.similarity_search(enhanced_query, k=num_results)
                    
                    result = st.session_state.rag_pipeline.query(
                        query, 
                        retrieved_docs, 
                        enable_highlighting=enable_highlighting,
                        conversation_history=conversation_history
                    )
                    st.session_state.chat_history.append({"question": query, "result": result})
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        
        if st.session_state.chat_history:
            st.divider()
            for chat in reversed(st.session_state.chat_history):
                with st.container():
                    st.write(f"**Question:** {chat['question']}")
                    st.write(f"**Answer:** {chat['result']['answer']}")
                    
                    confidence = chat['result']['confidence']
                    confidence_class = get_confidence_class(confidence)
                    st.markdown(
                        f"<strong>Confidence Score:</strong> <span class='{confidence_class}'>{confidence}%</span>",
                        unsafe_allow_html=True
                    )
                    
                    with st.expander(f"View {len(chat['result'].get('sources', []))} Source Documents", expanded=False):
                        sources = chat['result'].get('sources', [])
                        
                        highlight_legend = chat['result'].get('highlight_legend', '')
                        if highlight_legend:
                            st.markdown(highlight_legend, unsafe_allow_html=True)
                        
                        if sources:
                            for j, source in enumerate(sources, 1):
                                source_name = source.get('source', 'Unknown')
                                chunk_id = source.get('chunk_id', 0)
                                relevance = source.get('relevance_score', 0)
                                content = source.get('content', 'No content available')
                                
                                relevance_color = "#d4edda" if relevance >= 0.7 else "#fff3cd" if relevance >= 0.5 else "#f8d7da"
                                relevance_text_color = "#155724" if relevance >= 0.7 else "#856404" if relevance >= 0.5 else "#721c24"
                                
                                st.markdown(f"""
                                <div class="source-box">
                                    <div class="source-header">
                                        <span><strong>Source {j}:</strong> {source_name}</span>
                                        <span class="source-meta">Chunk #{chunk_id}</span>
                                    </div>
                                    <div style="margin: 0.8rem 0;">
                                        <span class="relevance-badge" style="background: {relevance_color}; color: {relevance_text_color};">
                                            Relevance Score: {relevance:.1%}
                                        </span>
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                st.markdown(f'<div class="source-content">{content}</div>', unsafe_allow_html=True)
                        else:
                            st.warning("No sources were retrieved for this answer.")
                    st.divider()
        else:
            st.info("Ask a question to get started!")

if __name__ == "__main__":
    main()
