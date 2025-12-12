from PyPDF2 import PdfReader
import os

docs_folder = "docs"
pdf_files = [f for f in os.listdir(docs_folder) if f.endswith('.pdf')]

print(f"Found {len(pdf_files)} PDF files in docs folder\n")

for pdf_file in pdf_files:
    pdf_path = os.path.join(docs_folder, pdf_file)
    print(f"\n{'='*60}")
    print(f"FILE: {pdf_file}")
    print('='*60)
    
    try:
        reader = PdfReader(pdf_path)
        first_page_text = reader.pages[0].extract_text()
        
        html_indicators = ['<mark', '<span', 'style=', 'background-color:', 'padding:', 'border-radius:']
        found_html = [indicator for indicator in html_indicators if indicator in first_page_text]
        
        if found_html:
            print(f"⚠️  WARNING: Found HTML-like content: {found_html}")
            print("\nFirst 800 characters:")
            print(first_page_text[:800])
        else:
            print("✓ No HTML tags detected")
            print("\nFirst 300 characters:")
            print(first_page_text[:300])
            
    except Exception as e:
        print(f"Error reading PDF: {e}")
