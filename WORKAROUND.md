# WORKAROUND: Build and Serve with Python

Since Windows is blocking Node.js dev server, we can **build the frontend** and serve it with Python's HTTP server instead.

---

## STEP 1: Build the Frontend (One-time)

```cmd
cd D:\Claude\Projects\scholars-terminal\frontend
npm run build
```

This creates a `dist` folder with static files.

---

## STEP 2: Start Backend (Terminal 1)

```cmd
cd D:\Claude\Projects\scholars-terminal\frontend\src
uvicorn Scholars_api:app --reload --host 127.0.0.1 --port 8000
```

---

## STEP 3: Serve Frontend with Python (Terminal 2)

```cmd
cd D:\Claude\Projects\scholars-terminal\frontend\dist
python -m http.server 8080
```

---

## STEP 4: Open Browser

Open: **http://localhost:8080**

---

## AUTOMATED LAUNCHER (After Building Once)

I'll create `launch_with_python.bat` that does this automatically.

---

## WHY THIS WORKS

- **Python HTTP server** isn't blocked by Windows security
- **Static files** don't need Vite dev server
- **Backend API** runs normally on port 8000
- **No Node.js network binding needed** for frontend

---

## LIMITATION

- You need to run `npm run build` after **any** code changes
- No hot-reload (have to rebuild and refresh browser)

---

## PERMANENT FIX STILL NEEDED

This is a **workaround**, not a fix. You still need to:

1. **Add Node.js to Windows Firewall exceptions**
2. **Add Node.js to IObit Malware Fighter exclusions** 
3. **Check Windows Defender settings**

---

## CHECKING WHAT'S BLOCKING

Run the diagnostic:

```cmd
cd D:\Claude\Projects\scholars-terminal
python diagnose_node_blocking.py
```

This will identify what's blocking Node.js.
