# Agent [N]: [Role Name]

## Mission
[One sentence: What specific improvement to make]

## Branch
`agent/[N]-[slug]`

## Context
[2-3 sentences: Why this matters, what problem it solves]

## Files to Modify
- `path/to/file1.py` - [What changes]
- `path/to/file2.py` - [What changes]
- `path/to/new_file.py` - [Create: purpose]

## Tasks
1. [ ] [Specific task with measurable outcome]
2. [ ] [Specific task with measurable outcome]
3. [ ] [Specific task with measurable outcome]

## Definition of Done
- [ ] [Primary deliverable]
- [ ] Tests added/updated
- [ ] No linting errors
- [ ] PR created with descriptive title
- [ ] Completion report provided (see below)

## Time Estimate
[X] hours

## Dependencies
- **Depends on:** [Agent N or "None"]
- **Blocks:** [Agent N or "None"]

## Notes
[Any gotchas, edge cases, or context the agent should know]

---

## START NOW

Read this file, create branch `agent/[N]-[slug]`, implement, create PR.

---

## COMPLETION REPORT FORMAT

When you finish, provide this report for the coordinator:

```markdown
## Agent [N] Completion Report

**Status:** ✅ Complete | ⚠️ Partial | ❌ Blocked
**Branch:** `agent/[N]-[slug]`
**PR:** #[number] or [link]

### What Was Done
- [Completed task 1]
- [Completed task 2]
- [Completed task 3]

### Files Changed
| File | Change |
|------|--------|
| path/to/file.py | Created (X lines) |
| path/to/other.py | Modified (+X/-Y lines) |

### Tests
- **Added:** [N] new tests
- **Status:** All passing | X failing
- **Coverage:** [file] [X]%

### API/Endpoints Affected
- `GET /api/endpoint` - [new/modified/tested]
- `POST /api/endpoint` - [new/modified/tested]

### Database Changes
- [New model/migration or "None"]

### Environment/Config
- [New env vars needed or "None"]

### Notes for Integration
- [Merge order dependencies]
- [Potential conflicts with other agents]
- [Things to watch for]

### Time Spent
[X] hours (estimate was [Y]h)
```
