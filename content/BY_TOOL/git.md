# Git Configuration

Patterns for git setup and common issues in DP's environment.

---

## SSH vs HTTPS

**DP's repos use SSH authentication, not HTTPS.**

When cloning or if push fails with "could not read Username":

```bash
# Check current remote
git remote -v

# If shows https://github.com/..., switch to SSH:
git remote set-url origin git@github.com:Dparent97/[repo-name].git

# Then push works
git push origin main
```

### Why This Happens
- Fresh Claude sessions don't know the SSH preference
- Some repos were cloned with HTTPS initially
- GitHub CLI (`gh`) defaults to HTTPS

### Prevention
Always check remote URL before pushing. If HTTPS, switch to SSH.

---

## Commit Message Convention

```
type: short description

Types:
- feat:     New feature
- fix:      Bug fix  
- docs:     Documentation only
- refactor: Code change (no new feature or fix)
- test:     Adding tests
- chore:    Maintenance
```

**Never mention AI/Claude in commit messages.**

---

## Branch Naming

```
improve/[N]-short-description   # Multi-agent workflow improvements
feature/add-notifications       # Features
fix/login-timeout              # Bug fixes
```

---

## Common Issues

### "Device not configured" on push
**Cause:** HTTPS remote, no credentials configured
**Fix:** Switch to SSH (see above)

### Stale branches accumulating
**Fix:** Delete after merge:
```bash
git branch -d branch-name           # Local
git push origin --delete branch-name # Remote
git fetch --prune                    # Clean up
```

---

## Projects

All DP repos use SSH:
- Reality-layer
- multi-agent-workflow
- ship-MTA-draft
- AgentOrchestratedCodeFactory

---

## macOS Case Insensitivity

### Filename Case Causes Git Confusion
**Date:** 2025-12-12
**Project:** ship-MTA-draft, AgentOrchestratedCodeFactory
**Context:** Copying CLAUDE.md to repos that had Claude.md

**Problem:**
macOS treats `CLAUDE.md` and `Claude.md` as the same file (case-insensitive filesystem). But Git tracks case differences. This causes confusing states where:
- `ls` shows one file
- `git status` shows modifications to differently-cased name
- Git may track both as separate files on case-sensitive systems

**Solution:**
```bash
# Just stage the file Git is tracking
git add Claude.md  # use whatever case Git shows in status
git commit -m "docs: update Claude.md"
```

**Prevention:**
- Be consistent with filename casing across repos
- Check `git status` output for the exact filename Git is tracking
- If renaming case, do it in two commits: `FILE.md` → `file-temp.md` → `file.md`

---

*Last updated: 2025-12-12*
