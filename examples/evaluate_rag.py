import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from src.document_processor import DocumentProcessor
from src.vector_store import VectorStoreManager
from src.rag_pipeline import RAGPipeline
from src.rag_evaluator import RAGEvaluator

load_dotenv()


def example_basic_metrics():
    print("=" * 60)
    print("Example 1: Basic Metrics (No LLM required)")
    print("=" * 60)
    
    api_key = os.getenv("OPENAI_API_KEY")
    vector_store = VectorStoreManager(api_key)
    
    vector_store.load("vector_store_openai/faiss_index")
    
    question = "What is the vacation policy?"
    retrieved_docs = vector_store.similarity_search(question, k=5)
    
    evaluator = RAGEvaluator()
    
    relevant_doc_ids = ["docs/sample_policy.txt"]
    
    precision_3 = evaluator.precision_at_k(retrieved_docs, relevant_doc_ids, k=3)
    print(f"\nPrecision@3: {precision_3:.2%}")
    print(f"  → {precision_3*3:.0f} out of top 3 documents are relevant")
    
    # Calculate Recall@5
    recall_5 = evaluator.recall_at_k(retrieved_docs, relevant_doc_ids, k=5)
    print(f"\nRecall@5: {recall_5:.2%}")
    print(f"  → Retrieved {recall_5*len(relevant_doc_ids):.0f} out of {len(relevant_doc_ids)} relevant documents")
    
    # Calculate MRR
    mrr = evaluator.mean_reciprocal_rank(retrieved_docs, relevant_doc_ids)
    print(f"\nMean Reciprocal Rank: {mrr:.3f}")
    if mrr > 0:
        print(f"  → First relevant document at position {int(1/mrr)}")
    
    print("\n" + "=" * 60)


def example_grounding_accuracy():
    print("\n" + "=" * 60)
    print("Example 2: Grounding Accuracy (LLM-based)")
    print("=" * 60)
    
    # Initialize components
    api_key = os.getenv("OPENAI_API_KEY")
    vector_store = VectorStoreManager(api_key)
    rag_pipeline = RAGPipeline(api_key)
    
    # Load vector store
    vector_store.load("vector_store_openai/faiss_index")
    
    question = "What is the vacation policy?"
    retrieved_docs = vector_store.similarity_search(question, k=3)
    
    result = rag_pipeline.query(question, retrieved_docs)
    answer = result['answer']
    
    print(f"\nQuestion: {question}")
    print(f"\nAnswer: {answer}")
    
    import openai
    llm_client = openai.OpenAI(api_key=api_key)
    evaluator = RAGEvaluator(llm_client=llm_client)
    
    grounding = evaluator.grounding_accuracy(answer, retrieved_docs, use_llm=True)
    print(f"\nGrounding Score: {grounding['grounding_score']:.2%}")
    print(f"Method: {grounding['method']}")
    
    if grounding['grounding_score'] >= 0.9:
        print("✓ Answer is well-grounded in the documents")
    elif grounding['grounding_score'] >= 0.7:
        print("⚠ Answer is mostly grounded but has some unsupported claims")
    else:
        print("✗ Answer may contain hallucinations or unsupported information")
    
    print("\n" + "=" * 60)


def example_answer_relevancy():
    print("\n" + "=" * 60)
    print("Example 3: Answer Relevancy")
    print("=" * 60)
    
    # Initialize components
    api_key = os.getenv("OPENAI_API_KEY")
    vector_store = VectorStoreManager(api_key)
    rag_pipeline = RAGPipeline(api_key)
    
    # Load vector store
    vector_store.load("vector_store_openai/faiss_index")
    
    question = "How many vacation days do employees get?"
    retrieved_docs = vector_store.similarity_search(question, k=3)
    
    result = rag_pipeline.query(question, retrieved_docs)
    answer = result['answer']
    
    print(f"\nQuestion: {question}")
    print(f"\nAnswer: {answer}")
    
    import openai
    llm_client = openai.OpenAI(api_key=api_key)
    evaluator = RAGEvaluator(llm_client=llm_client)
    
    relevancy = evaluator.answer_relevancy(question, answer, use_llm=True)
    print(f"\nRelevancy Score: {relevancy['relevancy_score']:.2%}")
    print(f"Method: {relevancy['method']}")
    
    if relevancy['relevancy_score'] >= 0.9:
        print("✓ Answer directly addresses the question")
    elif relevancy['relevancy_score'] >= 0.7:
        print("⚠ Answer partially addresses the question")
    else:
        print("✗ Answer may be off-topic or incomplete")
    
    print("\n" + "=" * 60)


def example_full_evaluation():
    print("\n" + "=" * 60)
    print("Example 4: Full Evaluation Suite")
    print("=" * 60)
    
    # Initialize components
    api_key = os.getenv("OPENAI_API_KEY")
    vector_store = VectorStoreManager(api_key)
    rag_pipeline = RAGPipeline(api_key)
    
    # Load vector store
    vector_store.load("vector_store_openai/faiss_index")
    
    question = "What is the vacation policy?"
    retrieved_docs = vector_store.similarity_search(question, k=5)
    
    result = rag_pipeline.query(question, retrieved_docs)
    answer = result['answer']
    
    print(f"\nQuestion: {question}")
    print(f"\nAnswer: {answer[:200]}...")
    
    import openai
    llm_client = openai.OpenAI(api_key=api_key)
    evaluator = RAGEvaluator(llm_client=llm_client)
    
    relevant_doc_ids = ["docs/sample_policy.txt"]
    
    eval_results = evaluator.evaluate_full(
        question=question,
        answer=answer,
        retrieved_docs=retrieved_docs,
        relevant_doc_ids=relevant_doc_ids,
        k=3
    )
    
    print("\n" + "-" * 60)
    print("EVALUATION RESULTS")
    print("-" * 60)
    
    print(f"\n📊 Retrieval Metrics:")
    print(f"  Precision@3: {eval_results.get('precision_at_k', 0):.2%}")
    print(f"  Recall@3: {eval_results.get('recall_at_k', 0):.2%}")
    print(f"  MRR: {eval_results.get('mrr', 0):.3f}")
    print(f"  Avg Retrieval Score: {eval_results['avg_retrieval_score']:.2%}")
    
    print(f"\n🎯 Generation Metrics:")
    print(f"  Grounding Score: {eval_results['grounding']['grounding_score']:.2%}")
    print(f"  Relevancy Score: {eval_results['relevancy']['relevancy_score']:.2%}")
    
    print(f"\n📈 Overall Assessment:")
    grounding = eval_results['grounding']['grounding_score']
    relevancy = eval_results['relevancy']['relevancy_score']
    
    if grounding >= 0.8 and relevancy >= 0.8:
        print("  ✓ Excellent - Answer is accurate and relevant")
    elif grounding >= 0.6 and relevancy >= 0.6:
        print("  ⚠ Good - Minor improvements possible")
    else:
        print("  ✗ Needs improvement - Check retrieval or generation")
    
    print("\n" + "=" * 60)


def example_batch_evaluation():
    print("\n" + "=" * 60)
    print("Example 5: Batch Evaluation")
    print("=" * 60)
    
    # Initialize components
    api_key = os.getenv("OPENAI_API_KEY")
    vector_store = VectorStoreManager(api_key)
    rag_pipeline = RAGPipeline(api_key)
    
    # Load vector store
    vector_store.load("vector_store_openai/faiss_index")
    
    import openai
    llm_client = openai.OpenAI(api_key=api_key)
    evaluator = RAGEvaluator(llm_client=llm_client)
    
    test_queries = [
        "What is the vacation policy?",
        "How many sick days are allowed?",
        "What are the working hours?"
    ]
    
    results = []
    
    for question in test_queries:
        retrieved_docs = vector_store.similarity_search(question, k=3)
        result = rag_pipeline.query(question, retrieved_docs)
        
        eval_result = evaluator.evaluate_full(
            question=question,
            answer=result['answer'],
            retrieved_docs=retrieved_docs,
            k=3
        )
        
        results.append({
            'question': question,
            'grounding': eval_result['grounding']['grounding_score'],
            'relevancy': eval_result['relevancy']['relevancy_score']
        })
    
    print("\n" + "-" * 60)
    print("BATCH RESULTS")
    print("-" * 60)
    
    for i, r in enumerate(results, 1):
        print(f"\n{i}. {r['question']}")
        print(f"   Grounding: {r['grounding']:.2%} | Relevancy: {r['relevancy']:.2%}")
    
    # Calculate averages
    avg_grounding = sum(r['grounding'] for r in results) / len(results)
    avg_relevancy = sum(r['relevancy'] for r in results) / len(results)
    
    print(f"\n" + "-" * 60)
    print(f"Average Grounding: {avg_grounding:.2%}")
    print(f"Average Relevancy: {avg_relevancy:.2%}")
    print("=" * 60)


if __name__ == "__main__":
    print("\n RAG Evaluation Examples\n")
    
    try:
        example_basic_metrics()
        example_grounding_accuracy()
        example_answer_relevancy()
        example_full_evaluation()
        example_batch_evaluation()
        
        print("\n✅ All examples completed!")
        print("\nNext steps:")
        print("1. Create your own test set with ground truth labels")
        print("2. Run evaluations on your specific use case")
        print("3. Track metrics over time to measure improvements")
        
    except Exception as e:
        print(f"\n Error: {e}")
        print("\nMake sure:")
        print("1. OPENAI_API_KEY is set in .env")
        print("2. Vector store exists at vector_store_openai/faiss_index")
        print("3. Documents are loaded in the vector store")
