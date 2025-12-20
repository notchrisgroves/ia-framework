# Python Security - Common Vulnerabilities and Prevention

**Language-specific security guide for Python code reviews**

This document covers vulnerabilities specific to Python, WHY they exist in Python, and HOW to prevent them properly.

---

## Python Version Context

**Current Python:** 3.11+ (as of 2025)

**Important:** Always verify Python version being used in the codebase. Some vulnerabilities/mitigations are version-specific.

---

## 1. Pickle Deserialization → Arbitrary Code Execution

### WHAT
Deserializing untrusted data with `pickle` allows arbitrary code execution.

### WHY (Root Cause)
Python's pickle module reconstructs Python objects by calling special methods like `__reduce__()` during deserialization. An attacker can craft a malicious pickle payload that executes arbitrary commands when unpickled.

**How pickle works:**
1. Serializes Python objects to bytecode
2. During deserialization, calls `__reduce__()` to reconstruct objects
3. `__reduce__()` can return a callable + arguments → arbitrary code execution

### VULNERABLE CODE
```python
import pickle
import requests

# Receive data from API
response = requests.get('https://api.example.com/data')
data = pickle.loads(response.content)  # DANGEROUS!
```

**WHY IT'S VULNERABLE:**
Attacker controls the pickle payload → can craft `__reduce__()` to execute:
```python
import os
os.system('rm -rf /')  # Executed during unpickling
```

### SECURE CODE
```python
import json
import requests

# Use JSON for untrusted data
response = requests.get('https://api.example.com/data')
data = json.loads(response.text)  # Safe - only data structures
```

**WHY IT'S SECURE:**
- JSON only deserializes primitive types (dict, list, str, int, float, bool, None)
- No code execution possible
- Type-safe deserialization

**WHEN YOU MUST USE PICKLE:**
Only for trusted, internal data (never user input or external APIs):
```python
import pickle
import hmac
import hashlib

# Sign pickle data
SECRET_KEY = os.getenv('PICKLE_SECRET_KEY')
pickled_data = pickle.dumps(my_object)
signature = hmac.new(SECRET_KEY.encode(), pickled_data, hashlib.sha256).hexdigest()

# Verify signature before unpickling
received_signature = request.headers.get('X-Pickle-Signature')
if not hmac.compare_digest(signature, received_signature):
    raise ValueError("Invalid signature")
data = pickle.loads(pickled_data)
```

**CWE:** CWE-502 (Deserialization of Untrusted Data)

---

## 2. SQL Injection via String Formatting

### WHAT
Building SQL queries with f-strings or `.format()` allows SQL injection.

### WHY (Root Cause)
Python's string formatting concatenates user input directly into SQL strings without escaping. The database cannot distinguish between SQL code and data.

### VULNERABLE CODE
```python
import sqlite3

username = request.form['username']
password = request.form['password']

# VULNERABLE - f-string concatenation
query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
cursor.execute(query)
```

**WHY IT'S VULNERABLE:**
Attacker input: `username = "admin' --"`
Resulting query: `SELECT * FROM users WHERE username = 'admin' --' AND password = '...'`
The `--` comments out the password check → authentication bypass.

### SECURE CODE
```python
import sqlite3

username = request.form['username']
password = request.form['password']

# SECURE - Parameterized query
query = "SELECT * FROM users WHERE username = ? AND password = ?"
cursor.execute(query, (username, password))
```

**WHY IT'S SECURE:**
- Database treats `?` placeholders as data, not SQL code
- Input is automatically escaped by the database driver
- Attacker cannot inject SQL syntax

**FOR DIFFERENT DATABASES:**
```python
# PostgreSQL (psycopg2)
cursor.execute("SELECT * FROM users WHERE username = %s", (username,))

# MySQL (mysql-connector)
cursor.execute("SELECT * FROM users WHERE username = %s", (username,))

# SQLAlchemy (ORM - safest)
user = session.query(User).filter_by(username=username).first()
```

**CWE:** CWE-89 (SQL Injection)

---

## 3. Command Injection via os.system / subprocess

### WHAT
Executing shell commands with user input allows command injection.

### WHY (Root Cause)
`os.system()` and `subprocess.call(..., shell=True)` pass the entire string to the shell, which interprets shell metacharacters (`;`, `|`, `&`, etc.). Attacker can chain commands.

### VULNERABLE CODE
```python
import os

filename = request.args.get('file')
os.system(f'cat {filename}')  # DANGEROUS!
```

**WHY IT'S VULNERABLE:**
Attacker input: `file=test.txt; rm -rf /`
Executed command: `cat test.txt; rm -rf /`
The semicolon chains a second command.

### SECURE CODE (Option 1: Avoid Shell)
```python
import subprocess

filename = request.args.get('file')

# Pass as list (no shell interpretation)
result = subprocess.run(['cat', filename], capture_output=True, check=True)
```

**WHY IT'S SECURE:**
- Arguments passed as list → no shell interpretation
- Filename treated as literal string, not parsed for metacharacters
- Even if filename = `"test.txt; rm -rf /"`, it's treated as a literal filename

### SECURE CODE (Option 2: Whitelist + Validation)
```python
import os
import re

filename = request.args.get('file')

# Whitelist allowed characters
if not re.match(r'^[a-zA-Z0-9_.-]+$', filename):
    raise ValueError("Invalid filename")

# Ensure file exists and is in allowed directory
allowed_dir = '/var/data/'
filepath = os.path.join(allowed_dir, filename)
if not os.path.realpath(filepath).startswith(allowed_dir):
    raise ValueError("Path traversal detected")

# Now safe to use
with open(filepath, 'r') as f:
    content = f.read()
```

**WHY IT'S SECURE:**
- Whitelist validation prevents metacharacters
- Path traversal check prevents `../` attacks
- No shell execution at all

**CWE:** CWE-78 (OS Command Injection)

---

## 4. Path Traversal

### WHAT
Unsanitized file paths allow access to files outside intended directory.

### WHY (Root Cause)
Python's `open()` directly uses the provided path without validation. `../` sequences allow traversing up directories.

### VULNERABLE CODE
```python
import os

filename = request.args.get('file')
filepath = os.path.join('/var/uploads/', filename)

with open(filepath, 'r') as f:
    content = f.read()
```

**WHY IT'S VULNERABLE:**
Attacker input: `file=../../../etc/passwd`
Resulting path: `/var/uploads/../../../etc/passwd` → resolves to `/etc/passwd`

### SECURE CODE
```python
import os

filename = request.args.get('file')
base_dir = '/var/uploads/'

# Resolve absolute path
filepath = os.path.abspath(os.path.join(base_dir, filename))

# Verify it's still within base directory
if not filepath.startswith(os.path.abspath(base_dir)):
    raise ValueError("Path traversal detected")

with open(filepath, 'r') as f:
    content = f.read()
```

**WHY IT'S SECURE:**
- `os.path.abspath()` resolves `..` sequences
- `startswith()` check ensures path is within allowed directory
- Any traversal attempt is detected and blocked

**CWE:** CWE-22 (Path Traversal)

---

## 5. Eval/Exec with User Input

### WHAT
Using `eval()` or `exec()` with user input allows arbitrary code execution.

### WHY (Root Cause)
`eval()` and `exec()` execute Python code as strings. User input = attacker-controlled Python code.

### VULNERABLE CODE
```python
# Calculator app
expression = request.form['expression']
result = eval(expression)  # EXTREMELY DANGEROUS!
```

**WHY IT'S VULNERABLE:**
Attacker input: `__import__('os').system('rm -rf /')`
This imports os module and executes shell commands.

### SECURE CODE (Option 1: ast.literal_eval)
```python
import ast

expression = request.form['expression']
try:
    # Only evaluates literals (numbers, strings, lists, dicts)
    result = ast.literal_eval(expression)
except (ValueError, SyntaxError):
    raise ValueError("Invalid expression")
```

**WHY IT'S SECURE:**
- `ast.literal_eval()` only evaluates Python literals
- No function calls, imports, or code execution possible
- Safe for deserializing simple data structures

### SECURE CODE (Option 2: Safe Math Library)
```python
import numexpr

expression = request.form['expression']
# Only evaluates math expressions
result = numexpr.evaluate(expression)
```

**WHY IT'S SECURE:**
- `numexpr` only supports mathematical operations
- No Python code execution
- Sandboxed evaluation

**CWE:** CWE-94 (Code Injection)

---

## 6. Weak Cryptography - MD5/SHA1 for Passwords

### WHAT
Using MD5 or SHA-1 for password hashing is insecure.

### WHY (Root Cause)
- **MD5/SHA-1 are too fast:** Attackers can try billions of hashes per second
- **No built-in salt:** Rainbow tables can crack unsalted hashes instantly
- **Designed for speed, not security:** Meant for checksums, not passwords

### VULNERABLE CODE
```python
import hashlib

password = request.form['password']
password_hash = hashlib.md5(password.encode()).hexdigest()
# Store password_hash in database
```

**WHY IT'S VULNERABLE:**
- MD5 can compute ~1 billion hashes/second on GPU
- No salt → rainbow tables effective
- Same password always produces same hash

### SECURE CODE
```python
import bcrypt

password = request.form['password']

# Hash with bcrypt (automatic salt + slow)
password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12))
# Store password_hash in database

# Verify later
if bcrypt.checkpw(entered_password.encode(), stored_hash):
    print("Password correct")
```

**WHY IT'S SECURE:**
- **Slow by design:** ~100ms per hash (GPU-resistant)
- **Automatic salt:** Each hash is unique even for same password
- **Adjustable work factor:** Can increase rounds as hardware improves

**ALTERNATIVES:**
```python
# Argon2 (winner of Password Hashing Competition)
from argon2 import PasswordHasher
ph = PasswordHasher()
password_hash = ph.hash(password)
ph.verify(password_hash, password)

# scrypt (also acceptable)
import hashlib
password_hash = hashlib.scrypt(password.encode(), salt=salt, n=2**14, r=8, p=1)
```

**CWE:** CWE-327 (Use of Broken Crypto), CWE-916 (Weak Password Hashing)

---

## 7. Insecure Random - random vs secrets

### WHAT
Using `random` module for security tokens is insecure.

### WHY (Root Cause)
- `random` uses Mersenne Twister algorithm (predictable)
- Given a few outputs, attacker can predict future values
- NOT cryptographically secure

### VULNERABLE CODE
```python
import random

# Generate password reset token
reset_token = str(random.randint(100000, 999999))
# Send reset_token to user
```

**WHY IT'S VULNERABLE:**
- Mersenne Twister is deterministic (same seed → same sequence)
- Attacker can predict tokens if they observe a few
- Only ~6 digits → brute force possible

### SECURE CODE
```python
import secrets

# Generate cryptographically secure token
reset_token = secrets.token_urlsafe(32)  # 32 bytes = 256 bits
# Send reset_token to user
```

**WHY IT'S SECURE:**
- `secrets` uses OS-level cryptographic RNG
- Unpredictable even with access to previous tokens
- 256 bits of entropy → brute force infeasible

**FOR DIFFERENT USE CASES:**
```python
import secrets

# URL-safe token
token = secrets.token_urlsafe(32)

# Hex token
token = secrets.token_hex(32)

# Random choice from list (secure)
password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(16))

# Random number in range (secure)
random_num = secrets.randbelow(100)  # 0-99
```

**CWE:** CWE-330 (Use of Insufficiently Random Values)

---

## 8. YAML Deserialization (PyYAML)

### WHAT
Using `yaml.load()` without SafeLoader allows code execution.

### WHY (Root Cause)
PyYAML's default loader can instantiate arbitrary Python objects, including executing code via `!!python/object/apply`.

### VULNERABLE CODE
```python
import yaml

config = request.files['config'].read()
data = yaml.load(config)  # DANGEROUS with Loader=FullLoader (default < 5.1)
```

**WHY IT'S VULNERABLE:**
Attacker uploads config file:
```yaml
!!python/object/apply:os.system
args: ['rm -rf /']
```
This executes `os.system('rm -rf /')` during parsing.

### SECURE CODE
```python
import yaml

config = request.files['config'].read()
data = yaml.safe_load(config)  # Safe - only standard types
```

**WHY IT'S SECURE:**
- `safe_load()` only constructs simple Python objects (dict, list, str, int, etc.)
- No arbitrary object instantiation
- No code execution possible

**CWE:** CWE-502 (Deserialization of Untrusted Data)

---

## 9. Flask Debug Mode in Production

### WHAT
Running Flask with `debug=True` in production exposes sensitive information.

### WHY (Root Cause)
Debug mode:
- Shows detailed stack traces (reveals code structure)
- Enables Werkzeug debugger (allows code execution via PIN)
- Reloads code automatically (performance impact)

### VULNERABLE CODE
```python
from flask import Flask

app = Flask(__name__)
app.debug = True  # NEVER in production!

if __name__ == '__main__':
    app.run()
```

**WHY IT'S VULNERABLE:**
- Stack traces reveal file paths, variable values, SQL queries
- Werkzeug debugger console allows executing Python code
- Information leakage aids further attacks

### SECURE CODE
```python
from flask import Flask
import os

app = Flask(__name__)
app.debug = os.getenv('FLASK_ENV') == 'development'

if __name__ == '__main__':
    app.run()
```

**WHY IT'S SECURE:**
- Debug mode only enabled in development environment
- Production errors logged without exposing details to users
- No interactive debugger exposed

**BETTER: Use Environment Variables**
```python
# .env (development)
FLASK_ENV=development
FLASK_DEBUG=1

# .env.production
FLASK_ENV=production
FLASK_DEBUG=0
```

**CWE:** CWE-209 (Information Exposure Through Error Message)

---

## 10. Django - Raw SQL Queries

### WHAT
Using `raw()` or `extra()` with user input allows SQL injection.

### WHY (Root Cause)
Even though Django ORM is safe, `raw()` bypasses ORM protections and concatenates SQL strings.

### VULNERABLE CODE
```python
from django.db import connection

search = request.GET.get('search')
cursor = connection.cursor()
cursor.execute(f"SELECT * FROM products WHERE name LIKE '%{search}%'")
```

**WHY IT'S VULNERABLE:**
Same as raw SQL injection - user input concatenated into SQL string.

### SECURE CODE
```python
from myapp.models import Product

search = request.GET.get('search')

# Use Django ORM (parameterized automatically)
products = Product.objects.filter(name__icontains=search)
```

**WHY IT'S SECURE:**
- Django ORM automatically parameterizes queries
- `__icontains` uses safe SQL LIKE with parameters
- No SQL injection possible

**IF YOU MUST USE RAW SQL:**
```python
from django.db import connection

search = request.GET.get('search')
cursor = connection.cursor()
cursor.execute("SELECT * FROM products WHERE name LIKE %s", [f'%{search}%'])
```

**CWE:** CWE-89 (SQL Injection)

---

## Python-Specific Best Practices

### 1. Use Type Hints (Python 3.5+)
```python
def process_user(user_id: int) -> dict:
    # Type hints help catch bugs early
    pass
```

### 2. Use Context Managers for Resources
```python
# Ensures file is closed even if exception occurs
with open('file.txt', 'r') as f:
    content = f.read()
```

### 3. Validate Input Types
```python
def process_age(age):
    if not isinstance(age, int):
        raise TypeError("Age must be integer")
    if age < 0 or age > 150:
        raise ValueError("Invalid age")
```

### 4. Use Environment Variables for Secrets
```python
import os

# NEVER hardcode
SECRET_KEY = os.getenv('SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("SECRET_KEY not set")
```

### 5. Keep Dependencies Updated
```bash
# Check for outdated packages
pip list --outdated

# Update packages
pip install --upgrade package_name

# Use safety to check for known vulnerabilities
pip install safety
safety check
```

---

## Dynamic Lookup for Current Best Practices

**Before reviewing Python code, always:**

1. **Check Python version:**
   ```python
   import sys
   print(sys.version)
   ```

2. **Look up current security advisories:**
   - Python Security Advisories: https://www.python.org/news/security/
   - PyPI Advisory Database: https://github.com/pypa/advisory-database

3. **Review framework-specific security guides:**
   - Django: https://docs.djangoproject.com/en/stable/topics/security/
   - Flask: https://flask.palletsprojects.com/en/stable/security/
   - FastAPI: https://fastapi.tiangolo.com/tutorial/security/

4. **Use WebSearch for language-specific issues:**
   ```
   "Python 3.11 security best practices"
   "Python [framework] security vulnerabilities 2025"
   ```

---

**Version:** 2.0
**Last Updated:** 2025-12-02
**Python Version:** 3.11+
**Focus:** WHAT vulnerabilities, WHY they exist, HOW to prevent them properly
