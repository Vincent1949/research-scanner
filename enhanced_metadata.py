"""
Enhanced Metadata Extraction for Scholar's Terminal
Captures page numbers, figure references, and enables "Open in PDF" functionality
"""

import re
from typing import Dict, Optional, List
from pathlib import Path


class EnhancedMetadataExtractor:
    """Extract rich metadata including page numbers and figure references"""
    
    # Patterns to detect figure/diagram references
    FIGURE_PATTERNS = [
        r'Figure\s+(\d+\.?\d*)',
        r'Fig\.\s+(\d+\.?\d*)',
        r'Diagram\s+(\d+\.?\d*)',
        r'Table\s+(\d+\.?\d*)',
        r'Chart\s+(\d+\.?\d*)',
        r'Illustration\s+(\d+\.?\d*)',
        r'Exhibit\s+(\d+\.?\d*)',
    ]
    
    # Patterns for page references
    PAGE_PATTERNS = [
        r'page\s+(\d+)',
        r'p\.\s+(\d+)',
        r'pp\.\s+(\d+)-(\d+)',
    ]
    
    @staticmethod
    def extract_figure_references(text: str) -> List[str]:
        """Extract figure/diagram references from text"""
        references = []
        
        for pattern in EnhancedMetadataExtractor.FIGURE_PATTERNS:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                ref_type = pattern.split(r'\s+')[0].replace('\\', '')
                references.append(f"{ref_type} {match}")
        
        return list(set(references))  # Remove duplicates
    
    @staticmethod
    def extract_page_references(text: str) -> List[int]:
        """Extract page number references from text"""
        pages = []
        
        for pattern in EnhancedMetadataExtractor.PAGE_PATTERNS:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    # Range of pages (e.g., pp. 45-67)
                    pages.extend(range(int(match[0]), int(match[1]) + 1))
                else:
                    pages.append(int(match))
        
        return sorted(list(set(pages)))
    
    @staticmethod
    def has_visual_content(text: str) -> bool:
        """Detect if chunk likely references visual content"""
        visual_keywords = [
            'figure', 'diagram', 'chart', 'graph', 'table',
            'illustration', 'image', 'photo', 'picture',
            'shows', 'depicts', 'illustrates', 'shown in',
            'see figure', 'as shown', 'displayed in'
        ]
        
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in visual_keywords)
    
    @staticmethod
    def create_enhanced_metadata(
        file_path: str,
        source_name: str,
        source_type: str,
        chunk_index: int,
        chunk_text: str,
        page_number: Optional[int] = None
    ) -> Dict:
        """
        Create enhanced metadata with visual content detection
        
        Args:
            file_path: Full path to source file
            source_name: Name of the source (from config)
            source_type: Type of source (books, code, etc.)
            chunk_index: Index of this chunk in the file
            chunk_text: The actual text content
            page_number: Page number if available (PDFs)
        
        Returns:
            Enhanced metadata dictionary
        """
        path = Path(file_path)
        
        # Base metadata
        metadata = {
            "source": str(file_path),
            "source_name": source_name,
            "source_type": source_type,
            "filename": path.name,
            "file_type": path.suffix.lower().lstrip('.'),
            "chunk_index": chunk_index,
        }
        
        # Add page number if available
        if page_number is not None:
            metadata["page_number"] = page_number
        
        # Extract figure references
        figures = EnhancedMetadataExtractor.extract_figure_references(chunk_text)
        if figures:
            metadata["figures"] = figures
        
        # Detect visual content
        if EnhancedMetadataExtractor.has_visual_content(chunk_text):
            metadata["has_visual_content"] = True
        
        # Extract page references from text
        page_refs = EnhancedMetadataExtractor.extract_page_references(chunk_text)
        if page_refs:
            metadata["page_references"] = page_refs
        
        return metadata


class PDFPageTracker:
    """Track page numbers while processing PDFs"""
    
    def __init__(self):
        self.current_page = 0
        self.chars_per_page = 3000  # Approximate characters per page
        self.char_count = 0
    
    def update(self, text_chunk: str) -> int:
        """
        Update character count and estimate page number
        
        Args:
            text_chunk: Text being processed
        
        Returns:
            Estimated page number
        """
        self.char_count += len(text_chunk)
        self.current_page = self.char_count // self.chars_per_page
        return self.current_page
    
    def reset(self):
        """Reset for new document"""
        self.current_page = 0
        self.char_count = 0


# ============================================================
# RESPONSE FORMATTER
# ============================================================

class OpenPDFActionFormatter:
    """Format search results with 'Open in PDF' actions"""
    
    @staticmethod
    def format_source_with_action(metadata: Dict, relevance_score: float = 1.0) -> Dict:
        """
        Format a source result with action capability
        
        Args:
            metadata: Chunk metadata from database
            relevance_score: Search relevance score
        
        Returns:
            Formatted source with action
        """
        source = {
            "filename": metadata.get("filename", "Unknown"),
            "source_type": metadata.get("source_type", "unknown"),
            "relevance": relevance_score,
        }
        
        # Add page number if available
        if "page_number" in metadata:
            source["page_number"] = metadata["page_number"]
        
        # Add figure references if available
        if "figures" in metadata:
            source["figures"] = metadata["figures"]
        
        # Add action if this is a PDF with page number
        if metadata.get("file_type") == "pdf" and "page_number" in metadata:
            source["action"] = {
                "type": "open_pdf",
                "file_path": metadata["source"],
                "page": metadata["page_number"],
                "label": f"Open PDF (page {metadata['page_number']})"
            }
        
        # Flag visual content
        if metadata.get("has_visual_content"):
            source["has_visual"] = True
        
        return source
    
    @staticmethod
    def format_response_with_actions(
        answer: str,
        sources: List[Dict],
        show_visual_hint: bool = True
    ) -> Dict:
        """
        Format complete response with actions
        
        Args:
            answer: Generated answer text
            sources: List of source metadata
            show_visual_hint: Add hint about visual content
        
        Returns:
            Complete formatted response
        """
        # Format sources with actions
        formatted_sources = []
        has_visual_content = False
        
        for source_meta in sources:
            formatted = OpenPDFActionFormatter.format_source_with_action(source_meta)
            formatted_sources.append(formatted)
            
            if formatted.get("has_visual"):
                has_visual_content = True
        
        response = {
            "answer": answer,
            "sources": formatted_sources,
        }
        
        # Add visual content hint
        if show_visual_hint and has_visual_content:
            response["visual_content_note"] = (
                "Some sources contain figures or diagrams. "
                "Click 'Open PDF' to view them in context."
            )
        
        return response


# ============================================================
# USAGE EXAMPLE
# ============================================================

def example_usage():
    """Example of how to use enhanced metadata"""
    
    # During database building
    text = """
    Figure 8.3 shows a cross-section of a stratovolcano.
    These composite volcanoes form from alternating layers
    of lava flows and pyroclastic material, as illustrated
    in the diagram.
    """
    
    metadata = EnhancedMetadataExtractor.create_enhanced_metadata(
        file_path="D:/Books/Earth Science.pdf",
        source_name="Personal Library",
        source_type="books",
        chunk_index=187,
        chunk_text=text,
        page_number=187
    )
    
    print("Enhanced Metadata:")
    print(metadata)
    # Output:
    # {
    #     "source": "D:/Books/Earth Science.pdf",
    #     "source_name": "Personal Library",
    #     "source_type": "books",
    #     "filename": "Earth Science.pdf",
    #     "file_type": "pdf",
    #     "chunk_index": 187,
    #     "page_number": 187,
    #     "figures": ["Figure 8.3"],
    #     "has_visual_content": True
    # }
    
    # During search response formatting
    formatted = OpenPDFActionFormatter.format_source_with_action(metadata)
    
    print("\nFormatted Source with Action:")
    print(formatted)
    # Output:
    # {
    #     "filename": "Earth Science.pdf",
    #     "source_type": "books",
    #     "page_number": 187,
    #     "figures": ["Figure 8.3"],
    #     "action": {
    #         "type": "open_pdf",
    #         "file_path": "D:/Books/Earth Science.pdf",
    #         "page": 187,
    #         "label": "Open PDF (page 187)"
    #     },
    #     "has_visual": True
    # }


if __name__ == "__main__":
    example_usage()
