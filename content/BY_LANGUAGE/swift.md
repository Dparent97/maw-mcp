# Swift / iOS Learnings

Patterns and gotchas from iOS/Swift projects.

---

## SwiftUI Patterns

### Published State in ObservableObject
```swift
class CameraManager: ObservableObject {
    @Published var isAnalyzing: Bool = false
    @Published var errorMessage: String?
    @Published var analysisResult: AnalysisResponse?
}
```

### Conditional Views with @ViewBuilder
```swift
@ViewBuilder
var statusOverlay: some View {
    if isLoading {
        ProgressView("Analyzing...")
    } else if let error = errorMessage {
        Text(error).foregroundColor(.red)
    }
}
```

---

## Common Gotchas

### Type Mismatches in Ternaries
See: [BY_ERROR/type-mismatches.md](../BY_ERROR/type-mismatches.md)

```swift
// BAD: different types
let bg = isWarning ? Color.red : LinearGradient(...)

// GOOD: same type
let bg = LinearGradient(
    colors: isWarning ? [.red] : [.blue],
    startPoint: .top, endPoint: .bottom
)
```

### Main Thread UI Updates
```swift
// BAD: updating UI from background thread
DispatchQueue.global().async {
    self.isLoading = false  // Crash or warning
}

// GOOD: dispatch to main
DispatchQueue.main.async {
    self.isLoading = false
}

// BETTER: use @MainActor
@MainActor
func updateUI() {
    self.isLoading = false
}
```

### Optional Binding
```swift
// BAD: force unwrap
let url = URL(string: urlString)!

// GOOD: guard
guard let url = URL(string: urlString) else {
    print("Invalid URL: \(urlString)")
    return
}
```

---

## Networking

### URLSession with Async/Await
```swift
func analyzeImage(_ imageData: Data) async throws -> AnalysisResponse {
    var request = URLRequest(url: URL(string: "\(baseURL)/analyze")!)
    request.httpMethod = "POST"
    request.setValue("image/jpeg", forHTTPHeaderField: "Content-Type")
    request.httpBody = imageData
    
    let (data, response) = try await URLSession.shared.data(for: request)
    
    guard let httpResponse = response as? HTTPURLResponse,
          httpResponse.statusCode == 200 else {
        throw NetworkError.serverError
    }
    
    return try JSONDecoder().decode(AnalysisResponse.self, from: data)
}
```

### localhost vs Device IP
See: [BY_ERROR/network-config.md](../BY_ERROR/network-config.md)

```swift
// Simulator: localhost works
// Device: need Mac's actual IP
#if DEBUG
static let backendURL = "http://192.168.1.100:8000"
#else
static let backendURL = "https://api.production.com"
#endif
```

---

## ARKit/RealityKit

### Basic AR Setup
```swift
struct ARViewContainer: UIViewRepresentable {
    func makeUIView(context: Context) -> ARView {
        let arView = ARView(frame: .zero)
        let config = ARWorldTrackingConfiguration()
        config.planeDetection = [.horizontal, .vertical]
        arView.session.run(config)
        return arView
    }
}
```

### Simulator Limitations
ARKit requires physical device. Check before running AR code:
```swift
#if targetEnvironment(simulator)
Text("AR requires physical device")
#else
ARViewContainer()
#endif
```

### 2D to 3D Coordinate Mapping
```swift
// Convert normalized 2D position to 3D world position
func worldPosition(from normalized: SIMD2<Float>, in arView: ARView) -> SIMD3<Float> {
    let screenPoint = CGPoint(
        x: CGFloat(normalized.x) * arView.bounds.width,
        y: CGFloat(normalized.y) * arView.bounds.height
    )
    
    if let result = arView.raycast(from: screenPoint, allowing: .estimatedPlane, alignment: .any).first {
        return result.worldTransform.translation
    }
    
    // Fallback: place at fixed distance
    return SIMD3<Float>(normalized.x - 0.5, normalized.y - 0.5, -1.0)
}
```

---

## Permissions

### Camera Permission
```swift
// Info.plist
<key>NSCameraUsageDescription</key>
<string>Camera access needed for AR features</string>

// Request
AVCaptureDevice.requestAccess(for: .video) { granted in
    DispatchQueue.main.async {
        self.cameraAuthorized = granted
    }
}
```

---

## Haptic Feedback
```swift
func triggerSuccessHaptic() {
    let generator = UINotificationFeedbackGenerator()
    generator.notificationOccurred(.success)
}

func triggerWarningHaptic() {
    let generator = UINotificationFeedbackGenerator()
    generator.notificationOccurred(.warning)
}
```

---

*Last updated: 2025-12-11*
