# Merge Conflict Patterns

Issues that arise from merging parallel agent work.

---

## Common Issues

### Duplicate Code Blocks After Merge
**Date:** 2025-12-21
**Project:** crew-shopping-list

**Context:** Four parallel agents working on same files. Agent 2 (Budget UI) and Agent 3 (Live Updates) both added `updateBudgetDisplay` and `storeNames` to shop.js.

**Problem:**
Git merge kept both copies - file had two identical function definitions:
```javascript
// Lines 161-214: First copy
const storeNames = { ... };
function updateBudgetDisplay(list) { ... }

// Lines 216-271: Second copy (duplicate)
const storeNames = { ... };
function updateBudgetDisplay(list) { ... }
```

**Symptom:**
- No merge conflict reported (additions at different locations)
- JavaScript loaded without syntax error
- But runtime broke - cook couldn't see shopping list
- No visible error in console (duplicate const just overwrites)

**Solution:**
```bash
# Find duplicates
grep -n "function updateBudgetDisplay" static/js/shop.js
# Delete the second occurrence
```

**Prevention:**
1. **Codex review** should identify files multiple agents will touch
2. **Coordinator** should specify which agent owns which functions
3. **Post-merge integration test** - actually load every page, not just check if app starts
4. When agents touch same file, add to merge checklist: "Check for duplicate functions/consts"

---

### Test Data vs Production Data Confusion
**Date:** 2025-12-21
**Project:** crew-shopping-list

**Context:** Test Claudes ran app with in-memory test database. User reported "no images showing."

**Problem:**
- TestingConfig uses `sqlite:///:memory:` with placeholder data
- Production uses `data/shopping.db` with real Cloudinary URLs
- API returned `image_url: "https://via.placeholder.com/200"` from test data

**Symptom:**
- Placeholder gray boxes instead of product images
- Code worked fine - it was rendering the URLs correctly

**Solution:**
Run with production config:
```bash
FLASK_APP=src.app:create_app flask run --port 5001
```
Then verify API returns real URLs:
```bash
curl http://localhost:5001/api/products/search?q=ZOA | jq '.[0].image_url'
```

**Prevention:**
1. Always check which database is being used before debugging
2. Test agents should use production-like seed data, not placeholders
3. Add to testing checklist: "Verify using correct database"
