# QUICK MERGE REVIEW

## Context
5 agents finished their work. I need to review and merge everything.

**Repository:** https://github.com/[YOUR_USERNAME]/[YOUR_REPO]
**Base Branch:** dev

## Your Tasks

### 1. List All PRs (2 minutes)
```bash
gh pr list --state open
```

### 2. Quick Review (15 minutes)
For each PR:
- Check what it does
- Verify tests pass
- Note files modified

### 3. Determine Merge Order (5 minutes)
Based on dependencies and conflicts, recommend order:
1. PR #XX - [Why first]
2. PR #YY - [Why second]
3. PR #ZZ - [Why third]
4. PR #AA - [Why fourth]
5. PR #BB - [Why fifth]

### 4. Merge All PRs (20-30 minutes)
For each PR in order:
```bash
gh pr merge [PR_NUMBER] --squash --delete-branch
git checkout dev && git pull origin dev
# Run tests
```

### 5. Final Check (5 minutes)
- [ ] All 5 PRs merged
- [ ] Tests passing
- [ ] App works
- [ ] Ready for next step

## Output Required

```markdown
# MERGE SUMMARY

## PRs Merged
1. PR #XX - [Description] ✅
2. PR #YY - [Description] ✅
3. PR #ZZ - [Description] ✅
4. PR #AA - [Description] ✅
5. PR #BB - [Description] ✅

## Final Status
- Tests: [Pass/Fail]
- Build: [Success/Errors]
- Issues: [Any problems]

## Next Steps
[Recommendation: Iterate/Deploy/Features]
```

---

**START NOW** - List the PRs and begin quick review
