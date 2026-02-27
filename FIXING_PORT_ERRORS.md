# FIXING PORT PERMISSION ERRORS - Windows

## The Problem
You're getting `EACCES: permission denied` errors when Node.js tries to bind to ports.
This is a **Windows security/firewall issue**, not a port conflict.

---

## SOLUTION 1: Run as Administrator ⭐ RECOMMENDED

This is the quickest fix:

1. **Open Command Prompt as Administrator**:
   - Press `Windows + X`
   - Click "Command Prompt (Admin)" or "Windows PowerShell (Admin)"

2. **Navigate and start the frontend**:
```cmd
cd D:\Claude\Projects\scholars-terminal\frontend
npm run dev
```

3. **The frontend should now start on port 8080**:
   - Open browser: http://localhost:8080

---

## SOLUTION 2: Add Windows Firewall Rule

Create a permanent firewall rule for Node.js:

### Step 1: Open Windows Firewall
```
Control Panel → System and Security → Windows Defender Firewall → Advanced Settings
```

### Step 2: Create Inbound Rule
1. Click "Inbound Rules" in left panel
2. Click "New Rule..." in right panel
3. Select "Program" → Next
4. Browse to: `C:\Program Files\nodejs\node.exe`
5. Select "Allow the connection" → Next
6. Check all boxes (Domain, Private, Public) → Next
7. Name: "Node.js Development Server"
8. Finish

### Step 3: Test
```cmd
cd D:\Claude\Projects\scholars-terminal\frontend
npm run dev
```

---

## SOLUTION 3: Check IObit Malware Fighter

You mentioned IObit before - it may be blocking Node.js:

1. Open IObit Malware Fighter
2. Go to Settings → Exclusions
3. Add: `C:\Program Files\nodejs\node.exe`
4. Restart and try `npm run dev`

---

## SOLUTION 4: Temporarily Disable Windows Firewall

**⚠️ Only for testing - remember to re-enable!**

### In Administrator PowerShell:
```powershell
# Disable firewall
Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled False

# Try starting the dev server
cd D:\Claude\Projects\scholars-terminal\frontend
npm run dev

# IMPORTANT: Re-enable firewall after testing
Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True
```

---

## SOLUTION 5: Use a Different Port Range

Some ports are less restricted. I've changed your config to port **8080**.

If 8080 still fails, try these in `vite.config.js`:
- Port 3000
- Port 8000
- Port 9000

Edit this file: `D:\Claude\Projects\scholars-terminal\frontend\vite.config.js`
```javascript
server: {
  port: 3000,  // Try different ports
  host: 'localhost',
  strictPort: false,
}
```

---

## CURRENT CONFIGURATION

✅ **Frontend**: Port 8080 (updated)
✅ **Backend**: Port 8000
✅ **API CORS**: Updated to allow port 8080

---

## QUICK START AFTER FIX

### Option A: Use the launcher (needs both admin terminals):
```cmd
launch_scholars_terminal_multi_db.bat
```

### Option B: Manual start (in Admin terminals):

**Terminal 1 (Backend):**
```cmd
cd D:\Claude\Projects\scholars-terminal\frontend\src
uvicorn Scholars_api:app --reload --host 127.0.0.1 --port 8000
```

**Terminal 2 (Frontend):**
```cmd
cd D:\Claude\Projects\scholars-terminal\frontend
npm run dev
```

**Then open**: http://localhost:8080

---

## VERIFICATION

After applying a fix, verify it works:

1. **Check if Node can bind to ports**:
```cmd
node -e "require('http').createServer().listen(8080, () => console.log('Success on 8080'))"
```

2. **If successful, you'll see**: "Success on 8080"

3. **If it fails**: Try the next solution above

---

## WHY IS THIS HAPPENING?

Windows security is blocking Node.js from binding to network ports. Common causes:

1. **Windows Firewall** - Blocking Node.js
2. **Antivirus** - IObit, Norton, McAfee, etc.
3. **User Permissions** - Need administrator rights
4. **Reserved Ports** - Some ports need special permissions

---

## RECOMMENDED ORDER

Try these in order:

1. ✅ **Run as Administrator** (quickest)
2. ✅ **Add Firewall Rule** (permanent fix)
3. ✅ **Check IObit/Antivirus**
4. ⚠️ **Disable Firewall temporarily** (testing only)

---

## AFTER YOU GET IT WORKING

Once the frontend starts successfully:

1. **Note which solution worked**
2. **Keep using that method**
3. **Or make it permanent** (firewall rule)

---

**Current Status**: Port changed to 8080, CORS updated, ready to test!
