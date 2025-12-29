# QUICK POST-INTEGRATION REVIEW

## Context
Just merged all agent branches. Need a quick sanity check before moving forward.

**Repository:** https://github.com/[YOUR_USERNAME]/[YOUR_REPO]
**Branch:** [dev or main]

## Your Mission: Quick Quality Check

Conduct a fast but thorough review focusing on critical issues only.

## Quick Review Checklist (30 minutes)

### 1. What Changed? (5 min)
```bash
git log --oneline -20
git diff main..dev --stat
```

Document:
- 5 improvements that were merged
- Number of files changed
- Any breaking changes

### 2. Critical Issues Check (10 min)

**Security:**
- [ ] No obvious security vulnerabilities?
- [ ] No secrets in code?
- [ ] Input validation present?

**Bugs:**
- [ ] No obvious bugs in changed code?
- [ ] Error handling present?
- [ ] Edge cases considered?

**Breaking Changes:**
- [ ] API compatibility maintained?
- [ ] Database migrations safe?
- [ ] Dependencies compatible?

### 3. Integration Check (10 min)

**Test:**
- [ ] All tests passing?
- [ ] New tests added for new code?
- [ ] No test failures?

**Build:**
- [ ] App builds successfully?
- [ ] No compilation errors?
- [ ] No warning avalanche?

**Run:**
- [ ] App starts successfully?
- [ ] Key features work?
- [ ] No obvious regressions?

### 4. Quick Risk Assessment (5 min)

**What could break?**
- [List top 3 risks]

**What's not tested?**
- [List critical untested paths]

**What needs monitoring?**
- [List what to watch in production]

## Output Required

```markdown
# QUICK REVIEW SUMMARY

## Status: [PASS | ISSUES FOUND | CRITICAL PROBLEMS]

### What Changed
- [Brief summary of 5 improvements]

### Critical Issues
- [List any critical issues, or "None found"]

### Risks
1. [Risk 1]
2. [Risk 2]

### Tests
- Status: [All passing | X failing]
- Coverage: [X]%

### Recommendation
[Ready to deploy | Fix issues first | Needs iteration 2]

### Next Steps
1. [Action 1]
2. [Action 2]
```

---

**START QUICK REVIEW NOW**
