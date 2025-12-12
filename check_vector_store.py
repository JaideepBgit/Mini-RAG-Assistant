import pickle
import os

vector_stores = ['vector_store_openai', 'vector_store_ollama']

for store_name in vector_stores:
    index_path = os.path.join('vector_store', store_name, 'faiss_index')
    
    if not os.path.exists(index_path):
        print(f"\n{store_name}: Not found")
        continue
        
    print(f"\n{'='*60}")
    print(f"Checking: {store_name}")
    print('='*60)
    
    docstore_path = os.path.join(index_path, 'index.pkl')
    
    if os.path.exists(docstore_path):
        try:
            with open(docstore_path, 'rb') as f:
                data = pickle.load(f)
                
            if isinstance(data, dict) and 'docstore' in data:
                docstore = data['docstore']
                docs = docstore._dict if hasattr(docstore, '_dict') else {}
                
                print(f"Found {len(docs)} documents in docstore")
                
                html_indicators = ['<mark', '<span', 'style=', 'background-color:', 'padding:', 'border-radius:']
                
                for i, (doc_id, doc) in enumerate(list(docs.items())[:3]):
                    content = doc.page_content if hasattr(doc, 'page_content') else str(doc)
                    found_html = [indicator for indicator in html_indicators if indicator in content]
                    
                    print(f"\n--- Document {i+1} (ID: {doc_id}) ---")
                    if found_html:
                        print(f"⚠️  WARNING: Found HTML tags: {found_html}")
                        print(f"First 400 chars:\n{content[:400]}")
                    else:
                        print("✓ No HTML detected")
                        print(f"First 200 chars:\n{content[:200]}")
                        
        except Exception as e:
            print(f"Error reading docstore: {e}")
    else:
        print("index.pkl not found")
