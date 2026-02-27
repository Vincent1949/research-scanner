# Scholar's Terminal - Database Setup

Build your personal knowledge base from your own content: books, code, research papers, or any text-based documents.

## Quick Start (3 Steps)

### 1. Configure Your Sources

Open `database_config.yaml` and edit the paths to point to your content:

```yaml
sources:
  - name: "My Books"
    path: "C:/Users/YourName/Books"  # ← Change this to your path
    type: "books"
    enabled: true
    extensions:
      - .pdf
      - .txt
```

### 2. Build the Database

**Windows:**
```bash
BUILD_DATABASE.bat
```

**Mac/Linux:**
```bash
chmod +x build_database.sh
./build_database.sh
```

### 3. Start Scholar's Terminal

```bash
python Scholars_api.py
```

Visit: http://localhost:8000

**That's it! You're ready to search your knowledge base.**

---

## What Can I Index?

You can index **any folder containing text-based content**:

### Common Use Cases

| What You Have | Configuration Example |
|---------------|----------------------|
| **📚 Book Collection** | Point to your books folder (PDFs, EPUBs, TXT) |
| **💻 Code Repositories** | Point to your GitHub folder (Python, JavaScript, etc.) |
| **📄 Research Papers** | Point to your papers folder (PDFs) |
| **📝 Personal Notes** | Point to your documents folder (Markdown, TXT) |
| **🗂️ All of the Above** | Add multiple sources! |

### Example Configuration

```yaml
sources:
  # Your book collection
  - name: "Technical Books"
    path: "D:/Books"
    type: "books"
    enabled: true
    extensions: [.pdf, .epub, .txt]
  
  # Your code projects
  - name: "GitHub Projects"
    path: "D:/GitHub"
    type: "code"
    enabled: true
    extensions: [.py, .js, .md]
  
  # Your research papers
  - name: "Research Papers"
    path: "D:/Research"
    type: "research"
    enabled: true
    extensions: [.pdf]
```

**You can add as many sources as you want!**

---

## Configuration Guide

### Required Settings

Only 3 things you **must** configure:

1. **name** - Friendly name for this source
2. **path** - Where your files are located
3. **enabled** - Set to `true` to index this source

### Optional Settings

Everything else has sensible defaults:

- **type**: Category (books, code, research, documents)
- **extensions**: Which file types to process
- **description**: Notes for yourself

### Path Examples

**Windows:**
```yaml
path: "C:/Users/YourName/Documents"
path: "D:\\Books"                    # Backslashes must be escaped
```

**Mac:**
```yaml
path: "/Users/yourname/Documents"
```

**Linux:**
```yaml
path: "/home/yourname/books"
```

---

## Common Scenarios

### Scenario 1: "I just want to index my books"

```yaml
sources:
  - name: "My Books"
    path: "/path/to/books"  # ← Your books folder
    type: "books"
    enabled: true
    extensions: [.pdf]
```

Run: `BUILD_DATABASE.bat` (Windows) or `./build_database.sh` (Mac/Linux)

### Scenario 2: "I have books in multiple folders"

```yaml
sources:
  - name: "Technical Books"
    path: "/path/to/tech/books"
    type: "books"
    enabled: true
    extensions: [.pdf]
  
  - name: "Fiction"
    path: "/path/to/fiction"
    type: "books"
    enabled: true
    extensions: [.pdf, .epub]
```

### Scenario 3: "I want to search my code AND books"

```yaml
sources:
  - name: "Books"
    path: "/path/to/books"
    type: "books"
    enabled: true
    extensions: [.pdf]
  
  - name: "Code"
    path: "/path/to/github"
    type: "code"
    enabled: true
    extensions: [.py, .js, .md]
```

### Scenario 4: "I want everything!"

```yaml
sources:
  - name: "Books"
    path: "/path/to/books"
    enabled: true
    extensions: [.pdf, .epub]
  
  - name: "Code"
    path: "/path/to/github"
    enabled: true
    extensions: [.py, .js, .ts, .md]
  
  - name: "Papers"
    path: "/path/to/research"
    enabled: true
    extensions: [.pdf]
  
  - name: "Notes"
    path: "/path/to/notes"
    enabled: true
    extensions: [.md, .txt]
```

---

## How Long Does It Take?

| Number of Files | Approximate Time |
|----------------|------------------|
| 100 books | ~5 minutes |
| 1,000 books | ~30-60 minutes |
| 10,000 books | ~2-4 hours |

**Progress is saved** - If interrupted, just run the builder again and it will resume where it left off.

---

## After Building

### Check the Build

Look for:
```
🎉 Build Complete!

📊 Total Statistics:
   Files processed: 1,234
   Chunks created: 567,890
   
💾 Database:
   Total documents: 567,890
```

### Start Scholar's Terminal

```bash
python Scholars_api.py
```

Visit: http://localhost:8000

### Start Searching!

Your knowledge base is ready. Ask questions about your content!

---

## Troubleshooting

### "No sources enabled!"

**Fix:** Set at least one source to `enabled: true` in `database_config.yaml`

### "Source path does not exist"

**Fix:** Check that the path exists and is spelled correctly

### "No files found"

**Fix:** 
- Check your file extensions match your actual files
- Verify files exist in that folder

### Build fails with "Module not found"

**Fix:** Install dependencies:
```bash
pip install pyyaml chromadb pypdf2 tqdm
```

---

## Advanced Options

For detailed configuration options, see: [DATABASE_SETUP_GUIDE.md](DATABASE_SETUP_GUIDE.md)

Covers:
- Chunking settings
- File size limits
- Directory exclusions
- Performance tuning
- Adding new file types

---

## Example: Complete Configuration

Here's a complete real-world example:

```yaml
sources:
  # Main book library
  - name: "Technical Books"
    path: "D:/Books/Technical"
    type: "books"
    enabled: true
    extensions: [.pdf, .epub]
    description: "Programming and computer science"
  
  # Code projects
  - name: "GitHub Projects"
    path: "D:/GitHub"
    type: "code"
    enabled: true
    extensions: [.py, .js, .ts, .md]
    description: "Personal coding projects"
  
  # Research papers
  - name: "Research Papers"
    path: "D:/Research/Papers"
    type: "research"
    enabled: false  # Disabled for now
    extensions: [.pdf]
    description: "Academic papers (enable later)"

# Database settings (defaults are fine)
database:
  path: "./data/vector_db"
  collection_name: "knowledge_base"

# Processing settings (defaults are fine)
processing:
  chunk_size: 1000
  chunk_overlap: 200
```

**Run:** `BUILD_DATABASE.bat` and you're done!

---

## Need Help?

1. Check [DATABASE_SETUP_GUIDE.md](DATABASE_SETUP_GUIDE.md) for detailed help
2. Look at `database_build.log` for errors
3. Open an issue on GitHub

---

## Summary

**Three simple steps:**

1. **Edit** `database_config.yaml` with your paths
2. **Run** `BUILD_DATABASE.bat` (or `.sh`)
3. **Start** `Scholars_api.py`

**That's it!** Your personal knowledge base is ready to use.
