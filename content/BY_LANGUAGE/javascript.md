# JavaScript Learnings

Language-specific patterns and gotchas for JavaScript development.

---

## Common Pitfalls

### Duplicate const/function Definitions Don't Error
**Date:** 2025-12-21
**Project:** crew-shopping-list

**Context:** Multi-agent merge left two copies of same function in file.

**Problem:**
Unlike compiled languages, JavaScript doesn't error on duplicate function definitions at load time:
```javascript
// Both functions load without error
function updateBudgetDisplay(list) { /* version 1 */ }
// ... 50 lines later ...
function updateBudgetDisplay(list) { /* version 2 */ }
// Second one silently overwrites first
```

For `const`, behavior depends on scope:
```javascript
// Top-level in module: SyntaxError (duplicate identifier)
const x = 1;
const x = 2;  // Error!

// But in different files concatenated: No error, second wins
```

**Symptom:**
- No console errors
- No syntax errors
- But runtime behavior is wrong (functions may have different logic)
- Hard to debug because everything "looks fine"

**Prevention:**
1. After merging parallel work, search for duplicate definitions:
   ```bash
   grep -n "function functionName\|const varName" file.js | sort | uniq -d
   ```
2. Use ESLint with `no-redeclare` rule
3. Use modules (ES6 imports) to prevent global scope pollution

---

### onclick vs addEventListener Scoping
**Date:** 2025-12-21
**Project:** crew-shopping-list

**Context:** Delete button needed to pass event to stopPropagation.

**Good Pattern:**
```javascript
// Inline onclick can access event implicitly
<button onclick="deleteItem(${item.id}, event)">🗑</button>

async function deleteItem(itemId, event) {
    event.stopPropagation();  // Prevent parent click handler
    // ... delete logic
}
```

**Alternative (better separation):**
```javascript
// addEventListener in JS file
document.querySelectorAll('.delete-btn').forEach(btn => {
    btn.addEventListener('click', (event) => {
        event.stopPropagation();
        deleteItem(btn.dataset.itemId);
    });
});
```

**Gotcha:** If using string interpolation to build HTML, inline onclick is simpler than re-querying DOM after innerHTML set.

---

## Useful Patterns

### HTML Escaping for User Content
**Date:** 2025-12-21
**Project:** crew-shopping-list

**Pattern:** Always escape user-provided content before inserting into DOM:
```javascript
function escapeHTML(str) {
    if (str == null) return '';
    return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}

// Usage
innerHTML = `<div>${escapeHTML(userInput)}</div>`;
```

**Why:** Prevents XSS attacks and broken HTML from user content.

---

### Toast Notifications Pattern
**Date:** 2025-12-21
**Project:** crew-shopping-list

**Pattern:** Self-removing toast system:
```javascript
function showToast(message, type = 'info', duration = 3000) {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `<span>${escapeHTML(message)}</span>`;
    document.body.appendChild(toast);
    
    // Trigger CSS animation
    requestAnimationFrame(() => toast.classList.add('show'));
    
    // Auto-remove
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);  // Wait for fade-out
    }, duration);
}
```

**Why:** Better UX than `alert()`, non-blocking, auto-dismisses.
