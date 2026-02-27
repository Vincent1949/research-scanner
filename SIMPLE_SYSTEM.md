# SIMPLE VIABLE SYSTEM - README

## What This Does

**One script. One command. One database.**

### BUILD_DATABASE.bat

This script will:
- ✅ Scan D:\Books for PDF, TXT, and MD files
- ✅ Process ~9,000 books
- ✅ Create chunks with metadata
- ✅ Build ChromaDB database at: `D:\Claude\Projects\scholars-terminal\data\vector_db`
- ✅ Save progress (can resume if interrupted)
- ✅ Log everything to `reindex.log`

### What It Skips (For Simplicity)

- ❌ EPUB files (no processing code - would need additional library)
- ❌ GitHub repositories (disabled - too many files, can add later)
- ❌ Email/Newsletters (separate system in D:\Newsletter_Processing)

---

## How to Use

### First Time (Fresh Build)

1. **Delete old database** (if starting fresh):
   ```
   Delete: D:\Claude\Projects\scholars-terminal\data\vector_db
   ```

2. **Run the builder**:
   ```
   Double-click: BUILD_DATABASE.bat
   ```

3. **Wait** (could take 1-2 hours for 9,000 books)

4. **Done!**

### Resume After Interruption

- Just run `BUILD_DATABASE.bat` again
- It will skip already-processed files
- Progress is saved in `reindex_progress.json`

---

## Expected Results

**After completion:**
- Database size: ~70-100 GB
- Total chunks: ~13 million
- Files processed: ~9,000
- Success rate: ~99.8%

**Some errors are normal:**
- 10-20 PDF files may fail (corrupt/encrypted)
- This is fine - 99%+ success rate

---

## Troubleshooting

### "No module named ebooklib"
- EPUB processing was disabled, this shouldn't happen
- If it does, run: `pip install ebooklib`

### "Database is locked"
- Close Scholar's Terminal application
- Kill any Python processes
- Try again

### Build is very slow
- This is normal for 9,000 books
- Can take 1-2 hours
- Progress is logged every 100 files

---

## What's Next?

After the database is built:

### Test It Works
```batch
cd D:\Claude\Projects\scholars-terminal
python Scholars_api.py
```

Visit: http://localhost:8000

### Add GitHub Later (Optional)
Edit `reindex_config.py`:
```python
INDEX_GITHUB = True
```
Run `BUILD_DATABASE.bat` again

### Add Emails Later (Optional)
Use the separate system:
```batch
cd D:\Newsletter_Processing
python master_pipeline.py
```

---

## Files Changed

### Fixed Configuration
- `reindex_config.py`
  - Database path: `vector_db` (not `vector_db_new`)
  - EPUBs: Disabled (no processing code)
  - GitHub: Disabled (too complex for v1)

### New Files
- `BUILD_DATABASE.bat` - Simple launcher
- `SIMPLE_SYSTEM.md` - This file

---

## Philosophy

**"Simple Viable System" means:**
- ✅ One command to build database
- ✅ Works with your existing books
- ✅ Can run unattended
- ✅ Saves progress
- ✅ Clear success/failure indicators

**Not:**
- ❌ Trying to do everything at once
- ❌ Complex multi-stage pipelines
- ❌ Fragile dependencies
- ❌ Mysterious failures

---

**Just run BUILD_DATABASE.bat and you're done.**
