#!/usr/bin/env python3
"""
Round 1B: Persona-Driven Document Intelligence
Connecting the Dots Challenge - Connect What Matters For the User Who Matters
"""

import os
import json
import time
import fitz
import re
from collections import defaultdict, Counter
from typing import Dict, List, Set
import statistics
from datetime import datetime

class PersonaAnalyzer:
    """Analyzes persona and job requirements"""
    
    def create_persona_profile(self, persona: str, job_to_be_done: str) -> Dict:
        """Create comprehensive persona profile"""
        persona_type = self.classify_persona_type(persona)
        expertise_areas = self.extract_expertise_areas(persona)
        job_priorities = self.analyze_job_priorities(job_to_be_done)
        content_preferences = self.infer_content_preferences(persona, job_to_be_done)
        
        return {
            "persona_type": persona_type,
            "expertise_areas": expertise_areas,
            "job_priorities": job_priorities,
            "content_preferences": content_preferences,
            "relevance_weights": self.calculate_relevance_weights(persona_type)
        }

    def classify_persona_type(self, persona: str) -> str:
        """Classify persona into categories"""
        persona_lower = persona.lower()
        
        if any(term in persona_lower for term in ['researcher', 'phd', 'scientist', 'academic']):
            return "academic_researcher"
        elif any(term in persona_lower for term in ['analyst', 'investment', 'financial', 'business']):
            return "business_analyst"
        elif any(term in persona_lower for term in ['student', 'undergraduate', 'graduate']):
            return "student"
        elif any(term in persona_lower for term in ['engineer', 'developer', 'technical']):
            return "technical_professional"
        else:
            return "general_professional"

    def extract_expertise_areas(self, persona: str) -> List[str]:
        """Extract expertise keywords from persona"""
        expertise_keywords = []
        
        # Domain-specific extraction
        if re.search(r'computational biology|drug discovery', persona, re.I):
            expertise_keywords.extend(['computational', 'biology', 'drug', 'discovery', 'methodology', 'datasets'])
        if re.search(r'investment|financial|analyst', persona, re.I):
            expertise_keywords.extend(['financial', 'investment', 'revenue', 'market', 'analysis'])
        if re.search(r'chemistry|organic|student', persona, re.I):
            expertise_keywords.extend(['chemistry', 'organic', 'reaction', 'kinetics', 'mechanisms'])
        
        # General keyword extraction
        words = re.findall(r'\b[a-zA-Z]{4,}\b', persona.lower())
        common_words = {'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had'}
        expertise_keywords.extend([w for w in words if w not in common_words])
        
        return list(set(expertise_keywords))

    def analyze_job_priorities(self, job_description: str) -> List[str]:
        """Extract job priorities"""
        priorities = []
        job_lower = job_description.lower()
        
        if 'literature review' in job_lower:
            priorities.extend(['methodology', 'datasets', 'performance', 'benchmarks'])
        if 'revenue trends' in job_lower:
            priorities.extend(['revenue', 'trends', 'financial', 'analysis'])
        if 'exam preparation' in job_lower:
            priorities.extend(['concepts', 'mechanisms', 'key', 'important'])
        
        # Extract action keywords
        action_patterns = [r'analyze?\s+(\w+)', r'identify\s+(\w+)', r'prepare\s+(\w+)']
        for pattern in action_patterns:
            matches = re.findall(pattern, job_description, re.I)
            priorities.extend(matches)
        
        return list(set(priorities))

    def infer_content_preferences(self, persona: str, job: str) -> Dict:
        """Infer content preferences"""
        preferences = {
            "technical_depth": 0.5,
            "quantitative_focus": 0.5,
            "summary_preference": 0.5,
            "detail_preference": 0.5
        }
        
        if 'researcher' in persona.lower() or 'phd' in persona.lower():
            preferences["technical_depth"] = 0.9
            preferences["detail_preference"] = 0.8
        elif 'student' in persona.lower():
            preferences["summary_preference"] = 0.8
            preferences["technical_depth"] = 0.4
        elif 'analyst' in persona.lower():
            preferences["quantitative_focus"] = 0.9
        
        return preferences

    def calculate_relevance_weights(self, persona_type: str) -> Dict:
        """Calculate relevance weights"""
        base_weights = {
            "keyword_match": 0.3,
            "section_type": 0.2,
            "content_depth": 0.2,
            "quantitative_content": 0.15,
            "position_importance": 0.15
        }
        
        if persona_type == "academic_researcher":
            base_weights["content_depth"] = 0.3
            base_weights["keyword_match"] = 0.25
        elif persona_type == "business_analyst":
            base_weights["quantitative_content"] = 0.35
            base_weights["keyword_match"] = 0.3
        
        return base_weights


class DocumentProcessor:
    """Processes documents to extract sections"""
    
    def extract_document_sections(self, document: Dict) -> List[Dict]:
        """Extract sections from document"""
        sections = []
        doc_name = document["name"]
        pages_content = document["content"]["pages"]
        
        # Analyze document structure
        doc_analysis = self.analyze_document_structure(pages_content)
        
        # Extract sections
        current_section = None
        
        for page in pages_content:
            page_num = page["page_num"]
            
            for elem in page["elements"]:
                text = elem["text"].strip()
                if not text:
                    continue
                
                # Check if heading
                if self.is_section_heading(elem, doc_analysis):
                    # Save previous section
                    if current_section and current_section["content"].strip():
                        sections.append(current_section)
                    
                    # Start new section
                    current_section = {
                        "title": text,
                        "content": "",
                        "document": doc_name,
                        "page": page_num,
                        "section_type": self.classify_section_type(text)
                    }
                else:
                    # Add to current section
                    if current_section:
                        current_section["content"] += text + " "
        
        # Add final section
        if current_section and current_section["content"].strip():
            sections.append(current_section)
        
        return sections

    def analyze_document_structure(self, pages_content: List[Dict]) -> Dict:
        """Analyze document structure"""
        all_elements = []
        for page in pages_content:
            all_elements.extend(page["elements"])
        
        if not all_elements:
            return {"primary_size": 12, "heading_threshold": 14}
        
        sizes = [elem["avg_size"] for elem in all_elements]
        size_counter = Counter(sizes)
        primary_size = size_counter.most_common(1)[0][0]
        
        return {
            "primary_size": primary_size,
            "heading_threshold": primary_size * 1.2
        }

    def is_section_heading(self, elem: Dict, doc_analysis: Dict) -> bool:
        """Check if element is a heading"""
        text = elem["text"].strip()
        
        # Size check
        if elem["avg_size"] >= doc_analysis["heading_threshold"]:
            return True
        
        # Style check
        if elem["is_bold"] and len(text.split()) <= 15:
            return True
        
        # Pattern check
        patterns = [
            r'^\d+\.?\s+[A-Z]',
            r'^[A-Z][A-Z\s]+$',
            r'^(Chapter|Section|Abstract|Introduction|Conclusion|Methodology)$'
        ]
        
        for pattern in patterns:
            if re.match(pattern, text, re.I):
                return True
        
        return False

    def classify_section_type(self, text: str) -> str:
        """Classify section type"""
        text_lower = text.lower()
        
        if any(term in text_lower for term in ['abstract', 'summary']):
            return "abstract"
        elif any(term in text_lower for term in ['introduction', 'background']):
            return "introduction"
        elif any(term in text_lower for term in ['methodology', 'methods']):
            return "methodology"
        elif any(term in text_lower for term in ['results', 'findings']):
            return "results"
        elif any(term in text_lower for term in ['discussion', 'analysis']):
            return "discussion"
        elif any(term in text_lower for term in ['conclusion']):
            return "conclusion"
        else:
            return "general"


class RelevanceScorer:
    """Scores section relevance"""
    
    def score_sections(self, sections: List[Dict], persona_profile: Dict) -> List[Dict]:
        """Score all sections for relevance"""
        scored_sections = []
        
        for section in sections:
            relevance_score = self.calculate_relevance_score(section, persona_profile)
            
            section_with_score = section.copy()
            section_with_score["relevance_score"] = relevance_score
            scored_sections.append(section_with_score)
        
        return scored_sections

    def calculate_relevance_score(self, section: Dict, persona_profile: Dict) -> float:
        """Calculate comprehensive relevance score"""
        weights = persona_profile["relevance_weights"]
        
        keyword_score = self.calculate_keyword_score(section, persona_profile)
        section_type_score = self.calculate_section_type_score(section, persona_profile)
        content_depth_score = self.calculate_content_depth_score(section)
        quantitative_score = self.calculate_quantitative_score(section)
        position_score = self.calculate_position_score(section)
        
        total_score = (
            keyword_score * weights["keyword_match"] +
            section_type_score * weights["section_type"] +
            content_depth_score * weights["content_depth"] +
            quantitative_score * weights["quantitative_content"] +
            position_score * weights["position_importance"]
        )
        
        return min(total_score, 1.0)

    def calculate_keyword_score(self, section: Dict, persona_profile: Dict) -> float:
        """Calculate keyword matching score"""
        expertise_areas = persona_profile["expertise_areas"]
        job_priorities = persona_profile["job_priorities"]
        
        text = (section["title"] + " " + section["content"]).lower()
        
        expertise_matches = sum(1 for keyword in expertise_areas if keyword.lower() in text)
        priority_matches = sum(1 for priority in job_priorities if priority.lower() in text)
        
        expertise_score = min(expertise_matches / max(len(expertise_areas), 1), 1.0)
        priority_score = min(priority_matches / max(len(job_priorities), 1), 1.0)
        
        return (expertise_score * 0.4 + priority_score * 0.6)

    def calculate_section_type_score(self, section: Dict, persona_profile: Dict) -> float:
        """Calculate section type relevance"""
        section_type = section["section_type"]
        persona_type = persona_profile["persona_type"]
        
        type_preferences = {
            "academic_researcher": {
                "methodology": 0.9, "results": 0.9, "discussion": 0.8,
                "abstract": 0.7, "introduction": 0.6
            },
            "business_analyst": {
                "results": 0.9, "discussion": 0.8, "abstract": 0.7
            },
            "student": {
                "introduction": 0.9, "methodology": 0.7, "abstract": 0.8
            }
        }
        
        preferences = type_preferences.get(persona_type, {})
        return preferences.get(section_type, 0.5)

    def calculate_content_depth_score(self, section: Dict) -> float:
        """Calculate content depth score"""
        word_count = len(section["content"].split())
        
        if word_count < 50:
            return 0.3
        elif word_count < 200:
            return 0.6
        elif word_count < 500:
            return 0.8
        else:
            return 1.0

    def calculate_quantitative_score(self, section: Dict) -> float:
        """Calculate quantitative content score"""
        content = section["title"] + " " + section["content"]
        
        numbers = len(re.findall(r'\b\d+(?:\.\d+)?%?\b', content))
        statistical_terms = len(re.findall(r'\b(?:mean|median|average|analysis)\b', content, re.I))
        
        quant_indicators = numbers + statistical_terms * 2
        return min(quant_indicators / 5.0, 1.0)

    def calculate_position_score(self, section: Dict) -> float:
        """Calculate position score"""
        page = section["page"]
        
        if page == 0:
            return 1.0
        elif page <= 2:
            return 0.8
        elif page <= 5:
            return 0.6
        else:
            return 0.4


class SectionRanker:
    """Ranks and selects sections"""
    
    def rank_and_select(self, scored_sections: List[Dict]) -> List[Dict]:
        """Rank sections and select top ones"""
        if not scored_sections:
            return []
        
        # Sort by relevance score
        ranked_sections = sorted(scored_sections, key=lambda x: x["relevance_score"], reverse=True)
        
        # Select with diversity
        selected = []
        doc_counts = defaultdict(int)
        max_sections = 10
        min_score = 0.3
        max_per_doc = 3
        
        for section in ranked_sections:
            if len(selected) >= max_sections:
                break
            
            if section["relevance_score"] < min_score:
                continue
            
            doc_name = section["document"]
            if doc_counts[doc_name] >= max_per_doc:
                continue
            
            selected.append(section)
            doc_counts[doc_name] += 1
        
        # Add ranking
        for i, section in enumerate(selected):
            section["rank"] = i + 1
        
        return selected


class PersonaDrivenAnalyzer:
    """Main analyzer for persona-driven document intelligence"""
    
    def __init__(self):
        self.persona_analyzer = PersonaAnalyzer()
        self.document_processor = DocumentProcessor()
        self.relevance_scorer = RelevanceScorer()
        self.section_ranker = SectionRanker()
        
    def process_document_collection(self, input_dir: str, output_dir: str):
        """Process document collection"""
        print("Starting persona-driven document analysis")
        start_time = time.time()
        
        try:
            # Load configuration
            config = self.load_configuration(input_dir)
            
            # Extract documents
            documents = self.extract_documents(config["documents"], input_dir)
            
            # Create persona profile
            persona_profile = self.persona_analyzer.create_persona_profile(
                config["persona"], config["job_to_be_done"]
            )
            
            # Extract sections
            all_sections = []
            for doc in documents:
                doc_sections = self.document_processor.extract_document_sections(doc)
                all_sections.extend(doc_sections)
            
            # Score relevance
            scored_sections = self.relevance_scorer.score_sections(all_sections, persona_profile)
            
            # Rank and select
            selected_sections = self.section_ranker.rank_and_select(scored_sections)
            
            # Generate output
            result = self.generate_output(config, selected_sections)
            
            # Save result
            output_path = os.path.join(output_dir, "challenge1b_output.json")
            self.save_output(result, output_path)
            
            total_time = time.time() - start_time
            print(f"Analysis completed in {total_time:.2f}s")
            print(f"Selected {len(selected_sections)} relevant sections")
            
        except Exception as e:
            print(f"Error in analysis: {e}")
            fallback = self.create_fallback_output()
            output_path = os.path.join(output_dir, "challenge1b_output.json")
            self.save_output(fallback, output_path)

    def load_configuration(self, input_dir: str) -> Dict:
        """Load processing configuration"""
        config_files = [f for f in os.listdir(input_dir) if f.endswith('.json')]
        
        if config_files:
            with open(os.path.join(input_dir, config_files[0]), 'r') as f:
                return json.load(f)
        else:
            # Default configuration
            pdf_files = [f for f in os.listdir(input_dir) if f.endswith('.pdf')]
            return {
                "documents": pdf_files,
                "persona": "Research Analyst",
                "job_to_be_done": "Analyze and summarize key information"
            }

    def extract_documents(self, document_list: List[str], input_dir: str) -> List[Dict]:
        """Extract content from documents"""
        documents = []
        
        for doc_name in document_list:
            doc_path = os.path.join(input_dir, doc_name)
            if os.path.exists(doc_path) and doc_name.endswith('.pdf'):
                try:
                    doc_content = self.extract_pdf_content(doc_path)
                    documents.append({
                        "name": doc_name,
                        "path": doc_path,
                        "content": doc_content
                    })
                    print(f"Extracted content from {doc_name}")
                except Exception as e:
                    print(f"Warning: Error extracting {doc_name}: {e}")
        
        return documents

    def extract_pdf_content(self, pdf_path: str) -> Dict:
        """Extract content from PDF"""
        doc = fitz.open(pdf_path)
        pages_content = []
        
        try:
            for page_num in range(len(doc)):
                page = doc[page_num]
                blocks = page.get_text("dict")
                page_elements = []
                
                for block in blocks.get("blocks", []):
                    if "lines" in block:
                        for line in block["lines"]:
                            line_text = ""
                            font_sizes = []
                            style_flags = []
                            
                            for span in line["spans"]:
                                text = span.get("text", "").strip()
                                if text:
                                    line_text += text + " "
                                    font_sizes.append(span.get("size", 12))
                                    style_flags.append(span.get("flags", 0))
                            
                            if line_text.strip():
                                page_elements.append({
                                    "text": line_text.strip(),
                                    "avg_size": statistics.mean(font_sizes) if font_sizes else 12,
                                    "is_bold": any(flag & 2**4 for flag in style_flags),
                                    "is_italic": any(flag & 2**6 for flag in style_flags),
                                    "bbox": line.get("bbox", [0, 0, 0, 0]),
                                    "page": page_num
                                })
                
                pages_content.append({
                    "page_num": page_num,
                    "elements": page_elements
                })
        
        finally:
            doc.close()
        
        return {
            "pages": pages_content,
            "total_pages": len(pages_content)
        }

    def generate_output(self, config: Dict, selected_sections: List[Dict]) -> Dict:
        """Generate output in required format"""
        return {
            "metadata": {
                "input_documents": config["documents"],
                "persona": config["persona"],
                "job_to_be_done": config["job_to_be_done"],
                "processing_timestamp": datetime.now().isoformat()
            },
            "extracted_sections": [
                {
                    "document": section["document"],
                    "page_number": section["page"],
                    "section_title": section["title"],
                    "importance_rank": section["rank"]
                }
                for section in selected_sections
            ],
            "sub_section_analysis": [
                {
                    "document": section["document"],
                    "refined_text": section["content"][:500] + "..." if len(section["content"]) > 500 else section["content"],
                    "page_number": section["page"]
                }
                for section in selected_sections[:5]
            ]
        }

    def create_fallback_output(self) -> Dict:
        """Create fallback output"""
        return {
            "metadata": {
                "input_documents": [],
                "persona": "General User",
                "job_to_be_done": "Document Analysis",
                "processing_timestamp": datetime.now().isoformat()
            },
            "extracted_sections": [],
            "sub_section_analysis": []
        }

    def save_output(self, result: Dict, output_path: str):
        """Save result to JSON file"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)


def main():
    """Main execution function"""
    analyzer = PersonaDrivenAnalyzer()
    analyzer.process_document_collection('/app/input', '/app/output')

if __name__ == "__main__":
    main()
