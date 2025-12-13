# Simple Architecture Diagram for Slide 2

## OPTION 1: Vertical Flow (Recommended for PowerPoint)

```
┌─────────────────────────────────────────┐
│         USER INTERFACE                  │
│         (Streamlit Web App)             │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│      DOCUMENT INGESTION                 │
│  • Auto-loader (docs folder)            │
│  • Manual upload (PDF/TXT)              │
│  • PyPDF2 + Text Splitter               │
│  • Chunks: 1000 chars, 200 overlap      │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│      EMBEDDING & VECTOR STORAGE         │
│  OpenAI: text-embedding-3-small         │
│  Ollama: all-MiniLM-L6-v2              │
│  FAISS Vector Database                  │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│      RETRIEVAL (Semantic Search)        │
│  • Cosine similarity                    │
│  • Top-K results (default: 4)           │
│  • Relevance scoring                    │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│      GENERATION (LLM)                   │
│  OpenAI: GPT-4o-mini                    │
│  Ollama: Qwen2.5:0.5b                  │
│  LangChain orchestration                │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│      RESPONSE ENRICHMENT                │
│  • Answer generation                    │
│  • Confidence scoring (0-100%)          │
│  • Source attribution                   │
│  • Text highlighting                    │
└─────────────────────────────────────────┘
```

---

## OPTION 2: Horizontal Flow (Alternative)

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│   User   │───▶│ Document │───▶│ Embedding│───▶│ Retrieval│───▶│    LLM   │───▶│ Response │
│   Query  │    │ Ingestion│    │ & Vector │    │  Search  │    │Generation│    │  Display │
└──────────┘    └──────────┘    └──────────┘    └──────────┘    └──────────┘    └──────────┘
                                                                                         │
                                                                                         ▼
                                                                                  ┌──────────┐
                                                                                  │Confidence│
                                                                                  │ Sources  │
                                                                                  │Highlights│
                                                                                  └──────────┘
```

---

## OPTION 3: Component-Based (Best for Understanding)

```
┌─────────────────────────────────────────────────────────────────────┐
│                         STREAMLIT UI LAYER                          │
│  • Question input  • Provider selection  • Multi-turn toggle        │
└─────────────────────────────────────────────────────────────────────┘
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        │                           │                           │
        ▼                           ▼                           ▼
┌──────────────┐          ┌──────────────┐          ┌──────────────┐
│  DOCUMENT    │          │   VECTOR     │          │     RAG      │
│  PROCESSOR   │          │   STORE      │          │   PIPELINE   │
│              │          │              │          │              │
│ • PyPDF2     │──────▶   │ • FAISS      │──────▶   │ • LangChain  │
│ • Chunking   │          │ • Embeddings │          │ • LLM        │
│ • Metadata   │          │ • Search     │          │ • Prompts    │
└──────────────┘          └──────────────┘          └──────────────┘
                                                              │
                                                              ▼
                                                    ┌──────────────┐
                                                    │   RESPONSE   │
                                                    │              │
                                                    │ • Answer     │
                                                    │ • Confidence │
                                                    │ • Sources    │
                                                    │ • Highlights │
                                                    └──────────────┘
```

---

## POWERPOINT CREATION GUIDE

### Step 1: Create Boxes
1. Insert → Shapes → Rectangle
2. Create 6 boxes (one for each component)
3. Size: Width 8", Height 1.5"
4. Arrange vertically with space between

### Step 2: Add Text
For each box, add:
- **Title** (Bold, 18pt): Component name
- **Details** (Regular, 12pt): Key features

**Box 1: User Interface**
- Title: "User Interface (Streamlit)"
- Details: "Question input • Provider selection • Multi-turn toggle"

**Box 2: Document Ingestion**
- Title: "Document Ingestion"
- Details: "Auto-loader • PDF/TXT parsing • Chunking (1000 chars, 200 overlap)"

**Box 3: Embedding & Vector Storage**
- Title: "Embedding & Vector Storage"
- Details: "OpenAI: text-embedding-3-small • Ollama: all-MiniLM-L6-v2 • FAISS"

**Box 4: Retrieval**
- Title: "Retrieval (Semantic Search)"
- Details: "Cosine similarity • Top-K results • Relevance scoring"

**Box 5: Generation**
- Title: "Generation (LLM)"
- Details: "OpenAI: GPT-4o-mini • Ollama: Qwen2.5:0.5b • LangChain"

**Box 6: Response**
- Title: "Response Enrichment"
- Details: "Answer • Confidence (0-100%) • Sources • Highlighting"

### Step 3: Add Arrows
1. Insert → Shapes → Arrow
2. Connect boxes vertically
3. Make arrows thick (3pt)
4. Color: Dark gray or blue

### Step 4: Color Scheme
**Option A: Blue Gradient**
- Box 1: Light blue (#E3F2FD)
- Box 2: Blue (#BBDEFB)
- Box 3: Medium blue (#90CAF9)
- Box 4: Blue (#64B5F6)
- Box 5: Dark blue (#42A5F5)
- Box 6: Darker blue (#2196F3)

**Option B: Professional Gray**
- All boxes: Light gray (#F5F5F5)
- Borders: Dark gray (#424242)
- Text: Black (#000000)
- Arrows: Blue (#2196F3)

**Option C: Colorful**
- Box 1: Light purple (#E1BEE7)
- Box 2: Light blue (#B3E5FC)
- Box 3: Light green (#C8E6C9)
- Box 4: Light yellow (#FFF9C4)
- Box 5: Light orange (#FFE0B2)
- Box 6: Light red (#FFCDD2)

### Step 5: Polish
- Align all boxes (select all → Align → Center)
- Make arrows same length
- Add drop shadow (optional): Format → Shape Effects → Shadow
- Group all elements: Select all → Right-click → Group

---

## GOOGLE SLIDES VERSION

### Quick Steps:
1. Go to slides.google.com
2. Create new presentation
3. Insert → Shape → Rectangle
4. Follow same steps as PowerPoint
5. Use "Align" tools to center
6. Download as PDF when done

---

## DRAW.IO VERSION

### Quick Steps:
1. Go to draw.io (free online tool)
2. Choose "Blank Diagram"
3. Drag "Rectangle" shapes from left panel
4. Double-click to add text
5. Use "Connector" tool for arrows
6. File → Export as → PNG
7. Insert PNG into your slides

---

## CANVA VERSION (Easiest)

### Quick Steps:
1. Go to canva.com (free account)
2. Create "Presentation" (16:9)
3. Search "flowchart" in templates
4. Customize with your text
5. Download as PDF
6. Extract the architecture slide

---

## MINIMAL TEXT VERSION (If Short on Time)

If you're really pressed for time, just use this text on your slide:

**ARCHITECTURE FLOW:**

1. **User Interface** → Streamlit web app
2. **Document Ingestion** → PDF/TXT parsing + chunking
3. **Embedding** → OpenAI or Ollama embeddings
4. **Vector Storage** → FAISS database
5. **Retrieval** → Semantic search (Top-K)
6. **Generation** → LLM (GPT-4o-mini or Qwen2.5)
7. **Response** → Answer + Confidence + Sources + Highlights

**Key Components:**
- Dual provider support (OpenAI + Ollama)
- Chunk size: 1000 chars, 200 overlap
- Retrieval: Top-4 sources by default
- Confidence scoring: 0-100%

---

## HAND-DRAWN OPTION

If you're artistic or short on time:

1. Draw boxes and arrows on paper
2. Take photo with phone
3. Use phone editor to increase contrast
4. Insert photo into slide
5. Add text labels in PowerPoint

This can actually look professional and shows creativity!

---

## TIME ESTIMATES

- **PowerPoint shapes:** 20-30 minutes
- **Draw.io:** 15-20 minutes
- **Canva template:** 10-15 minutes
- **Hand-drawn:** 10 minutes
- **Text only:** 5 minutes

---

## EXAMPLE SLIDE LAYOUT

```
┌────────────────────────────────────────────────────────────┐
│                                                            │
│  SLIDE 2: SOLUTION ARCHITECTURE AND DESIGN FLOW            │
│                                                            │
│  ┌──────────────────────────────────────────────────┐     │
│  │                                                  │     │
│  │         [ARCHITECTURE DIAGRAM HERE]              │     │
│  │                                                  │     │
│  │         (Use one of the options above)           │     │
│  │                                                  │     │
│  └──────────────────────────────────────────────────┘     │
│                                                            │
│  KEY TECHNICAL COMPONENTS:                                 │
│  • Framework: Streamlit (web UI)                          │
│  • Orchestration: LangChain                               │
│  • Vector DB: FAISS                                       │
│  • Embeddings: OpenAI / Ollama                            │
│  • LLM: GPT-4o-mini / Qwen2.5:0.5b                       │
│                                                            │
│  DATA FLOW:                                               │
│  Document → Chunking → Embedding → Vector Store →         │
│  Query → Search → Context → LLM → Answer + Sources        │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

---

## TIPS FOR SUCCESS

### Visual Design:
- **Keep it simple** - Don't overcomplicate
- **Use consistent colors** - Pick 2-3 colors max
- **Make text readable** - Minimum 12pt font
- **Align everything** - Use alignment tools
- **Add white space** - Don't cram too much

### Content:
- **Show data flow** - Arrows should be clear
- **Label everything** - Each box should be clear
- **Highlight key tech** - Mention FAISS, LangChain, etc.
- **Keep it high-level** - Don't get too detailed

### Common Mistakes:
- ❌ Too many boxes (keep it 5-7 max)
- ❌ Tiny text (make it readable)
- ❌ Unclear arrows (show direction clearly)
- ❌ Too much detail (keep it high-level)
- ❌ Inconsistent styling (use same colors/fonts)

---

## FINAL CHECKLIST

- [ ] Architecture diagram created
- [ ] All components labeled
- [ ] Arrows show data flow
- [ ] Colors are consistent
- [ ] Text is readable
- [ ] Looks professional
- [ ] Fits on one slide
- [ ] Matches your system

---

## YOU'RE READY!

Pick the option that works best for you:
- **Most professional:** PowerPoint shapes (30 min)
- **Fastest:** Canva template (15 min)
- **Most flexible:** Draw.io (20 min)
- **Emergency:** Text only (5 min)

All options are acceptable - choose based on your time and skills!

Good luck! 🎨
