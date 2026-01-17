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
git remote set-url origin git@github.com:derekparent/[repo-name].git

# Then push works
git push origin main
```

### Why This Happens
- Fresh Claude sessions don't know the SSH preference
- Some repos were cloned with HTTPS initially
- GitHub CLI (`gh`) defaults to HTTPS

### Prevention
Always check remote URL before pushing. If HTTPS, switch to SSH.

### `gh repo create` Gotcha
**Date:** 2026-01-01

`gh repo create` sets remote to HTTPS even when SSH is preferred:
```bash
# Creates repo but uses HTTPS remote
gh repo create my-repo --private --source=.

# Always follow with:
git remote set-url origin git@github.com:derekparent/my-repo.git
```

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
- ar-id (was Reality-layer)
- maw-mcp
- maintenance-tracker (was ship-MTA-draft)
- skills
- crew-shopping-list
- orb-tool (was oil_record_book_tool)
- voice-assistant

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

## GitHub Username/Repo Rename Checklist

**Date:** 2026-01-16
**Project:** Professional Development
**Context:** Changed GitHub username from Dparent97 to derekparent, renamed multiple repos

**What Needs Updating:**

1. **Git Remotes** (automated):
```bash
find ~/Projects -maxdepth 2 -name ".git" | while read gitdir; do
  repo=$(dirname "$gitdir")
  remote=$(git -C "$repo" remote get-url origin 2>/dev/null)
  if echo "$remote" | grep -q "OLD_USERNAME"; then
    newremote=$(echo "$remote" | sed 's/OLD_USERNAME/NEW_USERNAME/g')
    git -C "$repo" remote set-url origin "$newremote"
    echo "Updated: $repo"
  fi
done
```

2. **Config Files to Update:**
- `~/.claude/CLAUDE.md` - global SSH example and repo list
- `skills/*/data/*.yaml` - project registries
- Project `CLAUDE.md` files - SSH examples
- `README.md` files - clone commands
- `.cursor/rules/` files - project-specific rules

3. **Packaged Exports:**
- `.skill` files need regeneration (they're ZIP archives)
- Any other exported configs

4. **External References:**
- Claude desktop app userPreferences (manual)
- CI/CD configs if any

**Key Insight:** Profile README repo must exactly match username. GitHub auto-renames it when username changes, but links inside need manual update.

---

## Security Audit Pattern for Public Repos

**Date:** 2026-01-16
**Project:** Professional Development
**Context:** Auditing repos before job search to ensure no leaked secrets

**Checklist:**

```bash
# 1. Scan for hardcoded API keys
grep -rE "sk-[a-zA-Z0-9]{20,}|AIza[0-9A-Za-z_-]{35}" /path/to/repo

# 2. Check for committed .env files
git ls-files | grep -E "\.env$|credentials|secret|\.pem$|\.key$"

# 3. Verify .gitignore has secrets patterns
grep -E "\.env|secret|credential" .gitignore

# 4. Scan git history (secrets may be in old commits)
git log --all -p | grep -iE "api_key\s*=|password\s*=" | head -20

# 5. Check for database connection strings with passwords
grep -rE "postgresql://[^:]+:[^@]+@|mysql://[^:]+:[^@]+@" .
```

**Key Points:**
- Fake/example keys in documentation are OK (check context)
- Keys in git history are still exposed even if removed from current code
- Architecture matters: client apps should never have API keys, use backend proxy

---

*Last updated: 2026-01-16*
