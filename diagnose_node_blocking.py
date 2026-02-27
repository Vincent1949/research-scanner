"""
Node.js Port Binding Diagnostic
Checks what's preventing Node.js from binding to ports
"""

import subprocess
import sys

print("\n" + "="*60)
print("NODE.JS PORT BINDING DIAGNOSTIC")
print("="*60 + "\n")

tests = [
    {
        "name": "Test 1: Node.js Basic Port Binding",
        "command": 'node -e "require(\'http\').createServer().listen(8080, \'127.0.0.1\', () => console.log(\'SUCCESS\'))"',
        "timeout": 5
    },
    {
        "name": "Test 2: Check Windows Firewall Rules for Node.js",
        "command": 'netsh advfirewall firewall show rule name=all | findstr /i "node"',
        "timeout": 5
    },
    {
        "name": "Test 3: Check if port 8080 is in use",
        "command": 'netstat -ano | findstr ":8080"',
        "timeout": 3
    },
    {
        "name": "Test 4: Test Python HTTP server (Alternative)",
        "command": 'python -c "import http.server; print(\'Python HTTP available\')"',
        "timeout": 2
    }
]

print("Running diagnostic tests...\n")

for i, test in enumerate(tests, 1):
    print(f"\n[{i}/{len(tests)}] {test['name']}")
    print("-" * 60)
    
    try:
        result = subprocess.run(
            test['command'],
            shell=True,
            capture_output=True,
            text=True,
            timeout=test['timeout']
        )
        
        if result.stdout.strip():
            print(f"Output:\n{result.stdout}")
        else:
            print("No output (may be normal)")
            
        if result.stderr.strip():
            print(f"Errors:\n{result.stderr}")
            
        if result.returncode == 0:
            print("[OK] Test passed")
        else:
            print(f"[FAILED] Return code: {result.returncode}")
            
    except subprocess.TimeoutExpired:
        print("[TIMEOUT] Test took too long")
    except Exception as e:
        print(f"[ERROR] {e}")

print("\n" + "="*60)
print("DIAGNOSTIC COMPLETE")
print("="*60)
print("\nLIKELY CAUSES:")
print("  1. Windows Firewall blocking Node.js")
print("  2. IObit Malware Fighter blocking Node.js")
print("  3. Antivirus software interference")
print("  4. Windows Defender SmartScreen")
print("\nRECOMMENDED ACTIONS:")
print("  1. Add Node.js to Windows Firewall exceptions")
print("  2. Add Node.js to IObit exclusions")
print("  3. Try the Python HTTP server workaround (see WORKAROUND.md)")
print()
