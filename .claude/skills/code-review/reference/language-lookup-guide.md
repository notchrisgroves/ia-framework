# Language-Specific Security Review - Dynamic Lookup Guide

**How to review code in ANY language using dynamic lookup**

Secure coding standards are **entirely language-specific**. This guide teaches you how to dynamically look up and apply the right standards for any language.

---

## Core Principle

**❌ WRONG:** Apply generic security checklist to all languages

**✅ RIGHT:**
1. Identify language + version
2. Look up current security standards for that specific language
3. Understand WHY vulnerabilities exist in that language
4. Apply language-specific prevention patterns

---

## Step-by-Step Language Review Process

### Step 1: Identify Language and Version

**Look for:**
- Version files: `package.json`, `pom.xml`, `Cargo.toml`, `.csproj`, `go.mod`
- Runtime indicators: shebang (`#!/usr/bin/python3.11`), compiler version
- Framework indicators: Django, Spring Boot, ASP.NET, etc.

**Example:**
```json
// package.json
{
  "engines": {
    "node": ">=18.0.0"
  }
}
```
→ Reviewing **Node.js 18+** JavaScript code

---

### Step 2: Dynamic Standards Lookup

**Use WebSearch to find current standards:**

**Query Pattern:**
```
"[Language] [Version] security best practices"
"[Language] [Version] common vulnerabilities"
"[Framework] security guide"
```

**Examples:**
- `"Rust 1.75 security best practices"`
- `"Go 1.21 common vulnerabilities secure coding"`
- `"C# .NET 8 security guide"`
- `"Ruby on Rails 7 security vulnerabilities"`

---

### Step 3: Understand Language-Specific Context

**For EACH vulnerability, ask:**

1. **WHAT is the vulnerability in this language?**
   - What can go wrong?
   - What's the attack vector?

2. **WHY does this vulnerability exist in this language?**
   - What language feature enables it?
   - What design decision makes this possible?
   - Why can't the compiler/runtime prevent it?

3. **HOW do you prevent it properly in this language?**
   - What's the secure pattern?
   - Why does this prevention work?
   - Are there language-specific libraries/features?

---

## Language-Specific Lookup Templates

### JavaScript / Node.js

**Key Areas to Research:**

**Prototype Pollution:**
- **WHAT:** Modifying `Object.prototype` affects all objects
- **WHY:** JavaScript's prototype chain is mutable, dynamic property access allows setting `__proto__`
- **LOOKUP:** `"JavaScript prototype pollution prevention 2025"`

**Command Injection:**
- **WHAT:** `child_process.exec` with user input executes shell commands
- **WHY:** `exec` passes string to shell which interprets metacharacters
- **LOOKUP:** `"Node.js child_process security best practices"`

**XSS in React/Vue/Angular:**
- **WHAT:** Rendering user input as HTML allows script injection
- **WHY:** Framework escape mechanisms can be bypassed with `dangerouslySetInnerHTML`, `v-html`, etc.
- **LOOKUP:** `"React XSS prevention 2025"`, `"Vue.js security best practices"`

**Resources to Check:**
- OWASP Node.js Security Cheat Sheet
- npm security advisories
- Framework-specific security guides

---

### Rust

**Key Areas to Research:**

**Unsafe Blocks:**
- **WHAT:** Memory safety violations in unsafe code
- **WHY:** `unsafe` bypasses borrow checker for FFI/low-level ops
- **LOOKUP:** `"Rust unsafe code security audit best practices"`

**Panic Handling:**
- **WHAT:** Unhandled panics cause DoS
- **WHY:** Rust panics unwind stack, can crash process
- **LOOKUP:** `"Rust panic handling production best practices"`

**Dependency Security:**
- **WHAT:** Vulnerable crates in dependency tree
- **WHY:** Rust's cargo ecosystem has many dependencies
- **LOOKUP:** `"Rust cargo audit security"`

**Resources to Check:**
- Rust Security Response WG
- cargo-audit for known vulnerabilities
- RustSec Advisory Database

---

### C# / .NET

**Key Areas to Research:**

**Deserialization:**
- **WHAT:** `BinaryFormatter` allows arbitrary code execution
- **WHY:** Deserializes types with malicious constructors/finalizers
- **LOOKUP:** `".NET deserialization security best practices"`

**SQL Injection:**
- **WHAT:** String concatenation in ADO.NET queries
- **WHY:** No parameterization → SQL injection
- **LOOKUP:** `"C# Entity Framework SQL injection prevention"`

**XXE in XML Parsers:**
- **WHAT:** External entity processing in `XmlReader`
- **WHY:** Default settings process external entities
- **LOOKUP:** `".NET XML external entity prevention"`

**Resources to Check:**
- Microsoft Security Development Lifecycle (SDL)
- .NET Security documentation
- OWASP .NET Security Cheat Sheet

---

### Go

**Key Areas to Research:**

**SQL Injection:**
- **WHAT:** String concatenation in database queries
- **WHY:** Go's `database/sql` doesn't enforce parameterization
- **LOOKUP:** `"Go database sql injection prevention"`

**Command Injection:**
- **WHAT:** `exec.Command` with unsanitized input
- **WHY:** Shell interpretation of arguments
- **LOOKUP:** `"Go os/exec security best practices"`

**Race Conditions:**
- **WHAT:** Concurrent access to shared data without synchronization
- **WHY:** Go's concurrency model makes data races easy
- **LOOKUP:** `"Go race detector concurrent programming best practices"`

**Resources to Check:**
- Go Security documentation
- gosec static analysis tool
- Go vulnerability database

---

### Java

**Key Areas to Research:**

**Deserialization:**
- **WHAT:** `ObjectInputStream` with untrusted data allows code execution
- **WHY:** Deserializes objects with malicious `readObject()` methods
- **LOOKUP:** `"Java deserialization security 2025"`

**XXE:**
- **WHAT:** XML parsers process external entities by default
- **WHY:** Default DocumentBuilderFactory settings
- **LOOKUP:** `"Java XXE prevention XML parser configuration"`

**LDAP Injection:**
- **WHAT:** Unescaped input in LDAP queries
- **WHY:** LDAP filter syntax allows injection
- **LOOKUP:** `"Java LDAP injection prevention"`

**Resources to Check:**
- SEI CERT Oracle Coding Standard for Java
- OWASP Java Security Cheat Sheet
- Find Security Bugs (SpotBugs plugin)

---

### Ruby / Rails

**Key Areas to Research:**

**Mass Assignment:**
- **WHAT:** Unintended attribute updates via parameter binding
- **WHY:** Rails `params` hash directly updates model attributes
- **LOOKUP:** `"Ruby on Rails strong parameters security"`

**Command Injection:**
- **WHAT:** Backticks or `system()` with user input
- **WHY:** Ruby interpolates strings into shell commands
- **LOOKUP:** `"Ruby command injection prevention"`

**SQL Injection:**
- **WHAT:** String interpolation in ActiveRecord queries
- **WHY:** `where("name = '#{params[:name]}'")` doesn't escape
- **LOOKUP:** `"Rails SQL injection prevention ActiveRecord"`

**Resources to Check:**
- Rails Security Guide
- Brakeman static analysis
- Ruby Advisory Database

---

### PHP

**Key Areas to Research:**

**SQL Injection:**
- **WHAT:** `mysql_query()` with string concatenation
- **WHY:** No parameterization → SQL injection
- **LOOKUP:** `"PHP PDO prepared statements security"`

**File Inclusion:**
- **WHAT:** `include()` with user input allows code execution
- **WHY:** PHP executes included files as code
- **LOOKUP:** `"PHP local file inclusion prevention"`

**Deserialization:**
- **WHAT:** `unserialize()` with untrusted data
- **WHY:** PHP magic methods executed during unserialization
- **LOOKUP:** `"PHP unserialize security vulnerabilities"`

**Resources to Check:**
- OWASP PHP Security Cheat Sheet
- PHP Security Consortium
- Modern PHP Security

---

### C / C++

**Key Areas to Research:**

**Buffer Overflow:**
- **WHAT:** Writing beyond array bounds corrupts memory
- **WHY:** No bounds checking on array access
- **LOOKUP:** `"C buffer overflow prevention best practices"`

**Use After Free:**
- **WHAT:** Accessing freed memory causes undefined behavior
- **WHY:** Manual memory management, no garbage collection
- **LOOKUP:** `"C++ use after free prevention RAII"`

**Format String:**
- **WHAT:** `printf(user_input)` allows memory read/write
- **WHY:** Format specifiers interpreted from string
- **LOOKUP:** `"C format string vulnerability prevention"`

**Resources to Check:**
- SEI CERT C/C++ Coding Standards
- MISRA C guidelines
- Static analysis tools (Coverity, PVS-Studio)

---

## Language-Specific Vulnerability Patterns

### Memory-Safe Languages (Python, JavaScript, Java, C#, Go, Ruby)

**Primary Concerns:**
- Injection vulnerabilities (SQL, Command, XSS)
- Deserialization attacks
- Authentication/authorization flaws
- Cryptographic mistakes

**NOT Concerned About:**
- Buffer overflows (runtime prevents)
- Use after free (garbage collected)
- NULL pointer dereference (exceptions thrown)

---

### Memory-Unsafe Languages (C, C++, Rust with unsafe)

**Primary Concerns:**
- Buffer overflows
- Use after free
- NULL pointer dereference
- Race conditions
- Integer overflow

**ALSO Concerned About:**
- Injection vulnerabilities
- Cryptographic mistakes

---

### Compiled Languages (C, C++, Rust, Go, Java, C#)

**Security Advantages:**
- Type safety (prevents some logic errors)
- Earlier bug detection (compile-time)

**Security Disadvantages:**
- May hide vulnerabilities until runtime
- Compiler optimizations can introduce bugs

---

### Interpreted Languages (Python, JavaScript, Ruby, PHP)

**Security Advantages:**
- Easier to audit (source code always available)
- Dynamic analysis tools effective

**Security Disadvantages:**
- Code injection risks (eval, exec)
- Performance-based attacks easier

---

## Example: Reviewing Unknown Language

**Scenario:** You encounter Elixir code (functional language on Erlang VM)

**Step 1: Identify**
```elixir
# mix.exs
def project do
  [
    elixir: "~> 1.14"
  ]
end
```
→ Elixir 1.14

**Step 2: Research**
```
WebSearch: "Elixir 1.14 security best practices"
WebSearch: "Phoenix framework security vulnerabilities"
WebSearch: "Erlang VM security considerations"
```

**Step 3: Find Language-Specific Issues**
Discover:
- **Atoms are not garbage collected** → atom exhaustion DoS
- **SQL injection in Ecto** → use parameterized queries
- **CSRF in Phoenix** → enable `protect_from_forgery`

**Step 4: Understand WHY**
- Atoms: Erlang VM interns all atoms forever → unlimited user input as atoms = memory exhaustion
- Ecto: String interpolation in queries bypasses parameterization
- Phoenix: CSRF tokens must be explicitly enabled

**Step 5: Review Code**
Look for:
- `String.to_atom(user_input)` → vulnerable
- `Ecto.Query.where("name = '#{name}'")` → vulnerable
- Missing `protect_from_forgery` in controller → vulnerable

---

## Quick Reference: Where to Find Standards

| Language | Official Security Resources |
|---|---|
| **Python** | Python Security Advisories, Django/Flask security docs |
| **JavaScript** | OWASP Node.js Cheat Sheet, npm security advisories |
| **Rust** | RustSec Advisory Database, Rust Security WG |
| **C#** | Microsoft SDL, .NET Security documentation |
| **Go** | Go Security documentation, gosec tool |
| **Java** | SEI CERT Java Standard, OWASP Java Cheat Sheet |
| **Ruby** | Rails Security Guide, Ruby Advisory Database |
| **PHP** | OWASP PHP Cheat Sheet, PHP Security Consortium |
| **C/C++** | SEI CERT C/C++ Standards, MISRA C |

---

## Template for Language-Specific Review

```markdown
# [Language] Security Review

## Language Context
- **Version:** [X.Y.Z]
- **Framework:** [Framework Name] [Version]
- **Runtime:** [Node.js / JVM / .NET / etc.]

## Language-Specific Vulnerabilities

### 1. [Vulnerability Name]

**WHAT:** [Description of vulnerability in this language]

**WHY (Root Cause):**
- [Language feature that enables this]
- [Design decision that makes this possible]

**VULNERABLE CODE:**
```[language]
[Code example]
```

**WHY IT'S VULNERABLE:**
[Explanation of why this code is exploitable]

**SECURE CODE:**
```[language]
[Fixed code example]
```

**WHY IT'S SECURE:**
[Explanation of why prevention works]

**CWE:** CWE-XXX

---

[Repeat for each vulnerability type]
```

---

**Version:** 2.0
**Last Updated:** 2025-12-02
**Approach:** Dynamic lookup for language-specific security standards
**Focus:** Teach WHAT/WHY/HOW for each language's unique vulnerabilities
