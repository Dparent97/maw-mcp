---
name: capture-learnings
description: Extract learnings from current session and update central learnings repo. Invoke on "capture learnings", "save what we learned", or after productive debugging sessions.
triggers:
  - USE WHEN user says "capture learnings"
  - USE WHEN user says "save what we learned"  
  - USE WHEN user says "update learnings"
  - USE WHEN user says "add to learnings"
  - USE WHEN session had significant debugging or pattern discovery
---

# Capture Learnings

Extracts patterns, fixes, and insights and commits to the central learnings repository.

## Configuration

```
Learnings Repository: /Users/dp/Projects/maw-mcp/content/
Central Patterns: /Users/dp/Projects/maw-mcp/content/UNIVERSAL_PATTERNS.md
Auto-commit: true
Git Remote: git@github.com:Dparent97/maw-mcp.git
```

## Two-Tier System

### Tier 1: Project Learnings (Local, Gitignored)
- **Location:** `PROJECT_LEARNINGS.md` in each project root
- **Scope:** Personal notes, sensitive context, project-specific issues
- **Tool:** `maw_learn learning="..."`
- **Visibility:** Private to you

### Tier 2: Universal Patterns (Central, Committed)
- **Location:** `/Users/dp/Projects/maw-mcp/content/`
- **Scope:** Cross-project patterns, reusable solutions
- **Tool:** `maw_learn learning="..." promote=true`
- **Visibility:** Committed to git

---

## Learnings Structure

```
/Users/dp/Projects/maw-mcp/content/
├── BY_TOOL/           # Tool-specific patterns
│   ├── claude_skills.md
│   ├── gemini-api.md
│   ├── git.md
│   └── [tool-name].md
├── BY_ERROR/          # Error patterns and fixes
│   ├── import-time-init.md
│   ├── merge-conflicts.md
│   ├── network-config.md
│   └── [error-pattern].md
├── BY_LANGUAGE/       # Language-specific gotchas
│   ├── javascript.md
│   ├── python.md
│   ├── swift.md
│   └── [language].md
└── UNIVERSAL_PATTERNS.md  # Cross-project patterns
```

---

## Quick Usage

### Capture to Project (Private)
```
maw_learn learning="Flask-Login requires user_loader to return None for invalid IDs, not raise exception"
```

### Promote to Universal (Public)
```
maw_learn learning="Flask-Login requires user_loader to return None for invalid IDs" promote=true
```

### Search Existing Patterns
```
maw_patterns query="flask"
```

---

## What to Capture

### Capture if:
- Bug took >10 minutes to solve
- Pattern likely to recur across projects
- Non-obvious tool/library behavior
- "Aha" moment worth preserving
- Mistake you don't want to repeat

### Skip if:
- Trivial typo
- One-off project-specific issue
- Already documented in official docs
- Standard documented behavior

---

## Categorization Guide

| Learning About | Promote To |
|----------------|------------|
| Tool quirks (Claude, Git, etc.) | BY_TOOL/[tool].md |
| Error patterns | BY_ERROR/[pattern].md |
| Language gotchas | BY_LANGUAGE/[lang].md |
| Workflow patterns | UNIVERSAL_PATTERNS.md |
| Best practices | UNIVERSAL_PATTERNS.md |

---

## Learning Entry Format

```markdown
### [Short Descriptive Title]
**Date:** YYYY-MM-DD
**Project:** [project-name]
**Context:** [1-2 sentences on when this occurs]

**Problem:**
[What went wrong or was confusing]

**Solution:**
```[language]
[Code example or fix]
```

**Prevention:**
[How to avoid in future]
```

---

## After Capturing

When done:

```
✅ Learnings captured!

Added to:
• PROJECT_LEARNINGS.md (local)
• BY_TOOL/flask.md (promoted)

Committed: "docs: add learnings from [session-topic]"
```
