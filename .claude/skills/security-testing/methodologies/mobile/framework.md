
## Methodology Overview

Mobile application security testing identifies vulnerabilities in Android and iOS applications through static analysis, dynamic analysis, and runtime manipulation using the OWASP Mobile Application Security Testing Guide.

---

## OWASP MASTG Integration

**Reference:** https://mas.owasp.org/MASTG/ (use WebFetch)
**Size:** 1,168 files, 8.2 MB, 951k tokens
**Coverage:** Comprehensive mobile security testing for Android and iOS

### OWASP Mobile Application Security Verification Standard (MASVS)

**Security Categories (8 domains):**

1. **MASVS-STORAGE** - Secure Data Storage
   - Sensitive data in local storage
   - Logs containing sensitive information
   - Shared storage vulnerabilities
   - Keyboard cache leakage

2. **MASVS-CRYPTO** - Cryptography
   - Weak cryptographic algorithms
   - Insecure key storage
   - Hardcoded encryption keys
   - Inadequate random number generation

3. **MASVS-AUTH** - Authentication and Session Management
   - Insecure authentication mechanisms
   - Weak session management
   - Biometric bypass
   - OAuth/SSO issues

4. **MASVS-NETWORK** - Network Communication
   - Unencrypted data transmission
   - Certificate validation bypass
   - Certificate pinning issues
   - Cleartext traffic

5. **MASVS-PLATFORM** - Platform Interaction
   - Insecure IPC (Inter-Process Communication)
   - WebView vulnerabilities
   - Custom URL scheme abuse
   - Exported components (Android)

6. **MASVS-CODE** - Code Quality
   - Reverse engineering protections
   - Debugging enabled in production
   - Memory corruption vulnerabilities
   - Injection vulnerabilities

7. **MASVS-RESILIENCE** - Anti-Tampering and Anti-Reversing
   - Root/jailbreak detection
   - Debugger detection
   - Emulator detection
   - Code obfuscation
   - Anti-hooking mechanisms

8. **MASVS-PRIVACY** - Privacy Controls
   - Unnecessary permissions
   - Privacy policy compliance
   - Data minimization
   - User consent mechanisms

---

## Platform-Specific Testing

### Android Security Testing

**Android-Specific Vulnerabilities:**

1. **Insecure Data Storage**
   - SharedPreferences without encryption
   - Unencrypted SQLite databases
   - Files in external storage
   - Logcat leakage

2. **Component Security**
   - Exported Activities (unauthorized access)
   - Exported Content Providers (SQL injection, path traversal)
   - Exported Broadcast Receivers (intent manipulation)
   - Exported Services (unauthorized binding)

3. **Inter-Process Communication (IPC)**
   - Intent injection/sniffing
   - Implicit intents
   - Pending Intent vulnerabilities
   - Insecure Binder communication

4. **Android-Specific Attacks**
   - Task hijacking/overlay attacks
   - Tapjacking
   - Broadcast injection
   - Deep link exploitation

5. **Code Analysis**
   - Decompiling APK (JADX, JEB, Ghidra)
   - AndroidManifest.xml analysis
   - Native library vulnerabilities (.so files)
   - ProGuard/R8 obfuscation bypass

**Android Tools:**
- Frida (runtime instrumentation)
- Objection (Frida-based testing framework)
- MobSF (automated analysis)
- APKTool (decompilation)
- JADX (Java decompiler)
- Drozer (Android security testing framework)
- ADB (Android Debug Bridge)

---

### iOS Security Testing

**iOS-Specific Vulnerabilities:**

1. **Insecure Data Storage**
   - Unencrypted Keychain items
   - NSUserDefaults storing sensitive data
   - Core Data encryption issues
   - Backup data exposure

2. **Inter-App Communication**
   - Custom URL scheme hijacking
   - Universal Links misconfiguration
   - Pasteboard data leakage
   - Insecure App Extensions

3. **Platform Integration**
   - Insecure WebView configurations
   - JavaScript bridge vulnerabilities
   - TouchID/FaceID bypass
   - Local authentication weaknesses

4. **iOS-Specific Attacks**
   - Binary patching
   - Method swizzling
   - Runtime manipulation (Cycript)
   - IPA repackaging

5. **Code Analysis**
   - IPA extraction and analysis
   - Binary analysis (Hopper, IDA Pro, Ghidra)
   - Swift/Objective-C reverse engineering
   - Class-dump analysis
   - plist file inspection

**iOS Tools:**
- Frida (runtime instrumentation)
- Objection (Frida-based framework)
- MobSF (automated analysis)
- Clutch (decryption for jailbroken devices)
- Class-dump (Objective-C class extraction)
- Hopper Disassembler
- iProxy (USB tunneling)
- Burp Suite Mobile Assistant

---

## Testing Methodology Structure

### EXPLORE Phase

1. **Scope Review**
   - Read SCOPE.md for target applications
   - Identify platform (Android, iOS, or both)
   - Determine app version to test
   - Understand authentication requirements
   - Note any third-party SDKs in use

2. **Application Acquisition**
   - Download APK from Play Store or client
   - Extract IPA from App Store or client
   - Verify application authenticity
   - Document app version and build info

3. **Static Analysis (Initial)**
   - **Android:** Decompile APK, analyze AndroidManifest.xml
   - **iOS:** Extract IPA, analyze Info.plist
   - Identify sensitive strings (API keys, URLs)
   - Review permissions requested
   - Map application structure

4. **MASVS Mapping**
   - Map app features to MASVS categories
   - Identify high-risk areas (authentication, storage, network)
   - Prioritize testing based on sensitivity

### PLAN Phase

1. **Test Environment Setup**
   - **Android:** Emulator vs. physical device (rooted/non-rooted)
   - **iOS:** Simulator vs. jailbroken device
   - Proxy configuration (Burp Suite)
   - Certificate installation and pinning bypass

2. **Tool Inventory Check** (CRITICAL)
   - Review `/servers` for available mobile testing tools
   - Check for: Frida, Objection, MobSF, APKTool, Burp Mobile Assistant
   - Identify missing tools
   - Request deployment if needed (especially MobSF container)

3. **Test Plan Generation**
   - Map MASVS controls to specific tests
   - Plan static + dynamic analysis
   - Document testing approach per platform
   - Include certificate pinning bypass strategy
   - Get user approval

### CODE Phase (Testing)

**Static Analysis (Deep Dive):**

1. **Code Review**
   - Decompile and analyze source code
   - Identify hardcoded secrets (API keys, encryption keys)
   - Review cryptographic implementations
   - Analyze authentication logic
   - Check for insecure random number generation

2. **Manifest/Plist Analysis**
   - **Android:** Exported components, permissions, intent filters
   - **iOS:** URL schemes, App Transport Security, background modes
   - Identify misconfigurations

3. **Binary Analysis**
   - Analyze native libraries (.so, .dylib)
   - Check for binary protections (PIE, stack canaries)
   - Identify potential memory corruption vulnerabilities

**Dynamic Analysis:**

1. **Network Traffic Analysis**
   - Intercept traffic with Burp Suite
   - Test certificate pinning (SSL pinning bypass)
   - Identify cleartext traffic
   - Test API endpoints for web vulnerabilities

2. **Runtime Manipulation (Frida/Objection)**
   - Bypass root/jailbreak detection
   - Bypass SSL pinning
   - Hook methods to observe behavior
   - Modify return values for testing
   - Extract encryption keys from memory

3. **Data Storage Testing**
   - **Android:** SharedPreferences, SQLite, internal/external storage
   - **iOS:** Keychain, NSUserDefaults, Core Data
   - Check for sensitive data in logs
   - Test backup encryption

4. **Authentication & Session Testing**
   - Test biometric bypass
   - Session token analysis
   - JWT vulnerabilities (if used)
   - OAuth/SSO flow testing

5. **Platform Integration Testing**
   - **Android:** Intent fuzzing, component testing, IPC
   - **iOS:** URL scheme testing, pasteboard, App Extensions
   - WebView testing (XSS, file access)
   - Deep link exploitation

**Evidence Collection:**
- Screenshots of vulnerabilities
- Frida scripts used
- Code snippets demonstrating issues
- Network traffic captures
- Map findings to MASVS controls

### COMMIT Phase (Reporting)

1. **Findings Documentation**
   - Executive summary
   - Technical findings mapped to MASVS
   - Severity ratings
   - Evidence (screenshots, code, scripts)
   - Platform-specific remediation

2. **Remediation Recommendations**
   - Secure coding practices
   - Configuration changes
   - Library updates
   - Encryption recommendations
   - Reference OWASP Mobile Cheat Sheets

3. **MASVS Integration**
   - Map findings to MASVS categories
   - Include MASVS-L1/L2 control references
   - Link to relevant MASTG sections

---

## Common Mobile Vulnerabilities

### Data Storage
- **Sensitive Data in Logs:** Credentials, tokens in Logcat/Console
- **Unencrypted Databases:** SQLite, Realm without encryption
- **Insecure SharedPreferences/NSUserDefaults:** Passwords stored in plaintext
- **External Storage:** Sensitive files in publicly accessible storage
- **Keyboard Cache:** Sensitive input cached on device

### Cryptography
- **Hardcoded Keys:** Encryption keys in source code
- **Weak Algorithms:** DES, 3DES, MD5, SHA1
- **Insecure Random:** Predictable random number generation
- **ECB Mode Usage:** Block cipher in ECB mode

### Authentication
- **Biometric Bypass:** LocalAuthentication can be bypassed
- **Weak Session Management:** Sessions don't expire, tokens in SharedPreferences
- **Client-Side Validation Only:** No server-side authentication checks
- **OAuth Issues:** Redirect URI manipulation, PKCE not implemented

### Network Communication
- **No SSL/TLS:** Cleartext HTTP traffic
- **SSL Pinning Issues:** Improperly implemented or missing
- **Certificate Validation Bypass:** Accepting all certificates
- **Weak TLS Configuration:** TLS 1.0/1.1, weak cipher suites

### Platform-Specific
- **Android Exported Components:** Activities, Services, Receivers accessible
- **Android Intent Injection:** Malicious apps can send crafted intents
- **iOS URL Scheme Hijacking:** Another app registers same scheme
- **WebView Vulnerabilities:** JavaScript enabled, file access allowed

### Code Quality
- **Reverse Engineering:** Lack of obfuscation, easy decompilation
- **Debugging Enabled:** Debuggable flag set in production
- **Root/Jailbreak Detection:** Missing or easily bypassed
- **Memory Corruption:** Buffer overflows in native code

---

## Testing Tools by Platform

### Cross-Platform Tools
- **Frida:** Runtime instrumentation (Android/iOS)
- **Objection:** Frida-based testing framework
- **Burp Suite:** Network traffic interception
- **MobSF:** Automated static/dynamic analysis
- **Ghidra:** Binary analysis and reverse engineering

### Android-Specific
- **APKTool:** APK decompilation
- **JADX:** Java decompiler
- **Drozer:** Android security framework
- **ADB:** Android Debug Bridge
- **Apktool:** Resource extraction
- **dex2jar:** Convert DEX to JAR

### iOS-Specific
- **Clutch:** IPA decryption (jailbroken devices)
- **Class-dump:** Extract Objective-C headers
- **iProxy:** USB port forwarding
- **Hopper Disassembler:** Binary analysis
- **Cycript:** Runtime analysis (jailbroken)
- **SSL Kill Switch:** SSL pinning bypass

---

## Reference Resources

### Web Resources (Mobile-specific not ingested locally)

**OWASP Mobile:**
- MASTG: https://mas.owasp.org/MASTG/
- MASVS: https://mas.owasp.org/MASVS/
- Mobile Top 10: https://owasp.org/www-project-mobile-top-10/

**Books:** `Glob: resources/library/books/**/*mobile*` or `**/*bug-bounty*`

**Web Resources:**
- OWASP Mobile Testing Guide: https://mas.owasp.org/MASTG/

**Note:** Consider using gitingest to ingest OWASP Mobile Security repos if needed frequently.

---

**Created:** 2025-12-01
**Framework:** Intelligence Adjacent (IA) - Security Testing
**Version:** 1.0
