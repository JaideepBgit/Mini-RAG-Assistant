# 5-Slide Deck Structure Guide

## SLIDE 1: PROBLEM & OBJECTIVES
**Layout:** Title + 2 columns

### Left Column: Problem
**Title:** The Challenge
- 🔍 Manual document search is slow
- 📚 Information scattered across files
- ❌ No centralized Q&A system
- 🔒 Need both cloud & local options

### Right Column: Solution
**Title:** Our Objectives
- ✅ Build intelligent RAG system
- ✅ Support OpenAI + Ollama
- ✅ Semantic search with FAISS
- ✅ Confidence scores & citations
- ✅ Multi-turn conversations
- ✅ User-friendly web interface

**Visual:** Use icons for each bullet point

---

## SLIDE 2: ARCHITECTURE
**Layout:** Title + Large Diagram

### Architecture Diagram (Center)
```
┌─────────────────────────────────────────────────┐
│         USER INTERFACE (Streamlit)              │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│      DOCUMENT INGESTION                         │
│  • Auto-loader (docs folder)                    │
│  • Manual upload (PDF/TXT)                      │
│  • PyPDF2 + Text Splitter                       │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│      EMBEDDING & VECTOR STORAGE                 │
│  OpenAI: text-embedding-3-small (1536 dims)     │
│  Ollama: all-MiniLM-L6-v2 (384 dims)           │
│  FAISS Vector Database                          │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│      RETRIEVAL (Top-K Similarity Search)        │
│  Cosine similarity → Relevance scores           │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│      GENERATION (LLM)                           │
│  OpenAI: GPT-4o-mini                            │
│  Ollama: Qwen2.5:0.5b                          │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│      RESPONSE                                   │
│  Answer + Confidence (0-100%) + Sources         │
└─────────────────────────────────────────────────┘
```

**Key Points (bottom):**
- Chunk Size: 1000 chars, 200 overlap
- Retrieval: Top-4 sources by default
- Dual vector stores for each provider

---

## SLIDE 3: IMPLEMENTATION HIGHLIGHTS
**Layout:** Title + 2 columns with screenshots

### Left Column: Key Decisions

**1. Dual Provider Architecture**
```python
# Separate vector stores
if provider == "openai":
    embeddings = OpenAIEmbeddings()
else:
    embeddings = OllamaEmbeddings()
```
Why: Privacy vs Performance trade-off

**2. Chunking Strategy**
```python
RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
```
Why: Balance context & precision

**3. Confidence Scoring**
- LLM self-evaluation (0-100%)
- 90-100%: High confidence
- 70-89%: Good confidence
- 50-69%: Moderate
- <50%: Low confidence

### Right Column: Screenshots
- [Screenshot 1: Main interface]
- [Screenshot 2: Answer with confidence]
- [Screenshot 3: Source attribution]

---

## SLIDE 4: CHALLENGES & LEARNINGS
**Layout:** Title + 2 columns

### Left Column: Key Challenges

**1. Embedding Dimension Mismatch**
- Problem: OpenAI (1536) ≠ Ollama (384)
- Solution: Separate vector stores
- Learning: Vector stores not interchangeable

**2. Multi-Turn Context**
- Problem: "How do I request it?" failed
- Solution: Enhanced query + prompt engineering
- Learning: Fix both retrieval AND generation

**3. Ollama Connection**
- Problem: Local server must be running
- Solution: Graceful error handling
- Learning: UX matters for local deployment

**4. Context Window Limits**
- Problem: Too many chunks exceed tokens
- Solution: Top-K retrieval (default: 4)
- Learning: Quality over quantity

### Right Column: Key Learnings

**What Worked Well:**
✅ Auto-loading reduces friction
✅ Confidence scores build trust
✅ Source attribution enables verification
✅ Dual providers increase adoption

**Trade-offs Made:**
⚖️ Simplicity vs Features → MVP first
⚖️ Accuracy vs Speed → Balanced settings
⚖️ Privacy vs Performance → User choice

**Future Improvements:**
🔮 DOCX/HTML support
🔮 Extended conversation history
🔮 Document management UI
🔮 RAGAS evaluation metrics

---

## SLIDE 5: DEMO & NEXT STEPS
**Layout:** Title + 3 sections

### Section 1: Demo Highlights (Top)
**[Large screenshot of app in action]**

**Key Features Demonstrated:**
- 📄 Auto-loads 4 sample documents
- 💬 Natural language Q&A
- 🎯 Confidence scores (0-100%)
- 📚 Source attribution with relevance
- 🔄 Provider switching (OpenAI ↔ Ollama)
- 💡 Multi-turn conversations
- 🖍️ Text highlighting in sources

### Section 2: Sample Queries (Middle)

**Single-turn:**
- "What is the vacation leave policy?"
- "How many sick days do employees get?"

**Multi-turn:**
1. "What is the vacation policy?"
2. "How do I request it?" ← understands "it"
3. "What if I need to cancel?" ← maintains context

### Section 3: Next Steps (Bottom)

**Short-term (1-2 weeks):**
- Multi-format support (DOCX, HTML)
- Extended conversation history
- Evaluation framework (RAGAS)

**Medium-term (1-2 months):**
- Document management UI
- Performance optimization (caching)
- Enhanced security & access control

**Business Value:**
💰 70-80% reduction in search time
🎯 Improved answer consistency
🔒 Data privacy with local deployment

**Links:**
- 🔗 GitHub: [your-repo-link]
- 🎥 Demo Video: [video-link]
- 🌐 Live Demo: https://mini-rag-assistant-cxwtk46n9wrmtmwexhaxj7.streamlit.app

---

## DESIGN TIPS

### Color Scheme Suggestions:
- Primary: Blue (#2E86AB) - trust, technology
- Secondary: Green (#06A77D) - success, accuracy
- Accent: Orange (#F18F01) - highlights, warnings
- Background: White/Light gray
- Text: Dark gray (#2C3E50)

### Fonts:
- Headings: Calibri Bold or Arial Bold
- Body: Calibri or Arial (11-12pt)
- Code: Consolas or Courier New (10pt)

### Icons:
Use simple, consistent icons from:
- Flaticon.com
- Icons8.com
- Or PowerPoint built-in icons

### Layout:
- Keep 30% white space
- Use consistent margins
- Align elements properly
- Maximum 6 bullets per slide
- Use visuals over text when possible

---

## SCREENSHOTS TO TAKE

### For Slide 3:
1. **Main Interface** - Full app view with sidebar
2. **Answer Display** - Question + answer + confidence score
3. **Source Attribution** - Expanded sources with relevance scores

### For Slide 5:
1. **Multi-turn Conversation** - Show 3 Q&A exchanges
2. **Text Highlighting** - Source with highlighted text
3. **Provider Toggle** - Sidebar showing OpenAI/Ollama switch

### How to Take Good Screenshots:
- Use full browser window (not just partial)
- Clear any personal information
- Use sample data that looks professional
- Crop to remove unnecessary browser chrome
- Ensure text is readable (high resolution)
- Add borders or shadows for polish

---

## POWERPOINT CREATION STEPS

1. **Open PowerPoint** - Start with blank presentation
2. **Set Slide Size** - 16:9 widescreen
3. **Choose Theme** - Simple, professional (avoid busy templates)
4. **Create Title Slide** - Project name + your name
5. **Create 5 Content Slides** - Follow structure above
6. **Add Visuals** - Screenshots, diagrams, icons
7. **Add Code Snippets** - Use text boxes with Consolas font
8. **Review** - Check spelling, alignment, consistency
9. **Export as PDF** - File → Save As → PDF

---

## ALTERNATIVE: Google Slides

If you don't have PowerPoint:
1. Go to slides.google.com
2. Create new presentation
3. Follow same structure
4. Download as PDF when done

---

## QUICK CHECKLIST

Before finalizing slides:
- [ ] All 5 slides created
- [ ] Architecture diagram included
- [ ] Screenshots added
- [ ] Code snippets formatted
- [ ] No typos or grammar errors
- [ ] Consistent fonts and colors
- [ ] Slide numbers added
- [ ] Your name on title slide
- [ ] Links work (if clickable PDF)
- [ ] Exported as PDF
- [ ] File size reasonable (<10MB)

---

## TIME ESTIMATE

- Slide 1: 15 minutes
- Slide 2 (with diagram): 30 minutes
- Slide 3 (with screenshots): 20 minutes
- Slide 4: 15 minutes
- Slide 5 (with screenshots): 20 minutes
- Review and polish: 20 minutes

**Total: ~2 hours**

Good luck! Your content is excellent - now just make it visual! 🎨
