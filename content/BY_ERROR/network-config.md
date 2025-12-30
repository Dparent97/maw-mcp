# Network Configuration: localhost vs Device IP

When testing iOS apps with a local backend, `localhost` means different things on simulator vs physical device.

---

## The Problem

```swift
// Config.swift
static let backendURL = "http://localhost:8000"
```

- **Simulator:** `localhost` = your Mac ✅
- **Physical device:** `localhost` = the iPhone itself ❌

Your backend is on your Mac, not the phone.

---

## The Solution

Use your Mac's actual IP address:

```swift
// Config.swift
#if DEBUG
static let backendURL = "http://192.168.1.100:8000"  // Your Mac's IP
#else
static let backendURL = "https://api.production.com"
#endif
```

### Finding Your Mac's IP

```bash
# On Mac
ipconfig getifaddr en0    # WiFi
ipconfig getifaddr en1    # Ethernet
```

Or: System Settings → Network → WiFi → Details → IP Address

---

## Why This Keeps Happening

1. You fix it in Config.swift
2. Agent branch overwrites Config.swift during merge
3. You forget to re-fix after merge
4. Device testing fails with "connection refused"

---

## Better Solutions

### Option 1: Environment-based Config
```swift
static var backendURL: String {
    ProcessInfo.processInfo.environment["BACKEND_URL"] ?? "http://localhost:8000"
}
```

### Option 2: Build Configuration
Set in Xcode scheme: Edit Scheme → Run → Arguments → Environment Variables

### Option 3: Settings Bundle
Add a Settings.bundle to let users configure at runtime.

### Option 4: mDNS/Bonjour
Auto-discover backend on local network (more complex).

---

## Quick Debug Check

When device can't connect:

```bash
# On Mac - verify backend is accessible
curl http://localhost:8000/health

# On device - verify network
# (Use browser or network diagnostic app to hit http://YOUR_MAC_IP:8000/health)
```

---

## Projects Where This Occurred

| Project | Date | Context | Resolution |
|---------|------|---------|------------|
| Reality-layer | 2025-12-11 | AR app device testing | Hardcoded Mac IP in Config.swift |
| Reality-layer | 2025-12-11 | Post-merge regression | Re-fixed after agent overwrote |

---

*Last updated: 2025-12-11*
