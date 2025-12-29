# Universal Patterns

**Purpose:** Cross-project learnings that apply to ALL work in the multi-agent workflow.  
**Location:** This file lives in your maw-mcp installation, not per-project.

---

## How to Use

Patterns are added here via `maw_learn promote=true` when a learning is valuable across projects.

Search patterns with `maw_patterns query="keyword"`.

---

## Example Pattern

### Error Handling in Flask APIs
**Source:** example-project  
**Date:** 2025-01-15

Always return structured JSON errors:
```python
@app.errorhandler(Exception)
def handle_error(e):
    return jsonify({"error": str(e), "type": type(e).__name__}), 500
```

---

## Your Patterns Will Appear Below

As you run `maw_learn promote=true`, patterns accumulate here.
