# Round 1A: Understand Your Document

## Challenge Theme: Connecting the Dots Through Docs

### Overview

This solution extracts structured outlines from PDF documents with high accuracy and speed. It identifies document titles and hierarchical headings (H1, H2, H3) to create a foundation for intelligent document experiences.

### Approach

Our solution uses a multi-strategy approach that combines:

1. **Multi-Level Text Extraction**: Extracts text with comprehensive formatting information including font sizes, styles, and positioning
2. **Adaptive Threshold Calculation**: Dynamically determines heading thresholds based on document-specific font size distributions
3. **Ensemble Title Detection**: Uses weighted scoring combining font size, position, content quality, and style factors
4. **Pattern-Based Heading Detection**: Recognizes numbered sections, chapters, and standard academic/business document structures
5. **Quality Post-Processing**: Applies confidence-based filtering and duplicate removal for high precision results

### Key Features

- **Generic Processing**: Works with any PDF format without hardcoded logic
- **High Precision**: Uses confidence thresholds to ensure quality results
- **Fast Performance**: Optimized for sub-10-second processing of 50-page documents
- **Robust Error Handling**: Graceful fallbacks for problematic documents

### Models and Libraries Used

- **PyMuPDF (fitz)**: For PDF text extraction and formatting analysis
- **Python Standard Library**: For statistical analysis, pattern matching, and data processing
- **No External Models**: Completely self-contained with no ML model dependencies

### Technical Implementation

#### Title Detection Algorithm
```python
title_score = (
    size_score * 0.4 +      # Font size relative to document
    position_score * 0.2 +   # Position on first page
    content_score * 0.2 +    # Text quality and patterns
    style_score * 0.2        # Bold/italic formatting
)
```

#### Heading Detection Features
- Font size analysis with document-adaptive thresholds
- Pattern recognition for numbered sections (1.1, 2.3, etc.)
- Style analysis (bold, italic, case patterns)
- Content analysis (length, punctuation, keywords)
- Position and context evaluation

#### Adaptive Thresholds
The system calculates document-specific thresholds:
- H1: Largest font sizes or 1.5x dominant size
- H2: Second largest or 1.3x dominant size  
- H3: Third largest or 1.1x dominant size

### How to Build and Run

#### Using Docker (Recommended)
```bash
# Build the image
docker build --platform linux/amd64 -t round1a-solution .

# Run the solution
docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  --network none \
  round1a-solution
```

#### Expected Input/Output
- **Input**: PDF files in `/app/input/` directory
- **Output**: JSON files in `/app/output/` directory with format:
```json
{
  "title": "Document Title",
  "outline": [
    {"level": "H1", "text": "Chapter 1: Introduction", "page": 0},
    {"level": "H2", "text": "1.1 Overview", "page": 1},
    {"level": "H3", "text": "Background", "page": 2}
  ]
}
```

### Performance Characteristics

- **Processing Speed**: ≤ 10 seconds for 50-page PDFs
- **Memory Usage**: Efficient streaming processing
- **Model Size**: No models used (< 200MB total)
- **Accuracy**: High precision across diverse document types

### Architecture Benefits

1. **Scalable**: Handles documents of any complexity
2. **Maintainable**: Clean, modular code structure
3. **Extensible**: Easy to add new detection strategies
4. **Reliable**: Comprehensive error handling
5. **Efficient**: Optimized algorithms and data structures

This solution enables the foundation for intelligent document experiences by providing accurate structural understanding of PDF documents without relying on hardcoded assumptions or external models.
