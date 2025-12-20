# Mobile App Download Tools

**Purpose:** Flexible tools for downloading iOS and Android apps from various sources for security testing.

---

## Tool Architecture

### Core Components

1. **ipatool (iOS)** - VPS-based download from App Store
2. **Helper Scripts** - Flexible download workflows
3. **Manual Methods** - Alternative sources when needed

---

## iOS Download Methods

### Method 1: App Store (Official - ipatool)

**Use when:**
- App is publicly available on App Store
- Have valid Apple ID credentials
- App is free or already purchased

**Requirements:**
- ipatool installed on VPS (or local machine)
- Apple ID with app access

**Command:**
```bash
# By App ID
ipatool download --app-id <APP_ID> --purchase

# By Bundle ID
ipatool download --bundle-identifier <BUNDLE_ID> --purchase

# Specific version
ipatool download --app-id <APP_ID> --external-version-id <VERSION_ID>
```

**Example:**
```bash
ssh -i "C:\Users\Chris\.ssh\gro_256" root@72.60.27.87
ipatool download --app-id 914172636 --purchase
```

### Method 2: TestFlight (Beta Testing)

**Use when:**
- Testing beta/staging versions
- Provided TestFlight invitation link

**Requirements:**
- iOS device with TestFlight app installed
- Invitation link from target organization
- Apple ID invited to beta

**Process:**
1. Open TestFlight invitation link on iOS device
2. Accept invitation
3. Download from TestFlight app
4. Extract IPA using tools (requires jailbreak or special tooling)

### Method 3: Enterprise Distribution

**Use when:**
- Internal/enterprise apps distributed via MDM
- Direct .ipa file provided by organization
- Ad-hoc distribution profiles

**Requirements:**
- Direct download link (e.g., `.ipa` URL)
- Provisioning profile (if required)

**Command:**
```bash
curl -L -o app.ipa "https://example.com/downloads/app.ipa"
```

### Method 4: Direct IPA File

**Use when:**
- Organization provides IPA file directly
- App is not on App Store

**Process:**
1. Receive IPA via email, file sharing, etc.
2. Verify signature and source authenticity
3. Place in engagement binaries folder

---

## Android Download Methods

### Method 1: Google Play Store

**Option A - APK Mirror Sites (No Auth Required):**

**APKPure:**
```bash
# Manual download from:
https://apkpure.net/<package_id>
```

**APKMirror:**
```bash
# Manual download from:
https://www.apkmirror.com/
# Search for app name
```

**Option B - Direct Play Store (Requires Auth):**

Tools available (if needed in future):
- `gplaycli` (Python-based)
- `apkeep` (Rust-based, requires Google credentials)
- `PlaystoreDownloader` (Python-based)

### Method 2: Internal Distribution

**Use when:**
- App distributed internally via Firebase App Distribution
- App uses custom APK hosting
- Enterprise app store

**Sources:**
- Firebase App Distribution links
- Internal app portals
- Direct APK download URLs

**Command:**
```bash
curl -L -o app.apk "https://internal.example.com/apps/latest.apk"
```

### Method 3: Direct APK File

**Use when:**
- Organization provides APK directly
- Custom/internal apps not on Play Store

**Process:**
1. Receive APK via email, file sharing, etc.
2. Verify signature: `apksigner verify --verbose app.apk`
3. Place in engagement binaries folder

---

## Helper Script Usage

**Location:** `C:\Users\Chris\.claude\tools\security\download_mobile_apps.sh`

**iOS Download:**
```bash
bash download_mobile_apps.sh ios <APP_ID> <OUTPUT_DIR>
```

**Android Download:**
```bash
bash download_mobile_apps.sh android <PACKAGE_ID> <OUTPUT_DIR>
```

**Future Enhancement:** Script can be extended to support:
- TestFlight URLs
- Custom distribution URLs
- Enterprise app stores
- Multiple app sources in single command

---

## Verification Workflow (Universal)

**MANDATORY for ALL apps, regardless of source:**

### 1. File Integrity
```bash
# iOS
codesign -dvv app.ipa
unzip -l app.ipa  # Check contents

# Android
apksigner verify --verbose app.apk
aapt dump badging app.apk
```

### 2. Network Traffic Verification
```bash
# Route app through Reaper proxy
# Capture first network requests
# Verify endpoints match expected environment (staging/test/production)

sqlite3 ~/.reaper/reaper.db "SELECT DISTINCT hostname FROM requests WHERE app_name = '<APP>';"
```

### 3. Environment Detection
```
✅ Verify app connects to TEST/STAGING environment
❌ DO NOT test if app points to PRODUCTION (unless production is in scope)
```

### 4. Login Test
- Attempt login with test credentials
- Success = Correct environment
- Failure = Wrong environment or invalid creds

---

## Adding New Sources

When encountering a new distribution method:

1. **Document the source:**
   - Source type (e.g., HockeyApp, AppCenter, custom portal)
   - Authentication requirements
   - Download process

2. **Add to this guide:**
   - Create new method section
   - Document commands/steps
   - Add verification requirements

3. **Update helper script (if automatable):**
   - Add new source type as option
   - Implement download logic
   - Test with real app

4. **Update SKILL.md:**
   - Reference new method
   - Add to engagement setup checklist

---

## Common Sources Reference

| Source | iOS | Android | Auth Required | Notes |
|--------|-----|---------|---------------|-------|
| App Store | ✅ | ❌ | Apple ID | Use ipatool |
| Google Play | ❌ | ✅ | Optional | APK mirrors easier |
| TestFlight | ✅ | ❌ | Invitation | Beta iOS apps |
| Firebase App Distribution | ✅ | ✅ | Invitation | Internal testing |
| HockeyApp (deprecated) | ✅ | ✅ | Account | Legacy platform |
| App Center | ✅ | ✅ | Account | Microsoft platform |
| Enterprise MDM | ✅ | ✅ | Varies | Internal distribution |
| Direct URL | ✅ | ✅ | Varies | Custom hosting |

---

## Troubleshooting

### iOS Issues

**"App not purchased":**
- Use `--purchase` flag (works for free apps)
- Or purchase app with Apple ID first

**"Invalid credentials":**
- Use app-specific password: https://appleid.apple.com
- Enable 2FA if required

**"App not found":**
- Verify app ID is correct
- Check app availability in your region
- App may be removed or restricted

### Android Issues

**APK download blocked:**
- Try different mirror site
- Use VPN if region-restricted
- Try direct Play Store with auth tools

**Wrong architecture:**
- Look for "universal" APK
- Or download all splits: arm64-v8a, armeabi-v7a, x86, x86_64

**Signature verification fails:**
- APK may be modified (DO NOT USE)
- Download from official source
- Verify with known good hash

---

## Documentation Template

When adding apps to `creds.txt`:

```
## Mobile Apps
iOS App Location: <path>/app-name.ipa
Android App Location: <path>/app-name.apk
iOS Version: <version>
Android Version: <version>
Download Source: [App Store / TestFlight / Firebase / Custom URL / etc.]
Download Date: <date>
Downloaded By: [Tool / Manual]
⚠️ Environment Verified: [ ] Yes [ ] No
✅ Signature Verified: [ ] Yes [ ] No
```

---

**Remember:** Always verify app environment before testing. One wrong endpoint = scope violation.
