"""
Scholar's Terminal - Universal Database Builder
Builds your knowledge base from multiple configurable sources
"""

import os
import sys
import yaml
import json
import hashlib
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from tqdm import tqdm

import chromadb
from chromadb.config import Settings
import PyPDF2


# ============================================================
# CONFIGURATION LOADER
# ============================================================

class Config:
    """Load and validate configuration from YAML"""
    
    def __init__(self, config_path: str = "database_config.yaml"):
        with open(config_path, 'r') as f:
            self.data = yaml.safe_load(f)
        
        self.sources = [s for s in self.data['sources'] if s['enabled']]
        self.database = self.data['database']
        self.processing = self.data['processing']
        self.limits = self.data['limits']
        self.exclude_dirs = set(self.data['exclude_dirs'])
        self.exclude_files = set(self.data['exclude_files'])
        self.embedding = self.data['embedding']
        self.progress_config = self.data['progress']
    
    def validate(self):
        """Validate configuration"""
        errors = []
        
        # Check that at least one source is enabled
        if not self.sources:
            errors.append("No sources enabled! Enable at least one source in database_config.yaml")
        
        # Check that source paths exist
        for source in self.sources:
            path = Path(source['path'])
            if not path.exists():
                errors.append(f"Source path does not exist: {source['path']}")
        
        if errors:
            print("\n❌ Configuration Errors:")
            for error in errors:
                print(f"  - {error}")
            print("\nPlease fix database_config.yaml and try again.\n")
            sys.exit(1)
        
        print("✅ Configuration validated")


# ============================================================
# PROGRESS TRACKER
# ============================================================

class ProgressTracker:
    """Track indexing progress and allow resume"""
    
    def __init__(self, progress_file: str):
        self.progress_file = progress_file
        self.data = self._load()
    
    def _load(self) -> Dict:
        """Load existing progress"""
        if os.path.exists(self.progress_file):
            with open(self.progress_file, 'r') as f:
                return json.load(f)
        return {
            "processed_files": [],
            "failed_files": [],
            "start_time": datetime.now().isoformat(),
            "last_checkpoint": datetime.now().isoformat(),
            "stats": {
                "total_files": 0,
                "total_chunks": 0,
                "errors": 0
            },
            "sources": {}
        }
    
    def save(self):
        """Save progress"""
        self.data["last_checkpoint"] = datetime.now().isoformat()
        with open(self.progress_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def is_processed(self, file_path: str) -> bool:
        """Check if file already processed"""
        return file_path in self.data["processed_files"]
    
    def mark_processed(self, file_path: str):
        """Mark file as processed"""
        self.data["processed_files"].append(file_path)
    
    def mark_failed(self, file_path: str, error: str):
        """Mark file as failed"""
        self.data["failed_files"].append({
            "file": file_path,
            "error": error,
            "timestamp": datetime.now().isoformat()
        })
    
    def update_stats(self, **kwargs):
        """Update statistics"""
        for key, value in kwargs.items():
            if key in self.data["stats"]:
                self.data["stats"][key] += value
            else:
                self.data["stats"][key] = value
    
    def update_source_stats(self, source_name: str, files: int, chunks: int):
        """Update per-source statistics"""
        if source_name not in self.data["sources"]:
            self.data["sources"][source_name] = {"files": 0, "chunks": 0}
        
        self.data["sources"][source_name]["files"] += files
        self.data["sources"][source_name]["chunks"] += chunks


# ============================================================
# FILE PROCESSING
# ============================================================

def should_process_file(file_path: str, max_size_mb: int, exclude_dirs: set, exclude_files: set) -> bool:
    """Check if file should be processed"""
    path = Path(file_path)
    
    # Check file size
    try:
        size_mb = path.stat().st_size / (1024 * 1024)
        if size_mb > max_size_mb:
            logging.warning(f"Skipping large file ({size_mb:.1f}MB): {path.name}")
            return False
    except Exception:
        return False
    
    # Check directory exclusions
    for exclude_dir in exclude_dirs:
        if exclude_dir in path.parts:
            return False
    
    # Check filename exclusions
    if path.name in exclude_files:
        return False
    
    return True


def chunk_text(text: str, chunk_size: int, overlap: int, min_size: int) -> List[str]:
    """Split text into overlapping chunks"""
    if len(text) < min_size:
        return []
    
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        
        if len(chunk.strip()) >= min_size:
            chunks.append(chunk)
        
        start = end - overlap
    
    return chunks


def read_file_content(file_path: str) -> Optional[str]:
    """Read and return file content"""
    path = Path(file_path)
    suffix = path.suffix.lower()
    
    try:
        if suffix == '.pdf':
            text_parts = []
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    text_parts.append(page.extract_text())
            return '\n\n'.join(text_parts)
        else:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
    except Exception as e:
        logging.error(f"Error reading {path.name}: {e}")
        return None


def generate_file_id(file_path: str) -> str:
    """Generate unique ID for file"""
    return hashlib.md5(file_path.encode()).hexdigest()[:16]


def create_metadata(file_path: str, source_name: str, source_type: str, chunk_index: int) -> Dict:
    """Create metadata for a chunk"""
    path = Path(file_path)
    
    return {
        "source": str(file_path),
        "source_name": source_name,
        "source_type": source_type,
        "filename": path.name,
        "file_type": path.suffix.lower().lstrip('.'),
        "chunk_index": chunk_index,
        "timestamp": datetime.now().isoformat(),
    }


def process_file(file_path: str, source_name: str, source_type: str, collection, 
                 config: Config, progress: ProgressTracker) -> int:
    """Process a single file and add to collection"""
    
    if progress.is_processed(file_path):
        return 0
    
    content = read_file_content(file_path)
    if not content:
        progress.mark_failed(file_path, "Could not read content")
        return 0
    
    chunks = chunk_text(
        content, 
        config.processing['chunk_size'],
        config.processing['chunk_overlap'],
        config.processing['min_chunk_size']
    )
    
    if not chunks:
        progress.mark_failed(file_path, "No chunks generated")
        return 0
    
    # Limit chunks per file
    if len(chunks) > config.processing['max_chunks_per_file']:
        chunks = chunks[:config.processing['max_chunks_per_file']]
    
    file_id = generate_file_id(file_path)
    ids = [f"{source_type}_{file_id}_{i}" for i in range(len(chunks))]
    metadatas = [create_metadata(file_path, source_name, source_type, i) for i in range(len(chunks))]
    
    try:
        # Add in batches
        batch_size = config.processing['batch_size']
        for i in range(0, len(chunks), batch_size):
            batch_end = min(i + batch_size, len(chunks))
            collection.add(
                ids=ids[i:batch_end],
                documents=chunks[i:batch_end],
                metadatas=metadatas[i:batch_end]
            )
        
        progress.mark_processed(file_path)
        progress.update_stats(total_chunks=len(chunks))
        
        logging.info(f"✅ {Path(file_path).name}: {len(chunks)} chunks")
        return len(chunks)
    
    except Exception as e:
        logging.error(f"❌ Error adding {Path(file_path).name}: {e}")
        progress.mark_failed(file_path, str(e))
        return 0


# ============================================================
# DIRECTORY SCANNING
# ============================================================

def scan_directory(root_dir: str, extensions: List[str], config: Config) -> List[str]:
    """Recursively scan directory for matching files"""
    files = []
    
    for root, dirs, filenames in os.walk(root_dir):
        # Remove excluded directories
        dirs[:] = [d for d in dirs if d not in config.exclude_dirs]
        
        for filename in filenames:
            if Path(filename).suffix.lower() in extensions:
                file_path = os.path.join(root, filename)
                
                if should_process_file(
                    file_path, 
                    config.limits['max_file_size_mb'],
                    config.exclude_dirs,
                    config.exclude_files
                ):
                    files.append(file_path)
    
    return files


# ============================================================
# MAIN BUILD FUNCTION
# ============================================================

def main():
    """Main database building function"""
    
    print("=" * 70)
    print("Scholar's Terminal - Database Builder")
    print("=" * 70)
    print()
    
    # Load configuration
    print("📋 Loading configuration...")
    config = Config()
    config.validate()
    print()
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(config.progress_config['log_file'], encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Initialize progress tracking
    progress = ProgressTracker("database_build_progress.json")
    
    if progress.data["processed_files"]:
        print(f"📂 Resuming previous build:")
        print(f"   Already processed: {len(progress.data['processed_files'])} files")
        print(f"   Failed: {len(progress.data['failed_files'])} files")
        print()
    
    # Connect to ChromaDB
    print(f"🔌 Connecting to ChromaDB...")
    print(f"   Path: {config.database['path']}")
    
    db_path = Path(config.database['path'])
    db_path.mkdir(parents=True, exist_ok=True)
    
    client = chromadb.PersistentClient(
        path=str(db_path),
        settings=Settings(anonymized_telemetry=False)
    )
    
    try:
        collection = client.get_collection(config.database['collection_name'])
        print(f"   ✅ Using existing collection: {config.database['collection_name']}")
        print(f"   📊 Current documents: {collection.count()}")
    except:
        print(f"   ✅ Creating new collection: {config.database['collection_name']}")
        collection = client.create_collection(
            name=config.database['collection_name'],
            metadata={"description": "Scholar's Terminal Knowledge Base"}
        )
    
    print()
    
    # Process each enabled source
    total_files = 0
    total_chunks = 0
    
    for source in config.sources:
        print("=" * 70)
        print(f"📚 Processing: {source['name']}")
        print(f"   Path: {source['path']}")
        print(f"   Type: {source['type']}")
        print("=" * 70)
        
        # Scan for files
        print(f"\n🔍 Scanning for files...")
        files = scan_directory(source['path'], source['extensions'], config)
        print(f"   Found: {len(files)} files")
        
        if not files:
            print("   ⚠️  No files found - check path and extensions")
            continue
        
        print()
        
        # Process files
        source_chunks = 0
        for i, file_path in enumerate(tqdm(files, desc=f"Processing {source['name']}")):
            chunks = process_file(
                file_path, 
                source['name'],
                source['type'],
                collection, 
                config, 
                progress
            )
            source_chunks += chunks
            
            # Save progress periodically
            if (i + 1) % config.progress_config['save_every'] == 0:
                progress.save()
        
        # Update statistics
        progress.update_source_stats(source['name'], len(files), source_chunks)
        progress.save()
        
        total_files += len(files)
        total_chunks += source_chunks
        
        print(f"\n   ✅ {source['name']}: {len(files)} files → {source_chunks} chunks")
        print()
    
    # Final summary
    print("=" * 70)
    print("🎉 Build Complete!")
    print("=" * 70)
    print()
    
    for source_name, stats in progress.data['sources'].items():
        print(f"📚 {source_name}:")
        print(f"   Files: {stats['files']}")
        print(f"   Chunks: {stats['chunks']}")
    
    print()
    print(f"📊 Total Statistics:")
    print(f"   Files processed: {total_files}")
    print(f"   Chunks created: {total_chunks}")
    print(f"   Failed files: {len(progress.data['failed_files'])}")
    print()
    print(f"💾 Database:")
    print(f"   Location: {config.database['path']}")
    print(f"   Total documents: {collection.count()}")
    print()
    
    if progress.data['failed_files']:
        print("⚠️  Some files failed (see database_build.log for details)")
        print()
    
    print("=" * 70)
    print("Next step: Start Scholar's Terminal to search your knowledge base!")
    print("=" * 70)


if __name__ == "__main__":
    main()
