# Swift Type Mismatches

Swift's type system is strict. Ternary operators and conditional expressions require matching types on both branches.

---

## The Problem

```swift
// BAD: mismatched types - won't compile
let background = isWarning ? Color.red : LinearGradient(...)
//                           ^^^^^^^      ^^^^^^^^^^^^^^^
//                           Color        LinearGradient
```

Swift sees `Color` and `LinearGradient` as different types, even though both can be used as backgrounds.

---

## The Solution

Make both branches return the same type:

```swift
// GOOD: both branches return LinearGradient
let background = LinearGradient(
    colors: isWarning ? [.red, .red.opacity(0.8)] : [.blue, .blue.opacity(0.8)],
    startPoint: .top,
    endPoint: .bottom
)
```

Or use type erasure:

```swift
// GOOD: both branches return AnyShapeStyle
let background: AnyShapeStyle = isWarning 
    ? AnyShapeStyle(Color.red) 
    : AnyShapeStyle(LinearGradient(...))
```

---

## Common Variations

### View Builders
```swift
// BAD
var body: some View {
    if condition {
        Text("A")
    } else {
        Image("B")  // Different type!
    }
}

// GOOD: Use @ViewBuilder or Group
@ViewBuilder
var body: some View {
    if condition {
        Text("A")
    } else {
        Image("B")
    }
}
```

### Optional Unwrapping
```swift
// BAD
let value = optionalString ?? 0  // String? vs Int

// GOOD
let value = optionalString ?? "default"
```

---

## Agent-Generated Code Warning

AI agents often generate ternary expressions without checking type consistency. After merging agent code:

1. Build immediately
2. Look for "cannot convert" or "type mismatch" errors
3. Fix by unifying types on both branches

---

## Projects Where This Occurred

| Project | Date | Context | Resolution |
|---------|------|---------|------------|
| Reality-layer | 2025-12-11 | AR label styling | Unified to LinearGradient on both branches |

---

*Last updated: 2025-12-11*
