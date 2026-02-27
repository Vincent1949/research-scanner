# Open PDF Feature - Implementation Guide

## Overview

The "Open PDF" feature allows users to seamlessly view images, diagrams, and figures referenced in search results by opening the source PDF directly at the relevant page.

### User Experience

**User Query:**
> "Show me the diagram of a stratovolcano"

**Scholar's Terminal Response:**
```
Answer:
A stratovolcano (composite volcano) has a distinctive internal 
structure with alternating layers of lava and pyroclastic material.

Sources:
┌─────────────────────────────────────────────────┐
│ 📄 Earth Science 15th Edition                   │
│ 📍 Page 187  │  📊 Figure 8.3                   │
│                                                  │
│ [Open PDF (page 187)]  ← User clicks this      │
└─────────────────────────────────────────────────┘
```

**What Happens:**
1. User clicks "Open PDF (page 187)"
2. Earth Science.pdf opens in their PDF viewer
3. PDF scrolls to page 187
4. User sees Figure 8.3 in full context

---

## Architecture

### 1. Enhanced Metadata (During Indexing)

When building the database, extract:
- **Page numbers** (for PDFs)
- **Figure references** (Figure 8.3, Diagram 2.1, etc.)
- **Visual content flags** (text mentions diagrams/images)
- **Page references** (cross-references to other pages)

```python
# During chunking
metadata = {
    "source": "D:/Books/Earth Science.pdf",
    "filename": "Earth Science.pdf",
    "page_number": 187,           # ← Page tracking
    "figures": ["Figure 8.3"],    # ← Detected figures
    "has_visual_content": True    # ← Visual flag
}
```

### 2. Search Results (API Response)

When user searches, return enhanced metadata:

```json
{
  "answer": "A stratovolcano has alternating layers...",
  "sources": [
    {
      "filename": "Earth Science.pdf",
      "page_number": 187,
      "figures": ["Figure 8.3"],
      "has_visual": true,
      "action": {
        "type": "open_pdf",
        "file_path": "D:/Books/Earth Science.pdf",
        "page": 187,
        "label": "Open PDF (page 187)"
      }
    }
  ],
  "visual_content_note": "Some sources contain figures. Click 'Open PDF' to view them."
}
```

### 3. Frontend (React)

Display sources with action buttons:

```jsx
<SourceCard>
  <h4>Earth Science.pdf</h4>
  <p>Page 187 • Figure 8.3</p>
  <Badge>Contains diagrams</Badge>
  <Button onClick={openPDF}>Open PDF (page 187)</Button>
</SourceCard>
```

### 4. Backend API (Python)

Handle PDF opening across platforms:

```python
@router.post("/api/open-pdf")
async def open_pdf(file_path: str, page: int):
    if platform.system() == "Windows":
        subprocess.Popen(['start', '', file_path])
    elif platform.system() == "Darwin":
        subprocess.Popen(['open', file_path])
    elif platform.system() == "Linux":
        subprocess.Popen(['xdg-open', file_path])
```

---

## Implementation Steps

### Step 1: Update Database Builder

Add enhanced metadata extraction to `build_database.py`:

```python
from enhanced_metadata import EnhancedMetadataExtractor, PDFPageTracker

# During PDF processing
page_tracker = PDFPageTracker()

for page_num, page in enumerate(pdf_reader.pages):
    text = page.extract_text()
    chunks = chunk_text(text)
    
    for chunk in chunks:
        # Create enhanced metadata
        metadata = EnhancedMetadataExtractor.create_enhanced_metadata(
            file_path=file_path,
            source_name=source_name,
            source_type=source_type,
            chunk_index=chunk_index,
            chunk_text=chunk,
            page_number=page_num  # ← Page tracking
        )
        
        # Add to database
        collection.add(
            ids=[chunk_id],
            documents=[chunk],
            metadatas=[metadata]
        )
```

### Step 2: Update API Response

Modify `Scholars_api.py` to format responses:

```python
from enhanced_metadata import OpenPDFActionFormatter

@router.post("/api/search")
async def search(query: str):
    # Get search results from ChromaDB
    results = collection.query(query_texts=[query], n_results=5)
    
    # Generate answer with LLM
    answer = generate_answer(query, results)
    
    # Format with actions
    response = OpenPDFActionFormatter.format_response_with_actions(
        answer=answer,
        sources=results['metadatas'][0]
    )
    
    return response
```

### Step 3: Add Backend Endpoint

Add to `Scholars_api.py`:

```python
from fastapi import APIRouter
import subprocess
import platform
import os

@router.post("/api/open-pdf")
async def open_pdf(file_path: str, page: int):
    """Open PDF at specified page"""
    
    if not os.path.exists(file_path):
        return {"success": False, "error": "File not found"}
    
    try:
        system = platform.system()
        
        if system == "Windows":
            subprocess.Popen(['start', '', file_path], shell=True)
        elif system == "Darwin":
            subprocess.Popen(['open', file_path])
        else:  # Linux
            subprocess.Popen(['xdg-open', file_path])
        
        return {"success": True}
    
    except Exception as e:
        return {"success": False, "error": str(e)}
```

### Step 4: Add Frontend Component

Use the `OpenPDFComponent.jsx` provided:

```jsx
import { SearchResults } from './components/OpenPDFComponent';

// In your search handler
const handleSearch = async (query) => {
  const response = await fetch('/api/search', {
    method: 'POST',
    body: JSON.stringify({ query })
  });
  
  const data = await response.json();
  
  return (
    <SearchResults
      answer={data.answer}
      sources={data.sources}
      visual_content_note={data.visual_content_note}
    />
  );
};
```

---

## Cross-Platform Support

### Windows

**Default behavior:**
- Opens in default PDF viewer (Adobe, Edge, Chrome, etc.)
- Uses `start` command

**Page navigation:**
- Some viewers support `/A page=N` parameter
- Others open to last viewed page

### macOS

**Default behavior:**
- Opens in Preview.app or default viewer
- Uses `open` command

**Limitations:**
- Preview doesn't support command-line page navigation
- Opens to last viewed page or first page

**Alternative:**
- Detect if PDF Studio or Adobe is installed
- Use their CLI for page navigation

### Linux

**Viewers tested:**
- **Evince:** `evince --page-label=187 file.pdf` ✅
- **Okular:** `okular --page 187 file.pdf` ✅
- **xdg-open:** Opens default viewer (no page control)

**Fallback:**
- Try viewers in order: evince, okular, xdg-open
- First successful one is used

---

## Detection Patterns

### Figure References

Detected patterns:
- `Figure 8.3`
- `Fig. 2.1`
- `Diagram 5`
- `Table 3.2`
- `Chart 7`
- `Illustration 4.5`

### Visual Content Keywords

Text containing these triggers `has_visual_content`:
- "as shown in"
- "illustrated in"
- "depicted in"
- "see figure"
- "see diagram"
- "refer to chart"

### Example Detection

**Text:**
```
"The internal structure of a stratovolcano is shown in 
Figure 8.3. As illustrated, these composite volcanoes..."
```

**Detected:**
- ✅ `figures: ["Figure 8.3"]`
- ✅ `has_visual_content: true`
- ✅ Keywords: "shown in", "illustrated"

---

## User Experience Benefits

### Before (Text Only)

**User:** "Show me volcano diagram"

**System:** "Stratovolcanoes have layers of lava and ash..."

**User:** 🤔 "Where's the diagram?"  
**User:** Opens file browser  
**User:** Finds Earth Science.pdf  
**User:** Scrolls through 800 pages looking for diagram  
**User:** 😫 Gives up

### After (Open PDF Feature)

**User:** "Show me volcano diagram"

**System:** "Found Figure 8.3 on page 187... [Open PDF]"

**User:** 🖱️ Clicks button  
**System:** Opens PDF to page 187  
**User:** 😊 Sees diagram immediately

---

## Configuration Options

### Enable/Disable Per Source Type

```yaml
# database_config.yaml

sources:
  - name: "Books"
    type: "books"
    enable_open_pdf: true    # Enable for books
  
  - name: "Code"
    type: "code"
    enable_open_pdf: false   # Disable for code
```

### Page Tracking Accuracy

```python
# Adjust characters per page based on your PDFs
page_tracker = PDFPageTracker()
page_tracker.chars_per_page = 3500  # Default: 3000

# Dense technical books: 4000-5000
# Fiction/narrative: 2500-3000
```

### Figure Detection Sensitivity

```python
# Add custom patterns
CUSTOM_PATTERNS = [
    r'Image\s+(\d+\.?\d*)',
    r'Plate\s+(\d+\.?\d*)',
    r'Map\s+(\d+\.?\d*)',
]

EnhancedMetadataExtractor.FIGURE_PATTERNS.extend(CUSTOM_PATTERNS)
```

---

## Testing

### Test Cases

**1. PDF with figures:**
```python
# Test detection
text = "See Figure 8.3 for details"
metadata = EnhancedMetadataExtractor.create_enhanced_metadata(...)

assert "Figure 8.3" in metadata["figures"]
assert metadata["has_visual_content"] == True
```

**2. PDF without figures:**
```python
text = "This is plain text content"
metadata = EnhancedMetadataExtractor.create_enhanced_metadata(...)

assert "figures" not in metadata
assert "has_visual_content" not in metadata
```

**3. Open PDF action:**
```python
# Test API endpoint
response = client.post("/api/open-pdf", json={
    "file_path": "test.pdf",
    "page": 10
})

assert response.json()["success"] == True
```

### Manual Testing

1. **Build database with enhanced metadata:**
   ```bash
   python build_database.py
   ```

2. **Search for content with figures:**
   ```
   Query: "volcano diagram"
   ```

3. **Verify response includes:**
   - ✅ Page number
   - ✅ Figure reference
   - ✅ "Open PDF" action
   - ✅ Visual content note

4. **Click "Open PDF" button:**
   - ✅ PDF opens in default viewer
   - ✅ Opens to correct page (or close)

---

## Troubleshooting

### PDF doesn't open

**Check:**
1. File path is absolute and correct
2. File exists and is accessible
3. Default PDF viewer is installed
4. Backend has permissions to execute subprocess

**Debug:**
```python
# Add logging
import logging
logging.info(f"Opening: {file_path}")
logging.info(f"Platform: {platform.system()}")
```

### Wrong page opens

**Causes:**
- Page tracking is approximate (character-based)
- Some PDF viewers don't support page parameter
- PDF has non-standard structure

**Solutions:**
- Adjust `chars_per_page` for your content type
- Use PyMuPDF for exact page extraction
- Document limitation in UI

### Figures not detected

**Causes:**
- Non-standard naming ("See image below")
- Different language
- OCR text from scanned PDFs

**Solutions:**
- Add custom patterns to detection
- Review and expand keyword list
- Accept that detection won't be 100%

---

## Future Enhancements

### Phase 2: Better Page Accuracy

Use PyMuPDF instead of character counting:

```python
import fitz  # PyMuPDF

doc = fitz.open(pdf_path)
for page_num, page in enumerate(doc):
    text = page.get_text()
    # Exact page numbers!
```

### Phase 3: Extract & Cache Images

```python
# Extract figure when detected
if "Figure 8.3" in text:
    extract_figure_image(pdf_path, page_num, figure_num)
    cache_image_for_quick_preview()
```

### Phase 4: In-App PDF Viewer

```jsx
// Show PDF in modal instead of external viewer
<PDFViewer
  file={pdf_path}
  page={page_number}
  highlight={figure_bbox}
/>
```

---

## Summary

**What this feature does:**
- ✅ Detects figures/diagrams during indexing
- ✅ Tracks page numbers in metadata
- ✅ Provides "Open PDF" actions in search results
- ✅ Opens PDFs at relevant pages
- ✅ Works cross-platform

**What it doesn't do:**
- ❌ Extract or display images directly
- ❌ Guarantee exact page navigation (approximate)
- ❌ Work with encrypted/locked PDFs

**Trade-offs:**
- **Pro:** Simple, uses native PDF viewers, no image storage
- **Con:** Page navigation may be approximate on some systems

**Best for:**
- Reference books with figures
- Technical documentation
- Academic papers
- Illustrated textbooks

**Result:** Users can quickly find AND view visual content from their library with minimal friction.
