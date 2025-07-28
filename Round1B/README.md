# Round 1B: Persona-Driven Document Intelligence

## Challenge Theme: Connect What Matters — For the User Who Matters

### Overview

This solution builds an intelligent document analyst that extracts and prioritizes the most relevant sections from document collections based on specific personas and their job-to-be-done requirements. The system understands user context and delivers personalized content recommendations.

### Approach

Our persona-driven approach combines:

1. **Persona Intelligence**: Analyzes user descriptions to extract expertise areas, preferences, and priorities
2. **Semantic Content Processing**: Extracts meaningful sections from documents with type classification
3. **Multi-Factor Relevance Scoring**: Uses weighted algorithms to score content relevance
4. **Intelligent Selection**: Ranks and selects sections ensuring both relevance and diversity

### Key Features

- **Universal Persona Support**: Works with any professional role or domain expertise
- **Contextual Understanding**: Adapts analysis based on specific job requirements
- **High Precision**: Uses confidence thresholds and quality filtering
- **Fast Processing**: Optimized for sub-60-second analysis of document collections

### Technical Implementation

#### Persona Analysis
The system creates comprehensive persona profiles including:
- Persona type classification (academic_researcher, business_analyst, student, etc.)
- Domain expertise extraction from descriptions
- Job priority analysis from task requirements
- Content preference inference (technical depth, quantitative focus, etc.)

#### Relevance Scoring Algorithm
```python
relevance_score = (
    keyword_match * 0.3 +           # Expertise and priority alignment
    section_type * 0.2 +            # Content type relevance
    content_depth * 0.2 +           # Technical detail appropriateness
    quantitative_content * 0.15 +   # Data and analysis presence
    position_importance * 0.15      # Document structural significance
)
```

#### Adaptive Weighting
- **Academic Researchers**: Higher emphasis on methodology and technical depth
- **Business Analysts**: Focus on quantitative content and results
- **Students**: Prioritize introductory and conceptual content

### Sample Test Cases Supported

#### Test Case 1: Academic Research
- **Documents**: Research papers on specialized topics
- **Persona**: PhD Researcher in domain area
- **Job**: Literature review focusing on methodologies and benchmarks
- **Output**: Methodology sections, results analysis, performance data

#### Test Case 2: Business Analysis
- **Documents**: Annual reports from companies
- **Persona**: Investment Analyst
- **Job**: Analyze revenue trends and market positioning
- **Output**: Financial sections, strategic analysis, quantitative metrics

#### Test Case 3: Educational Content
- **Documents**: Textbook chapters on subject matter
- **Persona**: Student in academic program
- **Job**: Exam preparation on specific topics
- **Output**: Key concepts, mechanisms, important definitions

### How to Build and Run

#### Using Docker (Recommended)
```bash
# Build the image
docker build --platform linux/amd64 -t round1b-solution .

# Run the solution
docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  --network none \
  round1b-solution
```

#### Input Specification
- **Documents**: 3-10 PDF files in `/app/input/` directory
- **Configuration**: Optional JSON file with persona and job description
- **Automatic Fallback**: Uses intelligent defaults if no configuration provided

#### Expected Output Format
```json
{
  "metadata": {
    "input_documents": ["doc1.pdf", "doc2.pdf"],
    "persona": "PhD Researcher in Computational Biology",
    "job_to_be_done": "Prepare comprehensive literature review",
    "processing_timestamp": "2024-01-01T12:00:00"
  },
  "extracted_sections": [
    {
      "document": "paper1.pdf",
      "page_number": 3,
      "section_title": "Methodology",
      "importance_rank": 1
    }
  ],
  "sub_section_analysis": [
    {
      "document": "paper1.pdf",
      "refined_text": "The methodology employed...",
      "page_number": 3
    }
  ]
}
```

### Performance Characteristics

- **Processing Time**: ≤ 60 seconds for 3-5 document collections
- **Model Size**: No external models (< 1GB total)
- **Memory Usage**: Efficient streaming processing
- **Accuracy**: High precision across diverse domains and personas

### Scoring Criteria Alignment

#### Section Relevance (60 points)
- Intelligent keyword matching with persona expertise
- Section type alignment with user preferences
- Job requirement prioritization
- Contextual understanding of user needs

#### Sub-Section Relevance (40 points)
- Granular content analysis and extraction
- Quality-based text refinement
- Appropriate detail level for persona
- Coherent narrative flow

### Architecture Benefits

1. **Scalable**: Handles unlimited persona and document combinations
2. **Intelligent**: True understanding of user context and requirements
3. **Efficient**: Fast processing with minimal resource usage
4. **Extensible**: Easy to add new persona types and scoring factors
5. **Reliable**: Robust error handling and quality assurance

This solution enables personalized document analysis that truly understands what matters most to each specific user, delivering contextually relevant insights that support their unique professional requirements.
