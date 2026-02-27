/**
 * Scholar's Terminal - Open PDF Component
 * 
 * React component that handles "Open in PDF" actions from search results
 * Works cross-platform (Windows, Mac, Linux)
 */

import React from 'react';
import { ExternalLink, FileText, Image } from 'lucide-react';

// ============================================================
// MAIN COMPONENT
// ============================================================

export const SourceWithAction = ({ source }) => {
  const handleOpenPDF = async (action) => {
    try {
      // Call backend API to open PDF
      const response = await fetch('/api/open-pdf', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          file_path: action.file_path,
          page: action.page
        })
      });
      
      if (!response.ok) {
        throw new Error('Failed to open PDF');
      }
      
      const result = await response.json();
      
      if (!result.success) {
        alert(`Could not open PDF: ${result.error}`);
      }
    } catch (error) {
      console.error('Error opening PDF:', error);
      alert('Failed to open PDF viewer');
    }
  };

  return (
    <div className="source-card border rounded-lg p-4 mb-3 bg-white shadow-sm">
      {/* Source Header */}
      <div className="flex items-start justify-between mb-2">
        <div className="flex items-center gap-2">
          <FileText className="w-5 h-5 text-blue-600" />
          <span className="font-semibold text-gray-900">
            {source.filename}
          </span>
        </div>
        
        {/* Relevance Score */}
        <span className="text-sm text-gray-500">
          {(source.relevance * 100).toFixed(0)}% relevant
        </span>
      </div>

      {/* Page Number & Figures */}
      <div className="flex gap-4 mb-3 text-sm text-gray-600">
        {source.page_number && (
          <span>Page {source.page_number}</span>
        )}
        
        {source.figures && source.figures.length > 0 && (
          <div className="flex items-center gap-1">
            <Image className="w-4 h-4" />
            <span>{source.figures.join(', ')}</span>
          </div>
        )}
      </div>

      {/* Visual Content Indicator */}
      {source.has_visual && (
        <div className="mb-3 p-2 bg-blue-50 rounded text-sm text-blue-800">
          📊 This source contains diagrams or figures
        </div>
      )}

      {/* Open PDF Action */}
      {source.action && source.action.type === 'open_pdf' && (
        <button
          onClick={() => handleOpenPDF(source.action)}
          className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
        >
          <ExternalLink className="w-4 h-4" />
          {source.action.label}
        </button>
      )}
    </div>
  );
};

// ============================================================
// SEARCH RESULTS COMPONENT
// ============================================================

export const SearchResults = ({ answer, sources, visual_content_note }) => {
  return (
    <div className="search-results">
      {/* Answer Section */}
      <div className="answer-section mb-6 p-4 bg-gray-50 rounded-lg">
        <h3 className="text-lg font-semibold mb-2">Answer</h3>
        <p className="text-gray-800 whitespace-pre-wrap">{answer}</p>
      </div>

      {/* Visual Content Note */}
      {visual_content_note && (
        <div className="mb-4 p-3 bg-yellow-50 border-l-4 border-yellow-400 text-yellow-800">
          <p className="text-sm">{visual_content_note}</p>
        </div>
      )}

      {/* Sources Section */}
      <div className="sources-section">
        <h3 className="text-lg font-semibold mb-3">
          Sources ({sources.length})
        </h3>
        
        {sources.map((source, index) => (
          <SourceWithAction key={index} source={source} />
        ))}
      </div>
    </div>
  );
};

// ============================================================
// BACKEND API ENDPOINT (FastAPI)
// ============================================================

/**
 * Python Backend API
 * 
 * Add this to your Scholars_api.py:
 */

/*
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import subprocess
import platform
import os

router = APIRouter()

class OpenPDFRequest(BaseModel):
    file_path: str
    page: int

@router.post("/api/open-pdf")
async def open_pdf(request: OpenPDFRequest):
    """Open PDF file at specified page"""
    
    try:
        # Verify file exists
        if not os.path.exists(request.file_path):
            raise HTTPException(status_code=404, detail="PDF file not found")
        
        system = platform.system()
        
        if system == "Windows":
            # Windows: Use default PDF viewer
            # For Adobe Reader, can specify page with /A "page=N"
            subprocess.Popen([
                'start', '',
                request.file_path,
                f'/A', f'page={request.page}'
            ], shell=True)
            
        elif system == "Darwin":  # macOS
            # macOS: Use Preview or default PDF viewer
            # Note: Preview doesn't support direct page opening via command line
            # Opens to last viewed page or first page
            subprocess.Popen(['open', request.file_path])
            
        elif system == "Linux":
            # Linux: Try common PDF viewers
            viewers = ['evince', 'okular', 'xdg-open']
            
            for viewer in viewers:
                try:
                    if viewer == 'evince':
                        # Evince supports page number
                        subprocess.Popen([viewer, f'--page-label={request.page}', request.file_path])
                        break
                    elif viewer == 'okular':
                        # Okular supports page number
                        subprocess.Popen([viewer, f'--page {request.page}', request.file_path])
                        break
                    else:
                        subprocess.Popen([viewer, request.file_path])
                        break
                except FileNotFoundError:
                    continue
            else:
                raise Exception("No PDF viewer found")
        
        return {
            "success": True,
            "message": f"Opened {os.path.basename(request.file_path)} at page {request.page}"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
*/

// ============================================================
// USAGE EXAMPLE
// ============================================================

/*
// In your main App component:

import { SearchResults } from './components/SourceWithAction';

function App() {
  const [searchResult, setSearchResult] = useState(null);

  const handleSearch = async (query) => {
    const response = await fetch('/api/search', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query })
    });
    
    const data = await response.json();
    setSearchResult(data);
  };

  return (
    <div className="app">
      {searchResult && (
        <SearchResults
          answer={searchResult.answer}
          sources={searchResult.sources}
          visual_content_note={searchResult.visual_content_note}
        />
      )}
    </div>
  );
}
*/

export default SearchResults;
