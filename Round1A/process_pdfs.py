#!/usr/bin/env python3
"""
Round 1A: PDF Document Structure Extraction
Connecting the Dots Challenge - Understanding Your Document
"""

import os
import json
import time
import fitz
import re
from collections import defaultdict, Counter
from typing import Dict, List, Tuple, Optional
import statistics

class PDFStructureExtractor:
    """Extracts structured outlines from PDF documents"""
    
    def __init__(self):
        self.debug_mode = False
        
    def process_all_pdfs(self, input_dir: str, output_dir: str):
        """Process all PDF files in input directory"""
        pdf_files = [f for f in os.listdir(input_dir) if f.endswith('.pdf')]
        
        print(f"Processing {len(pdf_files)} PDF documents")
        start_time = time.time()
        
        for pdf_file in pdf_files:
            file_start = time.time()
            input_path = os.path.join(input_dir, pdf_file)
            output_file = pdf_file.replace('.pdf', '.json')
            output_path = os.path.join(output_dir, output_file)
            
            try:
                result = self.extract_document_structure(input_path)
                self.save_json_result(result, output_path)
                
                file_time = time.time() - file_start
                print(f"Processed {pdf_file} -> {output_file} ({file_time:.2f}s)")
                
            except Exception as e:
                print(f"Error processing {pdf_file}: {e}")
                fallback = {"title": "Document", "outline": []}
                self.save_json_result(fallback, output_path)
        
        total_time = time.time() - start_time
        print(f"Completed processing {len(pdf_files)} documents in {total_time:.2f}s")

    def extract_document_structure(self, pdf_path: str) -> Dict:
        """Extract structured outline from PDF document"""
        doc = fitz.open(pdf_path)
        
        try:
            # Extract text with formatting information
            text_elements = self.extract_formatted_text(doc)
            
            # Analyze document characteristics
            doc_stats = self.analyze_document_statistics(text_elements)
            
            # Extract document title
            title = self.extract_document_title(text_elements, doc_stats)
            
            # Extract hierarchical outline
            outline = self.extract_document_outline(text_elements, doc_stats)
            
            return {
                "title": title,
                "outline": outline
            }
        finally:
            doc.close()

    def extract_formatted_text(self, doc) -> List[Dict]:
        """Extract text elements with formatting information"""
        text_elements = []
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            blocks = page.get_text("dict")
            
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
                            text_elements.append({
                                "text": line_text.strip(),
                                "page": page_num,
                                "avg_size": statistics.mean(font_sizes) if font_sizes else 12,
                                "max_size": max(font_sizes) if font_sizes else 12,
                                "is_bold": any(flag & 2**4 for flag in style_flags),
                                "is_italic": any(flag & 2**6 for flag in style_flags),
                                "bbox": line.get("bbox", [0, 0, 0, 0])
                            })
        
        return text_elements

    def analyze_document_statistics(self, text_elements: List[Dict]) -> Dict:
        """Analyze document-wide statistics for intelligent processing"""
        if not text_elements:
            return {"dominant_size": 12, "size_thresholds": {"h1": 18, "h2": 15, "h3": 13}}
        
        # Font size analysis
        font_sizes = [elem["max_size"] for elem in text_elements]
        size_counter = Counter(font_sizes)
        dominant_size = size_counter.most_common(1)[0][0]
        
        # Calculate adaptive thresholds
        unique_sizes = sorted(set(font_sizes), reverse=True)
        
        if len(unique_sizes) >= 3:
            h1_threshold = unique_sizes[0]
            h2_threshold = unique_sizes[1] if len(unique_sizes) > 1 else dominant_size * 1.3
            h3_threshold = unique_sizes[2] if len(unique_sizes) > 2 else dominant_size * 1.1
        else:
            h1_threshold = max(dominant_size * 1.5, max(font_sizes) * 0.9)
            h2_threshold = dominant_size * 1.3
            h3_threshold = dominant_size * 1.1
        
        return {
            "dominant_size": dominant_size,
            "all_sizes": font_sizes,
            "size_distribution": dict(size_counter),
            "size_thresholds": {
                "h1": h1_threshold,
                "h2": h2_threshold,
                "h3": h3_threshold
            }
        }

    def extract_document_title(self, text_elements: List[Dict], doc_stats: Dict) -> str:
        """Extract document title using multi-factor analysis"""
        if not text_elements:
            return "Document"
        
        # Focus on first page elements
        first_page_elements = [elem for elem in text_elements if elem["page"] == 0][:15]
        
        title_candidates = []
        
        for i, elem in enumerate(first_page_elements):
            text = elem["text"].strip()
            if not text or len(text) < 3:
                continue
            
            # Calculate title score using multiple factors
            size_score = self.calculate_size_score(elem, doc_stats)
            position_score = self.calculate_position_score(i)
            content_score = self.calculate_content_score(text)
            style_score = self.calculate_style_score(elem)
            
            # Weighted combination
            total_score = (size_score * 0.4 + position_score * 0.2 + 
                          content_score * 0.2 + style_score * 0.2)
            
            title_candidates.append((total_score, text))
        
        if title_candidates:
            title_candidates.sort(key=lambda x: x[0], reverse=True)
            best_title = title_candidates[0][1]
            return self.clean_title(best_title)
        
        return "Document"

    def calculate_size_score(self, elem: Dict, doc_stats: Dict) -> float:
        """Calculate size-based score"""
        size_ratio = elem["max_size"] / doc_stats["dominant_size"]
        
        if size_ratio >= 2.5:
            return 1.0
        elif size_ratio >= 2.0:
            return 0.9
        elif size_ratio >= 1.8:
            return 0.8
        elif size_ratio >= 1.5:
            return 0.7
        elif size_ratio >= 1.3:
            return 0.5
        else:
            return 0.2

    def calculate_position_score(self, position: int) -> float:
        """Calculate position-based score"""
        if position == 0:
            return 1.0
        elif position <= 2:
            return 0.8
        elif position <= 5:
            return 0.6
        else:
            return 0.3

    def calculate_content_score(self, text: str) -> float:
        """Calculate content quality score"""
        word_count = len(text.split())
        score = 0.0
        
        # Length scoring
        if 3 <= word_count <= 20:
            score += 0.5
        elif word_count <= 30:
            score += 0.3
        
        # Pattern scoring
        if text.istitle():
            score += 0.2
        elif text.isupper() and word_count <= 12:
            score += 0.3
        
        # Avoid non-title patterns
        if re.match(r'^\d+\.', text) or text.lower().startswith(('page ', 'figure ')):
            score -= 0.5
        
        return max(0, score)

    def calculate_style_score(self, elem: Dict) -> float:
        """Calculate style-based score"""
        score = 0.0
        if elem["is_bold"]:
            score += 0.6
        if elem["is_italic"]:
            score += 0.2
        return score

    def clean_title(self, title: str) -> str:
        """Clean and format title"""
        title = re.sub(r'\s+', ' ', title).strip()
        if len(title) > 100:
            words = title[:100].split()
            if len(words) > 1:
                title = ' '.join(words[:-1])
        return title if len(title) >= 3 else "Document"

    def extract_document_outline(self, text_elements: List[Dict], doc_stats: Dict) -> List[Dict]:
        """Extract hierarchical document outline"""
        outline = []
        thresholds = doc_stats["size_thresholds"]
        
        for elem in text_elements:
            text = elem["text"].strip()
            if not text or len(text) < 2:
                continue
            
            # Calculate heading score
            heading_score = self.calculate_heading_score(elem, doc_stats)
            
            if heading_score >= 0.7:  # High precision threshold
                level = self.determine_heading_level(elem, thresholds, text)
                
                outline.append({
                    "level": level,
                    "text": text,
                    "page": elem["page"],
                    "confidence": heading_score
                })
        
        # Post-process for quality
        outline = self.post_process_outline(outline)
        
        # Remove confidence scores
        for item in outline:
            item.pop("confidence", None)
        
        return outline

    def calculate_heading_score(self, elem: Dict, doc_stats: Dict) -> float:
        """Calculate heading detection score"""
        text = elem["text"].strip()
        score = 0.0
        
        # Font size factor
        size_ratio = elem["max_size"] / doc_stats["dominant_size"]
        if size_ratio >= 2.0:
            score += 0.5
        elif size_ratio >= 1.8:
            score += 0.45
        elif size_ratio >= 1.5:
            score += 0.4
        elif size_ratio >= 1.3:
            score += 0.3
        elif size_ratio >= 1.2:
            score += 0.2
        elif size_ratio >= 1.1:
            score += 0.1
        
        # Style factors
        if elem["is_bold"]:
            score += 0.25
        
        # Pattern factors
        if re.match(r'^\d+\.\d+\.?\s+', text):  # 1.1, 2.3, etc.
            score += 0.3
        elif re.match(r'^\d+\.?\s+', text):  # 1., 2., etc.
            score += 0.25
        elif re.match(r'^[A-Z]\.?\s+', text):  # A., B., etc.
            score += 0.2
        elif re.match(r'^(Chapter|Section|Part)\s+\d+', text, re.I):
            score += 0.35
        elif re.match(r'^(Appendix|Abstract|Introduction|Conclusion)', text, re.I):
            score += 0.3
        
        # Case patterns
        word_count = len(text.split())
        if text.isupper() and 2 <= word_count <= 8:
            score += 0.2
        elif text.istitle() and 2 <= word_count <= 12:
            score += 0.15
        
        # Length considerations
        if 1 <= word_count <= 15:
            score += 0.1
        elif word_count > 25:
            score -= 0.3
        
        # Punctuation
        if text.endswith(':'):
            score += 0.15
        elif text.endswith('.') and word_count > 10:
            score -= 0.2
        
        return min(score, 1.0)

    def determine_heading_level(self, elem: Dict, thresholds: Dict, text: str) -> str:
        """Determine heading level"""
        size = elem["max_size"]
        
        # Primary classification by size
        if size >= thresholds["h1"]:
            base_level = "H1"
        elif size >= thresholds["h2"]:
            base_level = "H2"
        else:
            base_level = "H3"
        
        # Pattern-based adjustments
        if re.match(r'^(Chapter|Part)\s+\d+', text, re.I):
            return "H1"
        elif re.match(r'^Section\s+\d+', text, re.I):
            return "H2"
        elif re.match(r'^\d+\.\d+', text):  # Multi-level numbering
            return "H3"
        elif re.match(r'^\d+\.?\s+', text) and base_level != "H3":
            return "H2"
        elif text.lower() in ['abstract', 'introduction', 'conclusion', 'references']:
            return "H1"
        
        return base_level

    def post_process_outline(self, outline: List[Dict]) -> List[Dict]:
        """Post-process outline for quality"""
        if not outline:
            return outline
        
        # Remove duplicates
        seen = set()
        unique_outline = []
        for item in outline:
            key = (item["text"].lower().strip(), item["page"])
            if key not in seen:
                seen.add(key)
                unique_outline.append(item)
        
        # Sort by page and confidence
        unique_outline.sort(key=lambda x: (x["page"], -x["confidence"]))
        
        # Apply limits for precision
        page_counts = defaultdict(int)
        filtered_outline = []
        max_per_page = 5
        
        for item in unique_outline:
            page = item["page"]
            if page_counts[page] < max_per_page and item["confidence"] >= 0.7:
                filtered_outline.append(item)
                page_counts[page] += 1
        
        # Global limit
        if len(filtered_outline) > 20:
            filtered_outline.sort(key=lambda x: x["confidence"], reverse=True)
            filtered_outline = filtered_outline[:20]
            filtered_outline.sort(key=lambda x: x["page"])
        
        return filtered_outline

    def save_json_result(self, result: Dict, output_path: str):
        """Save result to JSON file"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

def main():
    """Main execution function"""
    extractor = PDFStructureExtractor()
    extractor.process_all_pdfs('/app/input', '/app/output')

if __name__ == "__main__":
    main()
