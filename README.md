# Connecting the Dots Challenge

## Rethink Reading. Rediscover Knowledge.

Welcome to our submission for the "Connecting the Dots" Challenge - reimagining PDFs as intelligent, interactive experiences that understand structure, surface insights, and respond like trusted research companions.

### 🚀 **The Vision**

In a world flooded with documents, what wins is not more content — it's context. We're building the future of how we read, learn, and connect by transforming humble PDFs into intelligent document experiences.

## 📁 **Project Structure**

```
├── Round1A/                    # PDF Structure Extraction
│   ├── process_pdfs.py        # Main processing script
│   ├── Dockerfile             # Container configuration
│   ├── requirements.txt       # Dependencies
│   └── README.md              # Detailed documentation
└── Round1B/                   # Persona-Driven Intelligence
    ├── process_pdfs.py        # Main analysis script
    ├── Dockerfile             # Container configuration
    ├── requirements.txt       # Dependencies
    ├── approach_explanation.md # Methodology explanation
    └── README.md              # Detailed documentation
```

## 🧠 **Round 1A: Understand Your Document**

**Challenge Theme**: Connecting the Dots Through Docs

### Mission
Extract structured outlines from PDFs with blazing speed and pinpoint accuracy - identifying titles and hierarchical headings (H1, H2, H3) to enable smarter document experiences.

### Key Features
- **Generic Processing**: Works with any PDF format without hardcoded logic
- **Multi-Strategy Analysis**: Combines font, position, content, and style analysis
- **High Performance**: ≤ 10 seconds for 50-page PDFs
- **Adaptive Thresholds**: Document-specific heading detection

### Quick Start
```bash
cd Round1A
docker build --platform linux/amd64 -t round1a-solution .
docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  --network none \
  round1a-solution
```

## 🎯 **Round 1B: Persona-Driven Document Intelligence**

**Challenge Theme**: Connect What Matters — For the User Who Matters

### Mission
Build an intelligent document analyst that extracts and prioritizes relevant sections from document collections based on specific personas and their job-to-be-done.

### Key Features
- **Universal Persona Support**: Works with any professional role or expertise
- **Contextual Intelligence**: Understands user requirements and preferences
- **Multi-Factor Scoring**: Weighted relevance algorithms
- **Fast Processing**: ≤ 60 seconds for document collections

### Quick Start
```bash
cd Round1B
docker build --platform linux/amd64 -t round1b-solution .
docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  --network none \
  round1b-solution
```

## 🔧 **Technical Excellence**

### Architecture Principles
- **No Hardcoding**: Generic algorithms that adapt to any document
- **High Precision**: Quality over quantity in results
- **Performance Optimized**: Fast processing within constraints
- **Production Ready**: Robust error handling and graceful degradation

### Technology Stack
- **Language**: Python 3.10
- **PDF Processing**: PyMuPDF (fitz)
- **Containerization**: Docker (AMD64 compatible)
- **Dependencies**: Minimal (no external ML models)
- **Architecture**: CPU-only, offline processing

## 📊 **Performance Characteristics**

### Round 1A Specifications
- **Processing Speed**: ≤ 10 seconds for 50-page PDFs
- **Model Size**: No models used (< 200MB total)
- **Network**: Offline operation (no internet access)
- **Runtime**: CPU-only (amd64) with 8 CPUs, 16GB RAM

### Round 1B Specifications
- **Processing Speed**: ≤ 60 seconds for 3-5 documents
- **Model Size**: No external models (< 1GB total)
- **Network**: Offline operation (no internet access)
- **Runtime**: CPU-only with efficient memory usage

## 🎖️ **Competitive Advantages**

1. **True Intelligence**: Advanced algorithms that understand document context
2. **Zero Training**: Immediate deployment without model training
3. **Universal Applicability**: Works across all domains and document types
4. **Explainable Results**: Clear reasoning behind all decisions
5. **Production Ready**: Robust, scalable, and maintainable architecture

## 🚀 **Expected Execution**

Both solutions follow the standard execution pattern:

```bash
# Build
docker build --platform linux/amd64 -t mysolutionname:identifier .

# Run
docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  --network none \
  mysolutionname:identifier
```

## 📈 **Scoring Alignment**

### Round 1A Scoring (45 points total)
- **Heading Detection Accuracy**: 25 points - High precision/recall through multi-strategy analysis
- **Performance**: 10 points - Optimized for speed and size compliance
- **Bonus Multilingual**: 10 points - Generic algorithms handle diverse text patterns

### Round 1B Scoring (100 points total)
- **Section Relevance**: 60 points - Intelligent persona-aware content matching
- **Sub-Section Relevance**: 40 points - Quality granular extraction and ranking

## 🔮 **The Future**

This foundation enables Round 2's beautiful, intuitive reading webapp using Adobe's PDF Embed API. Our structured understanding and persona-driven intelligence will power futuristic document experiences that feel like magic.

## 🎯 **Why This Matters**

We're not just building tools — we're building the future of how we read, learn, and connect. Our solutions demonstrate that with the right algorithms and understanding, we can make every PDF speak to users, connect ideas, and narrate meaning across entire document libraries.

---

**Ready to connect the dots and build PDF experiences that feel like magic? Let's go!** 🚀
