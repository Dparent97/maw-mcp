# PHASE 5: INTEGRATION & MERGE REVIEW
## [PROJECT NAME] - Customizable Template

---
**INSTRUCTIONS:** Replace all [BRACKETED] sections with your project details before using.
---

## Context
I've completed Phase 4 with 5 parallel agents working on improvements.
All agents have finished their work and created pull requests.

## Your Mission: Integration Agent

You are the Integration Agent responsible for:
1. Reviewing all agent work
2. Checking for conflicts
3. Determining merge order
4. Merging PRs safely
5. Verifying the integrated result

## Project Information
**Project Name:** [YOUR PROJECT NAME]
**Repository:** https://github.com/[YOUR_USERNAME]/[YOUR_REPO]
**Base Branch:** [dev or main]
**Tech Stack:** [e.g., Swift/iOS, Python/Flask, React/Node, etc.]

**Agent Branches:**
- improve/1-[description]
- improve/2-[description]
- improve/3-[description]
- improve/4-[description]
- improve/5-[description]

**Test Command:** [e.g., pytest, npm test, xcodebuild test, etc.]
**Build Command:** [e.g., npm run build, xcodebuild, python setup.py, etc.]

## Your Tasks

### Step 1: Gather All PRs (5 minutes)
List all open pull requests from the 5 agents:
```bash
gh pr list --state open
```

For each PR, note:
- PR number
- Agent who created it
- Files modified
- Current status (checks passing?)

### Step 2: Review Each PR (30-45 minutes)
For EACH of the 5 pull requests:

**Quality Check:**
- [ ] Does it solve the stated problem?
- [ ] Code quality is acceptable?
- [ ] Tests are included and passing?
- [ ] Documentation is updated?
- [ ] No obvious bugs or issues?
- [ ] Follows [YOUR PROJECT] code style?
- [ ] No TODO comments without tracking?

**Conflict Analysis:**
- What files does this PR touch?
- Do any overlap with other PRs?
- Are there actual merge conflicts?
- What's the dependency relationship?

**Review Command:**
```bash
gh pr view [PR_NUMBER]
gh pr diff [PR_NUMBER]
gh pr checks [PR_NUMBER]
```

### Step 3: Determine Merge Order (10 minutes)
Based on:
- **Dependencies** - Which PRs depend on others?
- **Risk Level** - Merge safer changes first
- **File Conflicts** - Minimize conflict resolution
- **Priority** - Critical improvements first

Provide recommended merge order with reasoning:
```
1. PR #XX - [Agent/Improvement] - Why first?
2. PR #YY - [Agent/Improvement] - Why second?
3. PR #ZZ - [Agent/Improvement] - Why third?
4. PR #AA - [Agent/Improvement] - Why fourth?
5. PR #BB - [Agent/Improvement] - Why fifth?
```

### Step 4: Check for Conflicts (15 minutes)
For each PR in merge order, identify:
- Which files overlap with later PRs?
- Are there actual conflicts or just touching same files?
- How should conflicts be resolved?
- Should any PRs be rebased first?

### Step 5: Execute Merges (30-60 minutes)
For each PR in order:

**Merge Process:**
```bash
# 1. Review one final time
gh pr view [PR_NUMBER]

# 2. Check CI/tests
gh pr checks [PR_NUMBER]

# 3. Merge (squash recommended)
gh pr merge [PR_NUMBER] --squash --delete-branch

# 4. Verify [BASE_BRANCH] branch
git checkout [dev or main]
git pull origin [dev or main]

# 5. Run tests
[YOUR TEST COMMAND]

# 6. If tests fail, investigate immediately
```

**After EACH merge:**
- Confirm tests still pass
- Check for any issues
- Note any problems before continuing

### Step 6: Final Verification (15 minutes)
After all PRs merged:

**Verification Checklist:**
- [ ] All 5 PRs successfully merged to [BASE_BRANCH]
- [ ] Full test suite passes on [BASE_BRANCH]
- [ ] App builds without errors: [YOUR BUILD COMMAND]
- [ ] No merge conflicts remain
- [ ] All agent branches deleted
- [ ] [BASE_BRANCH] branch is stable and deployable

**Manual Testing:**
- [ ] Run the application
- [ ] Test key functionality: [LIST KEY FEATURES TO TEST]
- [ ] Verify improvements are working
- [ ] Check for any regressions

### Step 7: Documentation (10 minutes)
Update project documentation:
- Update CHANGELOG.md with all improvements
- Update version number if applicable
- Create release notes summary
- Update WORKFLOW_STATE.md with completion
- Update [ANY OTHER PROJECT-SPECIFIC DOCS]

### Step 8: Next Steps Decision (5 minutes)
Recommend next action:
- **Option A:** Merge [BASE_BRANCH] → main (if production ready)
- **Option B:** Start Iteration 2 (more improvements needed)
- **Option C:** Deploy to [STAGING/TESTFLIGHT/ETC] for testing
- **Option D:** Add new features

## Output Required

Please provide:

```markdown
# 📊 INTEGRATION REVIEW SUMMARY
**Project:** [YOUR PROJECT NAME]
**Date:** [DATE]
**Iteration:** [NUMBER]

## 1. PR Overview
| PR # | Agent | Description | Files | Status |
|------|-------|-------------|-------|--------|
| #XX  | Agent 1 | [Description] | N files | ✅/❌ |
| #YY  | Agent 2 | [Description] | N files | ✅/❌ |
| #ZZ  | Agent 3 | [Description] | N files | ✅/❌ |
| #AA  | Agent 4 | [Description] | N files | ✅/❌ |
| #BB  | Agent 5 | [Description] | N files | ✅/❌ |

## 2. Quality Assessment
**PR #XX:** [Pass/Fail] - [Reasoning]
**PR #YY:** [Pass/Fail] - [Reasoning]
**PR #ZZ:** [Pass/Fail] - [Reasoning]
**PR #AA:** [Pass/Fail] - [Reasoning]
**PR #BB:** [Pass/Fail] - [Reasoning]

## 3. Conflict Report
[List of conflicts found and resolution strategy]

## 4. Recommended Merge Order
1. PR #XX - [Why]
2. PR #YY - [Why]
3. PR #ZZ - [Why]
4. PR #AA - [Why]
5. PR #BB - [Why]

## 5. Merge Execution Results
- **PR #XX:** ✅ Merged - Tests passing
- **PR #YY:** ✅ Merged - Tests passing
- **PR #ZZ:** ✅ Merged - Tests passing
- **PR #AA:** ✅ Merged - Tests passing
- **PR #BB:** ✅ Merged - Tests passing

## 6. Final Verification
- **Tests:** [Pass/Fail] - [Details]
- **Build:** [Success/Errors] - [Details]
- **Manual Testing:** [Results]
- **Deployment Ready:** [Yes/No]

## 7. Issues Found
[Any problems discovered during integration]

## 8. Next Steps Recommendation
**Recommendation:** [Option A/B/C/D]

**Reasoning:** [Why this is the best next step]

**Timeline:** [Estimated time]

**Cost:** [If using paid credits]

## 9. Merge Commands Summary
```bash
[Complete list of commands executed]
```

## 10. Metrics
- **PRs Merged:** 5/5
- **Total Files Changed:** [NUMBER]
- **Lines Added:** [NUMBER]
- **Lines Removed:** [NUMBER]
- **Time to Complete:** [DURATION]
- **Issues Encountered:** [NUMBER]
```

---

## Project-Specific Notes
[Add any project-specific considerations here]

**Test Coverage Before:** [X]%
**Test Coverage After:** [Y]%

**Performance Before:** [METRICS]
**Performance After:** [METRICS]

**Known Limitations:** [LIST]

**Technical Debt Added:** [LIST]

**Technical Debt Resolved:** [LIST]

---

**START INTEGRATION NOW**

Begin by listing all open pull requests and analyzing each one.
